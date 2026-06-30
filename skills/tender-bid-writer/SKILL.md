---
name: tender-bid-writer
description: End-to-end tender and bid proposal workflow for Chinese government, enterprise, and integration projects. Use when Codex/OpenClaw/Hermes needs to analyze bidding documents, extract scoring criteria, qualification requirements, technical specifications, and business clauses; build a MECE proposal outline and chapter briefs; draft thick, evaluator-ready, low-AI-flavor technical or service proposal chapters; merge and quality-check HTML/Markdown/DOCX outputs; simulate multi-expert bid review; iterate revisions; and prepare final delivery checklists for tender submissions.
---

# Tender Bid Writer

## Operating Rule

Treat the tender document as the source of truth. Do not invent qualifications, certifications, past projects, prices, delivery dates, or manufacturer commitments. In internal ledgers and review notes, mark unknowns as `待确认` and ask for evidence when a claim affects compliance or scoring. In formal proposal chapters, never leave draft placeholders or internal notes; cite other formal chapters or attachments for unprovided evidence instead of fabricating it.

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
   - Decompose procurement requirements into three levels before outlining: Level 1 requirement domain or system boundary, Level 2 function/service/work item, and Level 3 minimum response unit with acceptance point, evidence, and primary proposal location.
   - Preserve exact source anchors where possible: file name, page, section, table row, or clause number.
   - Classify each requirement as `mandatory`, `scored`, `contractual`, `format`, or `evidence`.
   - Stop and report conflicts, missing annexes, unreadable scans, ambiguous scoring language, or hard pass/fail risks.

3. **Outline and chapter briefs**
   - Build a MECE outline that maps every scored and mandatory requirement to exactly one primary response location.
   - Write a brief for every chapter before drafting: chapter goal, source requirements, three-level procurement-demand mapping, claims allowed, evidence needed, diagrams/tables, and acceptance checks.
   - Create an overall page budget before drafting. Unless the tender document imposes a strict page limit, estimate the full proposal thickness by project value and complexity, using about 1 proposal page per RMB 10,000 as the practical planning baseline and keeping substantial bids no lower than roughly 300-500 pages.
   - Ask for human confirmation before full drafting when the outline controls compliance or a large document.

4. **Draft chapters**
   - Draft one chapter at a time from the approved brief.
   - Prefer HTML for long technical方案 chapters that need SVG architecture diagrams, flowcharts, tables, and later DOCX conversion.
   - For high-budget, complex, or highly competitive projects, draft chapters as thick proposal text rather than short generic summaries: combine正文,专项措施,表格化管理工具,交付记录, and验收支撑材料.
   - For every minimum-level section or subsection that responds to a Level 3 procurement requirement, write at least 3-5 substantive正文 paragraphs unless the tender response form forces a shorter answer. Paragraphs should cover mechanism, project scenario, execution details, records/forms, risks, and acceptance outputs, not repeat the heading in different words.
   - After each chapter, run a local self-check: requirement coverage, forbidden placeholders, evidence gaps, consistency with prior chapters, evaluator readability, low-AI-flavor detail, and验收可追溯性.

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

## Thick Proposal Drafting Rules

Use these rules whenever drafting formal bid chapters, especially for projects above RMB 30 million, multi-system platform projects, or scoring language such as `完全满足且优于项目需求`.

- Map the tender source into the正文. Connect scoring items, procurement needs, technical parameters, business clauses, deliverables, and acceptance requirements to specific response content. Avoid abstract promises such as "建立机制" or "加强管理" unless the text states how the mechanism runs, who is responsible, when it is executed, what records are formed, and how those records support acceptance.
- Break procurement-demand content into a stable three-level hierarchy. Level 1 should identify the requirement domain, platform, service area, or management theme; Level 2 should identify the concrete function, service task, control object, or deliverable group; Level 3 should identify the smallest response unit that can be written, checked, evidenced, and accepted. Use Level 3 items as the minimum units for正文 drafting, tables, and acceptance mapping.
- Match length and density to project complexity. Do not leave major chapters at a 5,000-10,000 character overview level when the full bid target is a thick technical volume. Expand with专项控制内容,流程细则,检查表,台账模板,风险预防措施,阶段门禁,交付记录, and验收映射表.
- Keep minimum sections substantial. Each smallest formal正文 section should normally contain at least 3-5 paragraphs with real content; use fewer only for fixed forms, compliance statements, or tender-mandated short responses. Do not use a single paragraph or a thin table as a substitute for a response that evaluators must score.
- Plan the full proposal by page count, not only by section list. If the tender has no hard page cap, use `RMB 10,000 contract value ≈ 1 proposal page` as the baseline, then adjust upward for complex systems, many scoring items, integration difficulty, data migration, demonstrations, or heavy acceptance obligations. For substantial projects, the technical/business proposal should generally not fall below 300-500 pages; prefer greater detail when it improves evaluability, traceability, and acceptance support.
- Reduce AI flavor. Avoid repeated slogan-like symmetric phrases such as "全过程、全链路、全角色、全闭环". Use concrete project scenes, business objects, data flows, interface joint debugging, role collaboration, quality records, issue handling, acceptance materials, and procurement-side coordination details.
- Prefer the structure `机制 + 场景 + 表单 + 输出成果`:
  - 机制: explain the management method and responsible role.
  - 场景: explain how it applies to this project's business or technical boundary.
  - 表单: identify the ledger, checklist, meeting minutes, test record, migration record, or acceptance mapping used to freeze the process.
  - 输出成果: state the material that supports evaluation, implementation, delivery, and acceptance.
- For project-understanding chapters, avoid broad policy boilerplate. Build a thick, evaluator-ready narrative from `政策背景 -> 采购人定位 -> 项目建设目标 -> 业务现状理解 -> 信息化现状判断 -> 痛点归纳 -> 建设必要性 -> 价值链/业务链分析 -> response strategy`. Use tender language first, then carefully infer business implications; do not invent purchaser internal data.
- For platform software projects, write project-specific专项方案 instead of generic software engineering. Cover relevant boundaries such as生产服务平台,流通服务平台,交易服务平台,数据中台,AI能力中心,电子合同,质量追溯,接口联调,数据迁移,主数据管理,业务连续性,演示功能. For each专项, state quality risks, control focus, inspection method, and output results.
- Make tables evaluative, not decorative. Use tables only when they support scoring or implementation control, such as质量指标表,阶段门禁表,岗位职责表,问题分级表,接口联调检查表,数据质量检查表,风险预防表,交付文档清单,验收映射表. Each table should help prove `完全满足且优于项目需求`.
- For scoring chapters, first read the target score and scoring language. When the evaluator expects `优于`, provide evidence through finer process control, fuller risk prevention, clearer acceptance linkage, and stronger专项措施 rather than restating the tender text.
- For common chapters such as质量管理,组织实施,验收交付, and运维服务, adapt them to the project. For example, a quality management chapter should include quality goals, indicators, responsibilities, issue handling, evaluation, rectification, incentives/penalties, lifecycle quality gates, platform-specific quality controls, data middle-platform quality controls, interface joint-debugging controls, data quality controls, trial-run controls, quality meetings, process forms, risk prevention, document consistency controls, purchaser collaboration, and acceptance tracking.
- Do not leave formal-chapter draft traces: `本章自查`, `待确认`, `TODO`, `公司名称`, `项目名称：填写`, `如有证据再补`, or similar wording. For unavailable personnel, certificates, performance cases, software copyrights, authorizations, or manufacturer evidence, reference formal bid sections or attachments, such as `详见本投标文件《项目组织实施方案》及《本项目管理人员及服务人员名单》`.

## Output Standards

- Keep every key claim traceable to tender text, user-provided company evidence, or a clear assumption.
- Use tables for requirement ledgers, scoring maps, evidence matrices, and review findings.
- Use concise, evaluable language. Prefer "满足/优于/响应/提供" statements tied to measurable tender clauses.
- Flag `否决项`, missing evidence, impossible deadlines, contradictory clauses, and formatting constraints before polishing prose.
- Do not fabricate screenshots, certificates, project cases, authorized letters, seal/signature status, or third-party commitments.

## Chapter-Level Review

After each formal chapter, review and revise before moving on:

- Verify coverage of the matching scoring items, mandatory clauses, procurement requirements, technical parameters, business clauses, deliverables, and acceptance requirements.
- Verify procurement requirements are decomposed to three levels and every Level 3 item has a primary response location, evidence/record expectation, and acceptance linkage.
- Identify unsupported claims and either remove them, tie them to evidence, or reference the formal attachment/chapter where evidence is provided.
- Remove draft traces, placeholders, internal review wording, and fabricated evidence.
- Check that the chapter fits this project rather than a generic template, including business scenes, platform boundaries, data/interface/control details, and purchaser collaboration.
- Check that each minimum-level formal正文 section has at least 3-5 substantive paragraphs unless a tender form or fixed response table justifies shorter treatment.
- Confirm every major commitment has a verifiable output: ledger, checklist, meeting minutes, test report, trial-run record, migration record, issue record, acceptance mapping, or delivery document.
- Check consistency with other chapters for scope, schedule, roles, deliverables, service commitments, and acceptance criteria.
- Judge whether the length and density match the project amount, complexity, scoring competitiveness, page-budget baseline, and target thickness of the full bid.

## Typical User Prompts

- "Use $tender-bid-writer to analyze this tender package and produce the requirement ledger."
- "Use $tender-bid-writer to create a technical proposal outline and chapter briefs."
- "Use $tender-bid-writer to draft the implementation方案 and run a compliance review."
- "Use $tender-bid-writer to merge these chapters, simulate expert review, and create a final delivery checklist."
