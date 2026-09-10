#!/usr/bin/env python3
"""Lightweight local QC for bid proposal drafts.

Dependency-free so it can run in Codex, OpenClaw, Hermes, or any plain
Python 3.9+ environment.

Checks:
- Draft/placeholder traces (refined to avoid false positives on legitimate
  phrases such as ``本项目名称为...`` in formal chapters).
- Very short draft files.
- Thin sections: headings followed by almost no substantive content.
- AI-flavor slogan density (空洞排比、互联网黑话).
- Cross-chapter copy-paste duplication.
- Page-budget estimate against ``--target-pages``.
- Requirement coverage gap between requirement ledgers and proposal text.
- Evidence-reference density when requirements demand certificates/cases.

Outputs a Markdown report (``--out``) and optionally machine-readable JSON
(``--json``) for agent post-processing.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
import zlib
from collections import Counter
from pathlib import Path
from typing import Iterable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".html", ".htm", ".json"}
PROPOSAL_EXTENSIONS = TEXT_EXTENSIONS | {".docx"}

SEVERITY_ORDER = {"BLOCKER": 0, "WARNING": 1, "INFO": 2}

# ---------------------------------------------------------------------------
# Placeholder / draft-trace patterns.
# Each entry: (label, regex, severity). Patterns are written to match genuine
# template traces, not normal prose such as ``项目名称为...`` or table headers.
# ---------------------------------------------------------------------------
PLACEHOLDER_PATTERNS: list[tuple[str, str, str]] = [
    ("TODO/TBD/FIXME marker", r"\b(?:TODO|TBD|FIXME|XXX)\b", "BLOCKER"),
    ("待办标记", r"待补充|待完善|待更新|待填写|待提供|待定稿|待商定|待补充材料", "BLOCKER"),
    ("内部确认痕迹", r"待确认|内部评审|本章自查|草稿版|如有证据再补", "BLOCKER"),
    ("占位指令", r"此处填写|此处插入|在此填写|在此插入|填写处|替换为 actual|占位符", "BLOCKER"),
    ("公司名称模板", r"(?:公司名称|投标人名称|供应商名称)\s*[:：]?\s*(?:填写|待|【|___|××|XX公司|某某公司)", "BLOCKER"),
    ("项目名称模板", r"(?:项目名称|采购项目名称|项目编号)\s*[:：]?\s*(?:填写|待|【|___|××|XX项目|某某项目)", "BLOCKER"),
    ("模板花括号", r"\{\{[^}]{1,60}\}\}", "BLOCKER"),
    ("方括号占位", r"【(?:待|填写|占位|公司名|项目名)[^】]{0,20}】", "BLOCKER"),
    ("方括号英文占位", r"\[[^\]\[]{0,12}(?:公司|项目|日期|姓名|金额|填写)[^\]\[]{0,12}\]", "WARNING"),
    ("示例文本痕迹", r"示例\s*[:：]|示例如下|（示例）|\(示例\)|某某(?:公司|项目|系统)", "WARNING"),
    ("泛化承诺", r"(?:建立|健全|完善)(?:相关)?(?:机制|制度|体系)(?:，|,)?(?:确保|保障)?(?:各项)?(?:工作)?(?:顺利|有序|规范)(?:开展|进行)", "WARNING"),
]

# Phrases that are almost always AI/template flavor in formal bid prose.
BUZZWORD_LIMITS: dict[str, int] = {
    "赋能": 2,
    "抓手": 1,
    "拉通": 1,
    "颗粒度": 1,
    "打法": 1,
    "组合拳": 1,
    "底层逻辑": 1,
    "护城河": 1,
    "互联网思维": 1,
    "新质生产力": 3,
}

# Slogan words allowed in moderation; only density triggers a warning.
SLOGAN_WORDS = [
    "全过程",
    "全流程",
    "全链路",
    "全角色",
    "全场景",
    "全方位",
    "全生命周期",
    "全天候",
    "一站式",
    "闭环",
]

# Adjacent symmetric slogans such as 全过程、全链路、全闭环
SYMMETRIC_SLOGAN_RE = re.compile(r"全[\u4e00-\u9fff]{2,4}\s*[、，,；;]?\s*全[\u4e00-\u9fff]{2,4}(?:\s*[、，,；;]?\s*全[\u4e00-\u9fff]{2,4})?")

EVIDENCE_WORDS = [
    "证书", "认证", "授权", "案例", "合同", "发票", "截图", "检测报告",
    "承诺函", "人员", "社保", "资质",
]

REQUIREMENT_HINTS = [
    "必须", "须", "应", "不得", "评分", "分值", "资质", "参数",
    "响应", "提供", "证明", "承诺",
]

DEFAULT_CHARS_PER_PAGE = 900  # rough CJK chars on one A4 page


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return read_docx_text(path)
    raw = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="ignore")
    if suffix in {".html", ".htm"}:
        text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        text = html.unescape(text)
    if suffix == ".json":
        try:
            obj = json.loads(text)
            text = json_to_text(obj)
        except json.JSONDecodeError:
            pass
    return normalize(text)


def read_docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            parts = [
                archive.read(name).decode("utf-8", errors="ignore")
                for name in archive.namelist()
                if name.startswith("word/") and name.endswith(".xml")
            ]
    except (zipfile.BadZipFile, OSError):
        return ""
    text = "\n".join(parts)
    text = re.sub(r"<[^>]+>", " ", text)
    return normalize(html.unescape(text))


def json_to_text(obj: object) -> str:
    if isinstance(obj, dict):
        return "\n".join(str(k) + ": " + json_to_text(v) for k, v in obj.items())
    if isinstance(obj, list):
        return "\n".join(json_to_text(v) for v in obj)
    return "" if obj is None else str(obj)


def normalize(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = text.replace("\u3000", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def iter_files(root: Path, extensions: set[str]) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in extensions:
            yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


# ---------------------------------------------------------------------------
# Requirement coverage
# ---------------------------------------------------------------------------

def split_requirement_lines(text: str) -> list[str]:
    lines = re.split(r"[。\n\r；;]", text)
    results: list[str] = []
    for line in lines:
        item = normalize(line)
        if len(item) < 8:
            continue
        if any(hint in item for hint in REQUIREMENT_HINTS):
            results.append(item[:160])
    return dedupe(results)


def dedupe(items: Iterable[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def requirement_tokens(requirement: str) -> list[str]:
    tokens = re.findall(r"[\w\u4e00-\u9fff]{2,}", requirement)
    stop = {"必须", "提供", "要求", "响应", "评分", "满足", "不得", "进行", "技术参数"}
    return [token for token in tokens if token not in stop][:8]


def requirement_covered(requirement: str, proposal_text: str) -> bool:
    req_compact = re.sub(r"[\s#：:，,。；;、]+", "", requirement)
    text_compact = re.sub(r"\s+", "", proposal_text)
    for word in ("必须", "须", "应", "提供", "要求", "响应", "评分", "满足", "不得", "进行", "技术参数"):
        req_compact = req_compact.replace(word, "")
    if 4 <= len(req_compact) <= 80 and req_compact in text_compact:
        return True
    phrase_parts = [part for part in re.split(r"[和及与并]", req_compact) if len(part) >= 4]
    if phrase_parts and sum(1 for part in phrase_parts if part in text_compact) >= max(1, int(len(phrase_parts) * 0.6)):
        return True
    tokens = requirement_tokens(requirement)
    if not tokens:
        return True
    hits = sum(1 for token in tokens if token in proposal_text)
    needed = len(tokens) if len(tokens) <= 2 else max(2, int(len(tokens) * 0.6))
    return hits >= needed


# ---------------------------------------------------------------------------
# Section analysis (markdown + HTML)
# ---------------------------------------------------------------------------

SECTION_EXCLUDE_RE = re.compile(
    r"目录|contents|修订记录|版本记录|attach|附件清单", re.IGNORECASE
)


def extract_sections_markdown(text: str) -> list[tuple[str, int, str]]:
    sections: list[tuple[str, int, str]] = []
    current_heading = None
    current_level = 0
    buffer: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*\S)?\s*$", line)
        if match:
            if current_heading is not None:
                sections.append((current_heading, current_level, "\n".join(buffer)))
            current_level = len(match.group(1))
            current_heading = (match.group(2) or "").strip()
            buffer = []
        elif current_heading is not None:
            buffer.append(line)
    if current_heading is not None:
        sections.append((current_heading, current_level, "\n".join(buffer)))
    return sections


def extract_sections_html(raw_text: str) -> list[tuple[str, int, str]]:
    stripped = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw_text)
    pattern = re.compile(r"<h([1-4])[^>]*>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
    matches = list(pattern.finditer(stripped))
    sections: list[tuple[str, int, str]] = []
    for index, match in enumerate(matches):
        level = int(match.group(1))
        heading_text = normalize(re.sub(r"<[^>]+>", " ", match.group(2)))
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(stripped)
        body = stripped[body_start:body_end]
        sections.append((heading_text, level, body))
    return sections


def section_body_stats(body: str, is_html: bool) -> tuple[int, int, bool]:
    """Return (paragraph_count, body_char_len, has_table)."""
    has_table = bool(re.search(r"<table", body, re.IGNORECASE)) if is_html else False
    if is_html:
        body_text = re.sub(r"(?s)<[^>]+>", "\n", body)
        body_text = html.unescape(body_text)
        para_count = len(re.findall(r"<p[\s>]", body, re.IGNORECASE))
    else:
        body_text = body
        para_count = 0
    # Markdown paragraphs: blank-line separated chunks.
    chunks = [c.strip() for c in re.split(r"\n\s*\n", body_text) if c.strip()]
    table_rows = sum(1 for line in body_text.splitlines() if line.strip().startswith("|"))
    if table_rows >= 3:
        has_table = True
    real_chunks = [c for c in chunks if len(re.sub(r"[\s|:\-—]+", "", c)) >= 30]
    if is_html and para_count == 0:
        para_count = len(real_chunks)
    if not is_html:
        para_count = len(real_chunks)
    body_len = len(re.sub(r"\s+", "", body_text))
    return para_count, body_len, has_table


def find_thin_sections(path: Path, raw_text: str) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm"}:
        sections = extract_sections_html(raw_text)
        is_html = True
    elif suffix in {".md", ".markdown", ".txt"}:
        sections = extract_sections_markdown(raw_text)
        is_html = False
    else:
        return []
    if len(sections) < 3:
        return []
    thin: list[dict] = []
    for index, (heading, level, body) in enumerate(sections):
        if not heading or SECTION_EXCLUDE_RE.search(heading):
            continue
        if level > 3:
            continue
        para_count, body_len, has_table = section_body_stats(body, is_html)
        if para_count == 0 and body_len == 0:
            # Pure container heading: all content lives in child sections.
            continue
        if has_table or para_count >= 2 or body_len >= 200:
            continue
        thin.append({
            "file": str(path),
            "heading": heading[:60],
            "level": level,
            "paragraphs": para_count,
            "chars": body_len,
        })
    return thin


# ---------------------------------------------------------------------------
# AI-flavor and duplication checks
# ---------------------------------------------------------------------------

def find_slogan_issues(text: str) -> list[dict]:
    issues: list[dict] = []
    total_units = max(len(re.findall(r"[\u4e00-\u9fff]", text)), 1)
    per_10k = total_units / 10000.0

    for word, absolute_limit in BUZZWORD_LIMITS.items():
        count = text.count(word)
        if count >= absolute_limit and count >= 2:
            issues.append({
                "type": "buzzword",
                "phrase": word,
                "count": count,
                "hint": f"互联网黑话/空泛词 `{word}` 出现 {count} 次，建议替换为具体机制、角色或数据",
            })

    density_limit = max(4, int(per_10k * 1.5))
    for word in SLOGAN_WORDS:
        count = text.count(word)
        if count >= density_limit:
            issues.append({
                "type": "slogan",
                "phrase": word,
                "count": count,
                "hint": f"口号词 `{word}` 出现 {count} 次（密度约 {count / per_10k:.1f}/千字），存在排比式空洞表述风险",
            })

    symmetric = SYMMETRIC_SLOGAN_RE.findall(text)
    if len(symmetric) >= 2:
        issues.append({
            "type": "symmetric-slogan",
            "phrase": " / ".join(dict.fromkeys(symmetric)).replace(" ", "")[:80],
            "count": len(symmetric),
            "hint": f"检测到 {len(symmetric)} 处『全X、全Y』式对称排比，属于典型 AI 味句式，建议改写为具体项目场景",
        })
    return issues


def find_duplication(
    file_texts: list[tuple[Path, str]],
    window: int = 40,
    sample_mod: int = 5,
) -> tuple[list[dict], list[dict]]:
    """Detect duplicated long passages across files and inside one file.

    Uses content-hashed character shingles (crc32 sampling) so detection is
    independent of where a repeated passage happens to start in each file.
    Returns (cross_file_pairs, self_repetition).
    """
    compact_texts = [re.sub(r"\s", "", text) for _, text in file_texts]

    chunk_files: dict[int, set[int]] = {}
    chunk_sample: dict[int, str] = {}
    self_dup: list[dict] = []

    for idx, compact in enumerate(compact_texts):
        if len(compact) < window * 3:
            continue
        local: Counter = Counter()
        for start in range(0, len(compact) - window + 1):
            crc = zlib.crc32(compact[start:start + window].encode("utf-8"))
            if crc % sample_mod:
                continue
            chunk_files.setdefault(crc, set()).add(idx)
            if len(chunk_sample) < 20000:
                chunk_sample.setdefault(crc, compact[start:start + window])
            local[crc] += 1
        repeated_hashes = sum(count - 1 for count in local.values() if count > 1)
        if repeated_hashes * sample_mod >= 100:
            top_crc = max(local, key=lambda c: local[c] if c in chunk_sample else 0)
            self_dup.append({
                "file": str(file_texts[idx][0]),
                "repeated_chars_approx": repeated_hashes * sample_mod,
                "sample": chunk_sample.get(top_crc, "")[:60],
            })

    pair_counts: Counter = Counter()
    pair_samples: dict[tuple[int, int], list[str]] = {}
    for crc, files in chunk_files.items():
        if len(files) < 2:
            continue
        ordered = sorted(files)
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                pair = (ordered[i], ordered[j])
                pair_counts[pair] += 1
                samples = pair_samples.setdefault(pair, [])
                if len(samples) < 2 and crc in chunk_sample:
                    samples.append(chunk_sample[crc][:60])

    file_lengths = [len(compact) for compact in compact_texts]
    results: list[dict] = []
    for (idx_a, idx_b), shared_hashes in pair_counts.most_common(10):
        shared_chars = shared_hashes * sample_mod
        base = min(file_lengths[idx_a], file_lengths[idx_b]) or 1
        ratio = shared_chars / base
        if shared_chars >= 100 or ratio >= 0.08:
            results.append({
                "files": [str(file_texts[idx_a][0]), str(file_texts[idx_b][0])],
                "shared_chars_approx": shared_chars,
                "ratio": round(ratio, 3),
                "samples": pair_samples.get((idx_a, idx_b), []),
            })
    return results, self_dup


def estimate_pages(text: str, chars_per_page: int) -> int:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_words = len(re.findall(r"[A-Za-z0-9]+", text))
    weighted = cjk + int(latin_words * 0.5)
    return int(weighted / max(chars_per_page, 100))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Check bid proposal draft quality.")
    parser.add_argument("--workspace", required=True, help="Proposal workspace or draft file.")
    parser.add_argument("--requirements", help="Requirement ledger file or directory.")
    parser.add_argument("--proposal", help="Proposal draft file or directory. Defaults to workspace.")
    parser.add_argument("--out", help="Write Markdown report to this path.")
    parser.add_argument("--json", dest="json_out", help="Write machine-readable JSON report to this path.")
    parser.add_argument("--target-pages", type=int, help="Expected full-proposal page count for budget check.")
    parser.add_argument("--chars-per-page", type=int, default=DEFAULT_CHARS_PER_PAGE,
                        help=f"CJK chars per page for estimation (default {DEFAULT_CHARS_PER_PAGE}).")
    parser.add_argument("--fail-on-warning", action="store_true",
                        help="Exit with code 1 when warnings are found.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    proposal_root = Path(args.proposal).resolve() if args.proposal else workspace
    req_root = Path(args.requirements).resolve() if args.requirements else workspace / "01_requirements"

    findings: list[tuple[str, str, str]] = []

    def add_finding(severity: str, message: str, location: str) -> None:
        findings.append((severity, message, location))

    proposal_files = list(iter_files(proposal_root, PROPOSAL_EXTENSIONS))
    if not proposal_files:
        add_finding("BLOCKER", "No proposal files found", str(proposal_root))

    proposal_texts: list[tuple[Path, str]] = []
    all_thin_sections: list[dict] = []
    for path in proposal_files:
        raw = path.read_text(encoding="utf-8", errors="ignore") if path.suffix.lower() in TEXT_EXTENSIONS else ""
        text = read_text(path)
        proposal_texts.append((path, text))
        if len(text) < 500 and path.suffix.lower() in {".html", ".md", ".txt", ".docx"}:
            add_finding("WARNING", "Very short draft file (suspiciously thin chapter)", str(path))
        for label, pattern, severity in PLACEHOLDER_PATTERNS:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                snippet = text[max(match.start() - 15, 0):match.end() + 15].strip()
                add_finding(severity, f"Draft/placeholder trace `{label}`: …{snippet}…", str(path))
                break
        if raw:
            all_thin_sections.extend(find_thin_sections(path, raw))

    all_proposal = "\n".join(text for _, text in proposal_texts)
    total_chars = len(re.sub(r"\s", "", all_proposal))
    estimated_pages = estimate_pages(all_proposal, args.chars_per_page)

    for item in all_thin_sections[:20]:
        add_finding(
            "WARNING",
            f"Thin section `{item['heading']}`: {item['paragraphs']} paragraph(s), {item['chars']} chars "
            f"(formal sections should normally have 3-5 substantive paragraphs or a table)",
            item["file"],
        )

    # Page budget check.
    page_info = {
        "total_chars": total_chars,
        "estimated_pages": estimated_pages,
        "chars_per_page": args.chars_per_page,
        "target_pages": args.target_pages,
    }
    if args.target_pages:
        floor = int(args.target_pages * 0.85)
        ceiling = int(args.target_pages * 1.3)
        if estimated_pages < floor:
            add_finding("WARNING",
                        f"Estimated length {estimated_pages} pages is below 85% of target {args.target_pages} pages",
                        "page budget")
        elif estimated_pages > ceiling:
            add_finding("INFO",
                        f"Estimated length {estimated_pages} pages exceeds 130% of target {args.target_pages} pages; "
                        "check tender page cap and trim padded prose",
                        "page budget")
        else:
            add_finding("INFO",
                        f"Estimated length {estimated_pages} pages is within budget around target {args.target_pages} pages",
                        "page budget")

    # Requirement coverage.
    requirement_files = list(iter_files(req_root, TEXT_EXTENSIONS)) if req_root.exists() else []
    requirement_text = "\n".join(read_text(path) for path in requirement_files)
    requirements = split_requirement_lines(requirement_text)

    if req_root.exists() and not requirement_files:
        add_finding("WARNING", "Requirements path exists but contains no readable requirement files", str(req_root))
    if not req_root.exists():
        add_finding("WARNING", "No 01_requirements directory or requirements file supplied", str(req_root))

    missing: list[str] = []
    for req in requirements[:200]:
        if not requirement_covered(req, all_proposal):
            missing.append(req)
    if missing:
        add_finding("WARNING",
                    f"{len(missing)}/{min(len(requirements), 200)} extracted requirements may not be covered in proposal text",
                    "requirements coverage")

    evidence_mentions = sum(all_proposal.count(word) for word in EVIDENCE_WORDS)
    if requirement_text and any(word in requirement_text for word in EVIDENCE_WORDS) and evidence_mentions < 5:
        add_finding("WARNING",
                    "Requirements mention evidence/qualification, but proposal has few evidence references",
                    "evidence matrix")

    # AI-flavor and duplication.
    slogan_issues = find_slogan_issues(all_proposal)
    for item in slogan_issues:
        add_finding("WARNING", item["hint"], "AI-flavor check")

    duplication, self_repetition = find_duplication(proposal_texts)
    for item in duplication:
        sample = f", e.g. …{item['samples'][0]}…" if item["samples"] else ""
        add_finding("WARNING",
                    f"Chapters share about {item['shared_chars_approx']} duplicated chars ({item['ratio']:.0%} of the smaller file){sample} — possible copy-paste padding",
                    "cross-chapter duplication")
    for item in self_repetition[:5]:
        add_finding("WARNING",
                    f"File repeats about {item['repeated_chars_approx']} chars of its own text, e.g. …{item['sample']}… — possible copy-paste padding",
                    item["file"])

    blocker_count = sum(1 for severity, _, _ in findings if severity == "BLOCKER")
    warning_count = sum(1 for severity, _, _ in findings if severity == "WARNING")
    info_count = sum(1 for severity, _, _ in findings if severity == "INFO")

    # ------------------------------------------------------------------ JSON
    json_payload = {
        "workspace": str(workspace),
        "summary": {
            "proposal_files": len(proposal_files),
            "requirement_files": len(requirement_files),
            "requirements_checked": min(len(requirements), 200),
            "requirements_missing": len(missing),
            "blockers": blocker_count,
            "warnings": warning_count,
            "infos": info_count,
            "page_estimate": page_info,
            "exit_code": 2 if blocker_count else (1 if args.fail_on_warning and warning_count else 0),
        },
        "findings": [
            {"severity": severity, "message": message, "location": location}
            for severity, message, location in sorted(findings, key=lambda f: SEVERITY_ORDER.get(f[0], 9))
        ],
        "thin_sections": all_thin_sections[:20],
        "ai_flavor": slogan_issues,
        "duplication": duplication,
        "self_repetition": self_repetition[:5],
        "missing_requirements": missing[:50],
    }
    if args.json_out:
        json_path = Path(args.json_out).resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # --------------------------------------------------------------- Markdown
    report = [
        "# Bid Quality Check Report",
        "",
        f"- Workspace: `{workspace}`",
        f"- Proposal files scanned: {len(proposal_files)}",
        f"- Requirement files scanned: {len(requirement_files)}",
        f"- Total proposal length: about {total_chars} chars ≈ {estimated_pages} pages"
        + (f" (target {args.target_pages} pages)" if args.target_pages else ""),
        f"- Blockers: {blocker_count} | Warnings: {warning_count} | Info: {info_count}",
        "",
        "## Findings",
        "",
    ]
    if findings:
        for severity, message, location in sorted(findings, key=lambda f: SEVERITY_ORDER.get(f[0], 9)):
            report.append(f"- **{severity}**: {message} ({location})")
    else:
        report.append("- No blocker or warning found by automated checks.")

    if all_thin_sections:
        report.extend(["", "## Thin Sections", ""])
        for item in all_thin_sections[:20]:
            report.append(f"- `{item['heading']}` ({item['paragraphs']} para / {item['chars']} chars) in {item['file']}")

    if slogan_issues:
        report.extend(["", "## AI-Flavor Signals", ""])
        for item in slogan_issues:
            report.append(f"- {item['hint']}")

    if duplication:
        report.extend(["", "## Cross-Chapter Duplication", ""])
        for item in duplication:
            report.append(f"- `{item['files'][0]}` ↔ `{item['files'][1]}`: {item['shared_chars_approx']} duplicated chars ({item['ratio']:.0%})")

    if missing:
        report.extend(["", "## Possible Coverage Gaps", ""])
        for item in missing[:30]:
            report.append(f"- {item}")

    report.extend(
        [
            "",
            "## Manual Checks Still Required",
            "",
            "- Verify pass/fail clauses, scoring criteria, required forms, and seal/signature rules against the tender source.",
            "- Verify every certificate, case, authorization, staffing, price, date, and legal commitment with user-provided evidence.",
            "- Confirm final DOCX/PDF formatting after conversion.",
        ]
    )

    output = "\n".join(report) + "\n"
    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    if blocker_count:
        return 2
    if args.fail_on_warning and warning_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
