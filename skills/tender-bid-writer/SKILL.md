---
name: tender-bid-writer
description: End-to-end tender and bid proposal workflow for Chinese government, enterprise, and integration projects. Use when Codex/OpenClaw/Hermes needs to analyze bidding documents; handle outsourced/commissioned bid-writing intake; classify the bid as goods-mode, software-platform-mode, hybrid-goods-software-mode, or service-mode; extract scoring criteria, qualification requirements, technical specifications, and business clauses; build a MECE proposal outline and chapter briefs; draft evaluator-ready, low-AI-flavor bid chapters with mode-appropriate thickness; merge and quality-check HTML/Markdown/DOCX outputs; simulate multi-expert bid review; iterate revisions; and prepare final delivery checklists for tender submissions.
---

# Tender Bid Writer

## Operating Rule

Treat the tender document as the source of truth. Do not invent qualifications, certifications, past projects, prices, delivery dates, or manufacturer commitments. In internal ledgers and review notes, mark unknowns as `待确认` and ask for evidence when a claim affects compliance or scoring. In formal proposal chapters, never leave draft placeholders or internal notes; cite other formal chapters or attachments for unprovided evidence instead of fabricating it.

## Workflow

1. **Intake and workspace setup**
   - Locate tender files, annexes, drawings, templates, clarification notices, and mandatory response forms.
   - Identify the procurement object, project value, procurement method, scoring method, required response forms, hard page/format limits, and evidence attachments before drafting.
   - If the task is an outsourced/commissioned bid-writing job, or the user has only received the tender package without bidder evidence materials, enter the outsourced pre-audit workflow before drafting.
   - Create a working structure if none exists:
     - `00_source/` original tender files and extracted text
     - `01_requirements/` scoring, qualifications, technical parameters, business clauses, deliverables, forms
     - `02_outline/` proposal outline and per-chapter briefs
     - `03_chapters/` chapter drafts, preferably HTML when diagrams are needed
     - `04_merge/` merged proposal
     - `05_qc/` quality checks and review records
     - `06_delivery/` final DOCX/PDF/HTML and delivery checklist
     - `07_client_feedback/` outsourced pre-audit reports, material request lists, client-facing questions, and evidence-receipt tracking

2. **Bid type mode classification**
   - Before extracting requirements or outlining, classify the bid into exactly one primary mode: `goods-mode`, `software-platform-mode`, `hybrid-goods-software-mode`, or `service-mode`.
   - Record the classification basis from tender language, procurement object, scoring items, deliverables, evidence requirements, and acceptance method.
   - If the project includes both product supply and non-trivial software/platform/service implementation, default to `hybrid-goods-software-mode` and split the response into tracks instead of mixing product parameters with platform方案.
   - Let the selected mode control requirement extraction, evidence matrices, outline structure, page budget, drafting density, table design, and QC rules.

3. **Outsourced pre-audit gate**
   - Use this gate when the bid is outsourced, commissioned, or started before bidder-specific evidence is available.
   - First audit the tender file and produce a client-facing pre-audit package, not a full proposal draft.
   - Required outputs:
     - Tender review report: project overview, bid type mode, procurement object, deadlines, hard compliance items, scoring structure, response format, and major risks.
     - Overall proposal framework: mode-appropriate table of contents, target page budget, chapter goals, and primary response locations.
     - Scoring-response map: every scoring item, score value, source clause, response chapter, evidence needed, current evidence status, and expected scoring risk.
     - Material request list: required documents, owner/client provider, purpose, matching scoring item or clause, matching proposal chapter, priority (`P0` mandatory/pass-fail, `P1` scoring-critical, `P2` polishing/supporting), required format, and deadline.
     - Question and clarification list: issues to ask the client or purchaser, including ambiguous clauses, missing annexes, evidence gaps, impossible commitments, and authorization/status risks.
     - Client feedback message: a concise external-facing summary that explains what is needed, why it is needed, which score or clause it supports, and what drafting risk remains if it is not provided.
   - Use `待客户提供` or `待外包方确认` only in internal tracking tables and client feedback lists. Do not place these markers in formal proposal chapters.
   - Stop after the pre-audit package if critical evidence is missing. Resume full drafting only after the client provides materials or explicitly accepts the risk.

4. **Requirement extraction**
   - Extract four requirement ledgers before drafting: scoring criteria, qualification requirements, technical specifications, and business clauses.
   - Decompose procurement requirements into three levels before outlining: Level 1 requirement domain or system boundary, Level 2 function/service/work item, and Level 3 minimum response unit with acceptance point, evidence, and primary proposal location.
   - Extract mode-specific ledgers:
     - `goods-mode`: parameter response, brand/model/specification, product evidence, deviation, authorization, warranty, delivery, installation, commissioning, training, and acceptance.
     - `software-platform-mode`: business understanding, system boundary, function module, architecture, data, interface, security, migration, implementation, demonstration, acceptance, and operations.
     - `hybrid-goods-software-mode`: product response track, software/platform方案 track, and integration delivery track.
     - `service-mode`: service scope, staffing, SLA/KPI, workflow, records, tools, escalation, transition, training, assessment, and acceptance.
   - Preserve exact source anchors where possible: file name, page, section, table row, or clause number.
   - Classify each requirement as `mandatory`, `scored`, `contractual`, `format`, or `evidence`.
   - Stop and report conflicts, missing annexes, unreadable scans, ambiguous scoring language, or hard pass/fail risks.

5. **Outline and chapter briefs**
   - Build a MECE outline that maps every scored and mandatory requirement to exactly one primary response location.
   - Write a brief for every chapter before drafting: bid type mode, chapter goal, source requirements, three-level procurement-demand mapping, claims allowed, evidence needed, diagrams/tables, and acceptance checks.
   - Create an overall page budget before drafting. Unless the tender document imposes a strict page limit, estimate the full proposal thickness by project value, scoring method, and selected mode. Use about 1 proposal page per RMB 10,000 as a practical baseline for software-platform and complex hybrid bids; apply goods-mode and service-mode adjustments from the mode rules.
   - Ask for human confirmation before full drafting when the outline controls compliance or a large document.

6. **Draft chapters**
   - Draft one chapter at a time from the approved brief.
   - Prefer HTML for long technical方案 chapters that need SVG architecture diagrams, flowcharts, tables, and later DOCX conversion.
   - Follow the selected mode. For high-budget, complex, or highly competitive software-platform and hybrid projects, draft chapters as thick proposal text rather than short generic summaries: combine正文,专项措施,表格化管理工具,交付记录, and验收支撑材料. For goods-mode, do not inflate chapters with generic software/platform solution prose.
   - For every minimum-level section or subsection that responds to a Level 3 procurement requirement, write at least 3-5 substantive正文 paragraphs unless the selected mode or tender response form justifies a shorter table/form response. Paragraphs should cover mechanism, project scenario, execution details, records/forms, risks, and acceptance outputs, not repeat the heading in different words.
   - For outsourced bids, re-check that the source material for each claim has been received, mapped, and accepted before turning it into formal正文. Unreceived evidence should remain in the material request list, not be converted into a definitive commitment.
   - After each chapter, run a local self-check: requirement coverage, forbidden placeholders, evidence gaps, consistency with prior chapters, evaluator readability, low-AI-flavor detail, and验收可追溯性.

7. **Merge and quality check**
   - Merge chapters only after chapter-level checks pass.
   - Run deterministic checks with `scripts/bid_quality_check.py` when files are available.
   - Produce a QC report listing blockers, warnings, traceability gaps, mode-mismatch risks, and recommended fixes.

8. **Expert review simulation**
   - Review from at least five perspectives when the bid is substantial: compliance officer, technical architect, scoring evaluator, delivery/operations lead, and commercial/legal reviewer.
   - Add a product/evidence reviewer for `goods-mode`; add an integration reviewer for `hybrid-goods-software-mode`; add a service delivery/SLA reviewer for `service-mode`.
   - Score against the tender scoring rubric when available.
   - Convert review comments into a revision plan with owner, target chapter, evidence needed, and expected scoring impact.

9. **Iterate to final**
   - Repeat review and revision until the user accepts the risk level or the score target is reached.
   - Prepare a delivery checklist: final files, response forms, evidence attachments, unresolved confirmations, signature/seal items, and submission format.

## Resource Loading

- Read `references/workflow.md` for the detailed article-inspired process, output files, and stage gates.
- Read `references/checklists.md` when extracting requirements, writing briefs, or running expert review.
- Read `references/platform-compatibility.md` when installing or adapting this skill for Codex, OpenClaw, or Hermes.
- Use `scripts/bid_quality_check.py` for local proposal checks when draft files exist.

## Bid Type Modes

Always classify the bid before outlining. The mode is a control variable, not a label for display.

| Mode | Use when | Core materials | Writing thickness |
| --- | --- | --- | --- |
| `goods-mode` | The object is equipment, hardware, standard products, finished software, consumables, instruments, or other off-the-shelf goods. | Product brochure, model/spec sheet, test report, manufacturer authorization, certificate, parameter response table, deviation table, warranty, delivery/installation plan. | Most fixed. Prioritize parameters, evidence, traceability, deviation control, delivery, installation, warranty, and acceptance. Do not create bloated generic方案 chapters. |
| `software-platform-mode` | The object is custom development, system integration, data middle platform, business platform, AI capability center, operations platform, or software-intensive service. | Requirement analysis, architecture, function design, business flow, data/interface/security, implementation, migration, testing, demonstration, acceptance, operations. | Thickest. Expand by function, scenario, data object, interface, workflow, risk, record, and acceptance mapping. |
| `hybrid-goods-software-mode` | The object combines hardware/standard products with platform development, system integration, deployment, operations, or service delivery. | Product parameter evidence plus software/platform方案 plus integrated deployment, joint debugging, test, training, trial-run, and acceptance records. | Split into tracks. Keep product response, software方案, and integration delivery separately traceable. |
| `service-mode` | The object is operations, maintenance, consulting, planning, training, assessment, data governance, testing, supervision, or other human/process/service-heavy work without major product supply or platform development. | Service scope, staffing, role matrix, SLA/KPI, workflow, tools, records, escalation, reports, training, transition, assessment, and acceptance. | Medium to thick depending on SLA and scoring. Focus on people, process, records, KPI, risk, and acceptance rather than product parameters or software architecture. |

Mode rules:

- For `goods-mode`, build the proposal around `参数响应表 + 产品证据矩阵 + 偏离表 + 厂家/材料追溯 + 供货安装调试方案 + 售后质保方案 + 验收交付清单`.正文 should support evidence and履约, not replace parameter proof. A thin but complete parameter/evidence response is better than a long generic architecture chapter.
- For `software-platform-mode`, use the thick proposal rules aggressively. Every important function should explain business scenario, user role, process, data object, interface relation, permission/security, exception handling, testing, demonstration point, delivery artifact, and acceptance mapping.
- For `hybrid-goods-software-mode`, create three parallel ledgers and outlines: product response track, software/platform方案 track, and integration delivery track. Add a responsibility matrix that connects equipment installation, software deployment, interface joint debugging, system test, training, trial run, and final acceptance.
- For `service-mode`, write around service outcomes: service catalog, staffing model, shift/response mechanism, SLA/KPI, tools and records, issue escalation, report rhythm, assessment method, knowledge transfer, continuity, and acceptance. Do not force service bids into product parameter tables or software architecture chapters.
- If tender language conflicts with mode assumptions, obey the tender. A fixed response table, page cap, or mandatory format overrides thickness defaults.
- If the project looks like工程施工 or pure construction, report that the skill can support requirement extraction and review, but施工组织设计,工程量清单,安全文明施工, and construction-specific scheduling may require a separate construction-bid workflow.

## Outsourced Bid Intake Workflow

Use this workflow when someone asks the user to write a bid for them, when the bidder's company materials are not yet provided, or when the user needs to report back to the client before drafting.

The goal is to convert the tender into an actionable client feedback package:

- **Can we bid?** Identify hard compliance risks, qualification gaps, deadline risks, format risks, and evidence blockers.
- **How should the bid be structured?** Produce a mode-aware proposal framework and page budget.
- **What do we need from the client?** Produce a material request list that ties every requested item to a tender clause, scoring item, response chapter, and risk level.
- **How does each score get answered?** Produce a scoring-response map that shows the path from scoring language to proposal content and evidence.
- **What can be drafted now?** Separate reusable/general sections from evidence-dependent sections, and do not turn missing materials into formal claims.

Required tables for outsourced intake:

| Table | Required columns |
| --- | --- |
| Tender audit summary | Item, tender source, finding, risk level, action needed, owner |
| Scoring-response map | Score item, points, source clause, response strategy, target chapter, evidence required, evidence status, risk if missing |
| Material request list | Material, provider, purpose, source clause/score item, target chapter, priority, format, deadline, notes |
| Proposal framework | Chapter, purpose, mapped requirements, target pages, evidence dependencies, drafting status |
| Client question list | Question, reason, affected score/clause, decision needed, deadline |
| Evidence receipt tracker | Material, received status, file/location, quality check, usable claims, remaining gap |

Priority rules:

- `P0`: pass/fail, qualification, mandatory form, authorization, signature/seal, or hard compliance evidence. Do not proceed as if satisfied without evidence.
- `P1`: scoring-critical evidence or content that materially affects ranking.
- `P2`: supporting, polishing, or credibility-enhancing material.

When material returns from the client:

- Check each file against the material request list.
- Mark whether it is usable, incomplete, expired, inconsistent, or unrelated.
- Update the scoring-response map and chapter briefs before drafting.
- Ask follow-up questions for gaps instead of inventing claims.

## Thick Proposal Drafting Rules

Use these rules whenever drafting formal bid chapters, especially for software-platform or complex hybrid projects above RMB 30 million, multi-system platform projects, substantial service projects, or scoring language such as `完全满足且优于项目需求`. Adjust thickness by bid type mode.

- Map the tender source into the正文. Connect scoring items, procurement needs, technical parameters, business clauses, deliverables, and acceptance requirements to specific response content. Avoid abstract promises such as "建立机制" or "加强管理" unless the text states how the mechanism runs, who is responsible, when it is executed, what records are formed, and how those records support acceptance.
- Break procurement-demand content into a stable three-level hierarchy. Level 1 should identify the requirement domain, platform, service area, or management theme; Level 2 should identify the concrete function, service task, control object, or deliverable group; Level 3 should identify the smallest response unit that can be written, checked, evidenced, and accepted. Use Level 3 items as the minimum units for正文 drafting, tables, and acceptance mapping.
- Match length and density to project complexity and selected mode. Do not leave major software-platform, service, or hybrid方案 chapters at a 5,000-10,000 character overview level when the full bid target is a thick technical volume. Expand with专项控制内容,流程细则,检查表,台账模板,风险预防措施,阶段门禁,交付记录, and验收映射表.
- Keep minimum sections substantial. Each smallest formal正文 section should normally contain at least 3-5 paragraphs with real content; use fewer for goods-mode parameter responses, fixed forms, compliance statements, or tender-mandated short responses. Do not use a single paragraph or a thin table as a substitute for a response that evaluators must score.
- Plan the full proposal by page count, not only by section list. If the tender has no hard page cap, use `RMB 10,000 contract value ≈ 1 proposal page` as the baseline for software-platform and complex hybrid bids, then adjust upward for complex systems, many scoring items, integration difficulty, data migration, demonstrations, or heavy acceptance obligations. For substantial software-platform and complex hybrid projects, the technical/business proposal should generally not fall below 300-500 pages; for goods-mode, page count is driven by parameter/evidence completeness rather than long prose; for service-mode, scale by SLA complexity, staffing, records, and assessment requirements.
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
- Verify the selected bid type mode is still correct after reading the full tender, and flag mode mismatch risks such as a goods bid inflated with platform prose or a platform bid reduced to a product parameter table.
- Verify procurement requirements are decomposed to three levels and every Level 3 item has a primary response location, evidence/record expectation, and acceptance linkage.
- Identify unsupported claims and either remove them, tie them to evidence, or reference the formal attachment/chapter where evidence is provided.
- Remove draft traces, placeholders, internal review wording, and fabricated evidence.
- Check that the chapter fits this project rather than a generic template, including business scenes, platform boundaries, data/interface/control details, and purchaser collaboration.
- Check that each minimum-level formal正文 section has at least 3-5 substantive paragraphs unless `goods-mode`, a tender form, or a fixed response table justifies shorter treatment.
- Confirm every major commitment has a verifiable output: ledger, checklist, meeting minutes, test report, trial-run record, migration record, issue record, acceptance mapping, or delivery document.
- Check consistency with other chapters for scope, schedule, roles, deliverables, service commitments, and acceptance criteria.
- Judge whether the length and density match the project amount, complexity, scoring competitiveness, page-budget baseline, and target thickness of the full bid.

## Typical User Prompts

- "Use $tender-bid-writer to analyze this tender package and produce the requirement ledger."
- "Use $tender-bid-writer to create a technical proposal outline and chapter briefs."
- "Use $tender-bid-writer to draft the implementation方案 and run a compliance review."
- "Use $tender-bid-writer to merge these chapters, simulate expert review, and create a final delivery checklist."
