# Tender Bid Workflow

This workflow is inspired by the article "投标skill 2.0实战图解" by 然之, which demonstrates an AI-assisted bid process: install a bid skill, extract requirements, generate a MECE outline and chapter briefs, require human confirmation, draft chapter-by-chapter in HTML, merge, QC, run multi-expert review, iterate revisions, and convert final HTML to DOCX.

## Stage Gates

Do not skip these gates on real bids:

1. **Source completeness gate**
   - Confirm all tender files, annexes, drawings, clarification notices, templates, response forms, and submission rules are present.
   - Record missing or unreadable materials before extraction.

2. **Requirement extraction gate**
   - Produce ledgers for scoring, qualification, technical, business, format, and evidence requirements.
   - Identify pass/fail clauses, hard deadlines, mandatory forms, seal/signature rules, and disqualification risks.
   - Ask the user to confirm high-risk interpretation before drafting.

3. **Outline/brief gate**
   - Create a MECE chapter outline.
   - Map each scored and mandatory requirement to a chapter, section, evidence item, or attachment.
   - Write per-chapter briefs. Do not start large-scale drafting until the outline and briefs are accepted.

4. **Chapter drafting gate**
   - Draft one chapter per file under `03_chapters/`.
   - Use HTML when the chapter benefits from SVG diagrams, architecture maps, timelines, workflow figures, or complex tables.
   - End each chapter with a self-check summary: covered requirements, assumptions, evidence gaps, and recommended follow-up.

5. **Merge/QC gate**
   - Merge only checked chapters.
   - Run script-level checks when files exist.
   - Manually verify the highest-risk items: scoring criteria, qualifications, non-deviation clauses, and required forms.

6. **Expert review gate**
   - Simulate five reviewers:
     - Compliance officer: pass/fail, format, submission, qualification.
     - Technical architect: architecture, feasibility, parameter response, implementation depth.
     - Scoring evaluator: scoring point coverage, persuasive strength, differentiators.
     - Delivery/operations lead: schedule, staffing, risks, acceptance, after-sales.
     - Commercial/legal reviewer: contract clauses, commitments, warranty, liability, payment, IP/confidentiality.
   - Score with the tender rubric when available.
   - Convert comments into a revision plan.

7. **Delivery gate**
   - Prepare final DOCX/PDF/HTML as requested by the user and tender rules.
   - Prepare an attachment checklist, seal/signature checklist, unresolved-risk list, and final file manifest.

## Recommended Workspace Files

Use these names unless the user or project already has conventions:

- `01_requirements/scoring_criteria.md`
- `01_requirements/qualification_requirements.md`
- `01_requirements/technical_specifications.md`
- `01_requirements/business_clauses.md`
- `01_requirements/evidence_matrix.md`
- `02_outline/proposal_outline.md`
- `02_outline/chapter_briefs.md`
- `03_chapters/chapter_XX_<name>.html`
- `04_merge/final_proposal.html`
- `05_qc/qc_report.md`
- `05_qc/expert_review_round_N.md`
- `06_delivery/delivery_checklist.md`

## Drafting Style

- Lead with direct compliance language, then explain method and evidence.
- Tie each important paragraph to a tender requirement or scoring point.
- Use tables for parameter response, staffing, schedule, risk controls, service commitments, and evidence.
- Use diagrams only when they clarify architecture, process, organization, data flow, deployment, or schedule.
- Keep every unverified claim visibly marked until evidence is supplied.

## Human Confirmation Points

Request explicit confirmation when:

- The outline/brief mapping will determine the whole proposal structure.
- The agent must choose between conflicting interpretations.
- A requirement appears impossible, risky, or dependent on missing evidence.
- A claim would require a certificate, authorization, case study, price, staffing commitment, or legal representation.
- Final files are ready for conversion or submission packaging.
