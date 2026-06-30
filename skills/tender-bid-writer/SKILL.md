---
name: tender-bid-writer
description: End-to-end tender and bid proposal workflow for Chinese government, enterprise, and integration projects. Use when Codex/OpenClaw/Hermes needs to analyze bidding documents, extract scoring criteria, qualification requirements, technical specifications, and business clauses; build a MECE proposal outline and chapter briefs; draft technical or service proposal chapters; merge and quality-check HTML/Markdown/DOCX outputs; simulate multi-expert bid review; iterate revisions; and prepare final delivery checklists for tender submissions.
---

# Tender Bid Writer

## Operating Rule

Treat the tender document as the source of truth. Do not invent qualifications, certifications, past projects, prices, delivery dates, or manufacturer commitments. Mark unknowns as `待确认` and ask for evidence when a claim affects compliance or scoring.

## Workflow

1. **Intake and workspace setup**
   - Locate tender files, annexes, drawings, templates, clarification notices, and mandatory response forms.
   - Create a working structure if none exists:
     - `00_source/` original tender files and extracted text
     - `01_requirements/` scoring, qualifications, technical parameters, business clauses, deliverables, forms
     - `02_outline/` proposal outline and per-chapter briefs
     - `03_chapters/` chapter drafts, preferably HTML when diagrams are needed
     - `04_merge/` merged proposal
     - `05_qc/` quality checks and review records
     - `06_delivery/` final DOCX/PDF/HTML and delivery checklist

2. **Requirement extraction**
   - Extract four requirement ledgers before drafting: scoring criteria, qualification requirements, technical specifications, and business clauses.
   - Preserve exact source anchors where possible: file name, page, section, table row, or clause number.
   - Classify each requirement as `mandatory`, `scored`, `contractual`, `format`, or `evidence`.
   - Stop and report conflicts, missing annexes, unreadable scans, ambiguous scoring language, or hard pass/fail risks.

3. **Outline and chapter briefs**
   - Build a MECE outline that maps every scored and mandatory requirement to exactly one primary response location.
   - Write a brief for every chapter before drafting: chapter goal, source requirements, claims allowed, evidence needed, diagrams/tables, and acceptance checks.
   - Ask for human confirmation before full drafting when the outline controls compliance or a large document.

4. **Draft chapters**
   - Draft one chapter at a time from the approved brief.
   - Prefer HTML for long technical方案 chapters that need SVG architecture diagrams, flowcharts, tables, and later DOCX conversion.
   - After each chapter, run a local self-check: requirement coverage, forbidden placeholders, evidence gaps, consistency with prior chapters, and evaluator readability.

5. **Merge and quality check**
   - Merge chapters only after chapter-level checks pass.
   - Run deterministic checks with `scripts/bid_quality_check.py` when files are available.
   - Produce a QC report listing blockers, warnings, traceability gaps, and recommended fixes.

6. **Expert review simulation**
   - Review from at least five perspectives when the bid is substantial: compliance officer, technical architect, scoring evaluator, delivery/operations lead, and commercial/legal reviewer.
   - Score against the tender scoring rubric when available.
   - Convert review comments into a revision plan with owner, target chapter, evidence needed, and expected scoring impact.

7. **Iterate to final**
   - Repeat review and revision until the user accepts the risk level or the score target is reached.
   - Prepare a delivery checklist: final files, response forms, evidence attachments, unresolved confirmations, signature/seal items, and submission format.

## Resource Loading

- Read `references/workflow.md` for the detailed article-inspired process, output files, and stage gates.
- Read `references/checklists.md` when extracting requirements, writing briefs, or running expert review.
- Read `references/platform-compatibility.md` when installing or adapting this skill for Codex, OpenClaw, or Hermes.
- Use `scripts/bid_quality_check.py` for local proposal checks when draft files exist.

## Output Standards

- Keep every key claim traceable to tender text, user-provided company evidence, or a clear assumption.
- Use tables for requirement ledgers, scoring maps, evidence matrices, and review findings.
- Use concise, evaluable language. Prefer "满足/优于/响应/提供" statements tied to measurable tender clauses.
- Flag `否决项`, missing evidence, impossible deadlines, contradictory clauses, and formatting constraints before polishing prose.
- Do not fabricate screenshots, certificates, project cases, authorized letters, seal/signature status, or third-party commitments.

## Typical User Prompts

- "Use $tender-bid-writer to analyze this tender package and produce the requirement ledger."
- "Use $tender-bid-writer to create a technical proposal outline and chapter briefs."
- "Use $tender-bid-writer to draft the implementation方案 and run a compliance review."
- "Use $tender-bid-writer to merge these chapters, simulate expert review, and create a final delivery checklist."
