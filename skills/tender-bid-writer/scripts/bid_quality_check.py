#!/usr/bin/env python3
"""Lightweight local QC for bid proposal drafts.

This script is intentionally dependency-free so it can run in Codex, OpenClaw,
Hermes, or a plain Python environment.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".html", ".htm", ".json"}
PROPOSAL_EXTENSIONS = TEXT_EXTENSIONS | {".docx"}

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"待补充",
    r"待确认",
    r"公司名称",
    r"项目名称",
    r"客户名称",
    r"此处",
    r"示例",
    r"\{\{[^}]+\}\}",
    r"\[[^\]]*(公司|项目|日期|姓名|金额)[^\]]*\]",
]

EVIDENCE_WORDS = [
    "证书",
    "认证",
    "授权",
    "案例",
    "合同",
    "发票",
    "截图",
    "检测报告",
    "承诺函",
    "人员",
    "社保",
    "资质",
]

REQUIREMENT_HINTS = [
    "必须",
    "须",
    "应",
    "不得",
    "评分",
    "分值",
    "资质",
    "参数",
    "响应",
    "提供",
    "证明",
    "承诺",
]

AI_FLAVOR_PATTERNS = [
    (r"本项目属于[^。；;]{0,80}", "fixed project-classification opening"),
    (r"本节围绕[^。；;]{0,80}(展开|进行|阐述|响应)", "repeated section-opening template"),
    (r"本章节?将从[^。；;]{0,80}(方面|维度|角度)", "chapter preview filler"),
    (r"围绕[^。；;]{0,80}(展开响应|开展工作|进行说明)", "around-topic filler"),
    (r"项目经理会[^。；;]{0,80}", "template project-manager claim"),
    (r"从以往经验看[^。；;]{0,80}", "generic past-experience filler"),
    (r"(控制要点|细化核查|接口联调控制要点)\s*[0-9一二三四五六七八九十]+", "mechanical numbered heading"),
    (r"全(过程|链路|角色|闭环|维度|场景|周期)", "slogan-like 全* phrase"),
    (r"建立健全[^。；;]{0,30}机制", "abstract mechanism claim"),
    (r"(切实保障|有效提升|全面推进|不断完善|充分发挥|持续优化)", "generic official-sounding verb"),
    (r"形成[^。；;]{0,30}闭环", "abstract closed-loop claim"),
    (r"以[^。；;]{0,30}为抓手", "generic 抓手 phrase"),
]

PROJECT_RECORD_WORDS = [
    "台账",
    "记录",
    "清单",
    "签收",
    "验收",
    "检测",
    "巡检",
    "工单",
    "会议纪要",
    "复核",
    "整改",
    "交付",
    "归档",
]

EXCELLENCE_TOPIC_WORDS = [
    "数据一致性校验",
    "接口联调",
    "新旧系统并行运行",
    "切换演练",
    "业务回退",
    "过渡期运维",
]

FLOWCHART_WORDS = [
    "流程图",
    "流程如下",
    "mermaid",
    "graph TD",
    "sequenceDiagram",
]

TABLE_WORDS = [
    "职责矩阵",
    "风险台账",
    "验收映射",
    "接口清单",
    "数据校验",
    "问题分级",
    "交付材料",
    "检查表",
]


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
    except zipfile.BadZipFile:
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
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


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
    phrase_parts = [
        part
        for part in re.split(r"[和及与并]", req_compact)
        if len(part) >= 4
    ]
    if phrase_parts and sum(1 for part in phrase_parts if part in text_compact) >= max(1, int(len(phrase_parts) * 0.6)):
        return True

    tokens = requirement_tokens(requirement)
    if not tokens:
        return True
    hits = sum(1 for token in tokens if token in proposal_text)
    needed = len(tokens) if len(tokens) <= 2 else max(2, int(len(tokens) * 0.6))
    return hits >= needed


def find_ai_flavor_hits(text: str) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    for pattern, label in AI_FLAVOR_PATTERNS:
        for match in re.finditer(pattern, text):
            snippet = normalize(text[max(0, match.start() - 20): match.end() + 40])
            hits.append((label, snippet[:140]))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Check bid proposal draft quality.")
    parser.add_argument("--workspace", required=True, help="Proposal workspace or draft file.")
    parser.add_argument("--requirements", help="Requirement ledger file or directory.")
    parser.add_argument("--proposal", help="Proposal draft file or directory. Defaults to workspace.")
    parser.add_argument("--out", help="Write Markdown report to this path.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    proposal_root = Path(args.proposal).resolve() if args.proposal else workspace
    req_root = Path(args.requirements).resolve() if args.requirements else workspace / "01_requirements"

    findings: list[tuple[str, str, str]] = []

    proposal_files = list(iter_files(proposal_root, PROPOSAL_EXTENSIONS))
    if not proposal_files:
        findings.append(("BLOCKER", "No proposal files found", str(proposal_root)))

    proposal_texts = []
    for path in proposal_files:
        text = read_text(path)
        proposal_texts.append(text)
        if len(text) < 500 and path.suffix.lower() in {".html", ".md", ".txt", ".docx"}:
            findings.append(("WARNING", "Very short draft file", str(path)))
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                findings.append(("BLOCKER", f"Placeholder or unresolved marker matches `{pattern}`", str(path)))
                break

    all_proposal = "\n".join(proposal_texts)

    ai_hits = find_ai_flavor_hits(all_proposal)
    if len(ai_hits) >= 8:
        findings.append(("WARNING", f"{len(ai_hits)} AI-flavor/template phrases found; run human-prose rewrite pass", "human bid prose"))
    elif len(ai_hits) >= 3:
        findings.append(("WARNING", f"{len(ai_hits)} possible AI-flavor/template phrases found", "human bid prose"))

    record_mentions = sum(all_proposal.count(word) for word in PROJECT_RECORD_WORDS)
    if len(all_proposal) > 5000 and record_mentions < 8:
        findings.append(("WARNING", "Long proposal text has few concrete records/forms/acceptance artifacts", "human bid prose"))

    excellence_hits = [word for word in EXCELLENCE_TOPIC_WORDS if word in all_proposal]
    if any(word in all_proposal for word in ("数据迁移", "系统切换", "平台", "接口", "集成")):
        if len(excellence_hits) < 3:
            findings.append(("WARNING", "Complex platform/integration text mentions related work but covers few of the six excellence topics", "chapter structure"))

    flow_mentions = sum(all_proposal.count(word) for word in FLOWCHART_WORDS)
    table_mentions = sum(all_proposal.count(word) for word in TABLE_WORDS)
    if len(all_proposal) > 8000 and flow_mentions < 1:
        findings.append(("WARNING", "Long chapter/proposal text appears to lack a process or flow diagram", "chapter structure"))
    if len(all_proposal) > 8000 and table_mentions < 2:
        findings.append(("WARNING", "Long chapter/proposal text has few scoring/acceptance-oriented tables", "chapter structure"))

    requirement_files = list(iter_files(req_root, TEXT_EXTENSIONS)) if req_root.exists() else []
    requirement_text = "\n".join(read_text(path) for path in requirement_files)
    requirements = split_requirement_lines(requirement_text)

    if req_root.exists() and not requirement_files:
        findings.append(("WARNING", "Requirements path exists but contains no readable requirement files", str(req_root)))
    if not req_root.exists():
        findings.append(("WARNING", "No 01_requirements directory or requirements file supplied", str(req_root)))

    missing = []
    for req in requirements[:200]:
        if not requirement_covered(req, all_proposal):
            missing.append(req)
    if missing:
        findings.append(("WARNING", f"{len(missing)} extracted requirements may not be covered in proposal text", "requirements coverage"))

    evidence_mentions = sum(all_proposal.count(word) for word in EVIDENCE_WORDS)
    if requirement_text and any(word in requirement_text for word in EVIDENCE_WORDS) and evidence_mentions < 5:
        findings.append(("WARNING", "Requirements mention evidence/qualification, but proposal has few evidence references", "evidence matrix"))

    blocker_count = sum(1 for severity, _, _ in findings if severity == "BLOCKER")
    warning_count = sum(1 for severity, _, _ in findings if severity == "WARNING")

    report = [
        "# Bid Quality Check Report",
        "",
        f"- Workspace: `{workspace}`",
        f"- Proposal files scanned: {len(proposal_files)}",
        f"- Requirement files scanned: {len(requirement_files)}",
        f"- Blockers: {blocker_count}",
        f"- Warnings: {warning_count}",
        "",
        "## Findings",
        "",
    ]

    if findings:
        for severity, message, location in findings:
            report.append(f"- **{severity}**: {message} ({location})")
    else:
        report.append("- No blocker or warning found by automated checks.")

    if missing:
        report.extend(["", "## Possible Coverage Gaps", ""])
        for item in missing[:30]:
            report.append(f"- {item}")

    if ai_hits:
        report.extend(["", "## Possible AI-Flavor Phrases", ""])
        for label, snippet in ai_hits[:30]:
            report.append(f"- {label}: {snippet}")

    report.extend(
        [
            "",
            "## Manual Checks Still Required",
            "",
            "- Verify pass/fail clauses, scoring criteria, required forms, and seal/signature rules against the tender source.",
            "- Verify every certificate, case, authorization, staffing, price, date, and legal commitment with user-provided evidence.",
            "- Rewrite repeated template openings into purchaser scenes, execution stages, responsible roles, records/forms, and acceptance outputs.",
            "- Check chapter structure balance: light chapters stay concise, priority topics go deeper,正文 sits under leaf headings, and same-level heading counts are not mechanically uniform.",
            "- Check each major chapter has a useful flowchart and table, and final DOCX chapters use the master template, Heading 1-9/TB styles, and sortable files under 分章节定稿.",
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

    return 2 if blocker_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
