#!/usr/bin/env python3
"""Patch Codex documents render_docx.py for Windows LibreOffice rendering.

This fixes two Windows-specific issues seen when skills render DOCX files:

1. LibreOffice receives an invalid UserInstallation URI such as
   ``file://C:\\Users\\...`` instead of ``file:///C:/Users/...``.
2. pdf2image cannot find bundled Poppler executables when only ``.cmd``
   wrappers are on PATH.

The script is idempotent and creates a timestamped backup before editing.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import shutil
import sys
from pathlib import Path


HELPER_BLOCK = '''

def _find_poppler_path() -> str | None:
    """Find bundled Poppler binaries for pdf2image on Windows."""

    candidates: list[str] = []

    python_root = os.path.dirname(sys.executable)
    if os.path.basename(python_root) == "python":
        dependencies_root = os.path.dirname(python_root)
        if os.path.basename(dependencies_root) == "dependencies":
            candidates.append(
                os.path.join(dependencies_root, "native", "poppler", "Library", "bin")
            )

    current = os.path.dirname(os.path.realpath(__file__))
    while current and current != os.path.dirname(current):
        if os.path.basename(current) in {"codex-primary-runtime", "openai-primary-runtime"}:
            candidates.append(
                os.path.join(
                    current, "dependencies", "native", "poppler", "Library", "bin"
                )
            )
            break
        current = os.path.dirname(current)

    for candidate in candidates:
        if os.path.isfile(os.path.join(candidate, "pdfinfo.exe")):
            return candidate
    return None
'''


URI_HELPER_BLOCK = '''

def _lo_user_installation_arg(user_profile: str) -> str:
    """Return LibreOffice's UserInstallation env argument as a valid file URI."""

    path = os.path.abspath(user_profile)
    if os.name == "nt":
        uri = "file:///" + path.replace("\\\\", "/")
    else:
        uri = "file://" + path
    return "-env:UserInstallation=" + uri
'''


def default_render_paths() -> list[Path]:
    home = Path.home()
    roots = [
        home / ".codex" / "plugins" / "cache" / "openai-primary-runtime",
        home / ".codex" / "plugins" / "cache" / "openai-bundled",
    ]
    found: list[Path] = []
    for root in roots:
        if root.exists():
            found.extend(root.rglob("skills/documents/render_docx.py"))
    return sorted(set(found))


def patch_text(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    if "def _find_poppler_path()" not in text:
        marker = "\ndef calc_dpi_via_ooxml_docx("
        if marker not in text:
            raise RuntimeError("Could not locate insertion point for _find_poppler_path")
        text = text.replace(marker, HELPER_BLOCK + marker, 1)
        changes.append("added _find_poppler_path")

    if "def _lo_user_installation_arg(" not in text:
        marker = "\ndef _run_cmd("
        if marker not in text:
            raise RuntimeError("Could not locate insertion point for _lo_user_installation_arg")
        text = text.replace(marker, URI_HELPER_BLOCK + marker, 1)
        changes.append("added _lo_user_installation_arg")

    old = '"-env:UserInstallation=file://" + user_profile'
    if old in text:
        text = text.replace(old, "_lo_user_installation_arg(user_profile)")
        changes.append("fixed LibreOffice UserInstallation URI")

    old = "pdfinfo_from_path(pdf_path)"
    new = "pdfinfo_from_path(pdf_path, poppler_path=_find_poppler_path())"
    if old in text:
        text = text.replace(old, new)
        changes.append("passed Poppler path to pdfinfo_from_path")

    needle = 'output_file="page",\n                ),'
    replacement = 'output_file="page",\n                    poppler_path=_find_poppler_path(),\n                ),'
    if needle in text and "poppler_path=_find_poppler_path()" not in text[text.find(needle) - 300 : text.find(needle) + 200]:
        text = text.replace(needle, replacement, 1)
        changes.append("passed Poppler path to convert_from_path")

    return text, changes


def patch_file(path: Path, dry_run: bool) -> list[str]:
    original = path.read_text(encoding="utf-8")
    updated, changes = patch_text(original)
    if not changes:
        return []

    if not dry_run:
        stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_suffix(path.suffix + f".bak-{stamp}")
        shutil.copy2(path, backup)
        path.write_text(updated, encoding="utf-8")
    return changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="Specific render_docx.py path to patch")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    args = parser.parse_args()

    targets = [Path(args.path)] if args.path else default_render_paths()
    if not targets:
        print("No render_docx.py files found under the Codex plugin cache.", file=sys.stderr)
        return 1

    changed = 0
    for target in targets:
        if not target.exists():
            print(f"missing: {target}", file=sys.stderr)
            continue
        changes = patch_file(target, args.dry_run)
        if changes:
            changed += 1
            action = "would patch" if args.dry_run else "patched"
            print(f"{action}: {target}")
            for change in changes:
                print(f"  - {change}")
        else:
            print(f"already ok: {target}")

    return 0 if changed or targets else 1


if __name__ == "__main__":
    raise SystemExit(main())
