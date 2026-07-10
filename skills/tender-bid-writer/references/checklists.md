# Bid Checklists

## Requirement Ledger Template

Use this table shape for extracted requirements:

| ID | Source | Clause | Type | Requirement | Risk | Response Location | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | file/page/section | clause number | mandatory/scored/contractual/format/evidence | exact or concise paraphrase | blocker/high/medium/low | chapter/section/form | certificate/case/letter/data | open/covered/待确认 |

## Extraction Checklist

- Scoring method and point allocation
- Pass/fail clauses and disqualification items
- Vendor qualification, certificates, licenses, authorizations
- Product or service technical parameters
- Functional requirements and acceptance criteria
- Implementation schedule, milestones, staffing, delivery location
- After-sales, training, warranty, SLA, maintenance
- Security, data, privacy, localization, integration, compatibility
- Contract deviations, payment, penalties, IP, confidentiality
- Required response forms, seals, signatures, copies, file formats
- Submission mode: `electronic-bid`, `paper-bid`, or `dual-bid`
- Outsourced first-round deliverables: `资料清单（项目名称）.docx` for the client and `标书组织说明（项目名称）.md` for the writer
- Electronic bid details: platform account, CA/digital certificate, electronic seal/signature authority, upload operator, file format/size, encryption, decryption, online sign-in/opening contact, upload deadline
- Paper bid details: handwritten signature, company seal, page/cross-page seal, original/copy quantities, binding, envelope label/seal, delivery address/person/deadline
- Tender-native Word/DOCX forms that must be reproduced as Word tables in the client material collection package
- Clarification deadlines, bid opening time, submission channel

## Chapter Brief Template

Use this before drafting a chapter:

| Field | Content |
| --- | --- |
| Chapter | number and title |
| Goal | what the evaluator should believe after reading |
| Source requirements | requirement IDs and tender anchors |
| Scoring intent | points this chapter should win |
| Claims allowed | only claims supported by tender text or user evidence |
| Evidence needed | certificates, cases, screenshots, staffing, diagrams, tables |
| Structure | section outline |
| Must avoid | unsupported promises, contradictions, forbidden deviations |
| Acceptance checks | coverage, clarity, formatting, evidence, risk |

## Quality Checklist

Blocker checks:

- Missing response to a mandatory or scored requirement
- Unsupported qualification, certificate, case, authorization, staffing, or product claim
- Tender deadline, submission format, seal/signature, or form requirement omitted
- Current response file review misses blank quotation, blank mandatory form fields, unfilled dates, missing contact/bank/person fields, unresolved authorization identity, absent signature/seal, or unclear uploaded scan risks
- Embedded certificate, screenshot, contract, ID, deposit voucher, or license treated as compliant without checking clarity, orientation, entity consistency, expiry, and completeness
- Outsourced first-round output scattered into many client-facing files instead of the required Word material list plus internal Markdown organization file
- Client-facing Word document exposes internal-only notes, unsupported claims, or writer-control placeholders
- Electronic bid treated like a paper bid, or paper bid treated like an electronic-only upload
- Official Word/DOCX response tables flattened into generic checklists when the client must fill tender-native forms
- Contradiction between chapters or with tender clauses
- Placeholder text such as `TODO`, `待补充`, `公司名称`, `项目名称`, or template-only language
- Scope, price, schedule, warranty, or legal commitment invented by the agent

Warning checks:

- Repeated generic prose without evaluator-specific value
- Repeated AI-like openings such as `本节围绕`, `本章节将从`, or `围绕……展开响应`
- Slogan-heavy expressions such as `全过程`, `全链路`, `全角色`, `全闭环`, `建立健全机制`, or `切实保障` that are not converted into owner, stage, record, and acceptance output
- Paragraphs that do not name any project scene, role, record/form, issue handling path, or acceptance material
- Long sections that do not map to scoring criteria
- Weak evidence matrix or missing attachment reference
- Unclear ownership, timeline, acceptance method, or risk control
- Diagram or table lacks direct connection to requirements

## Expert Review Scorecard

Use a 0-5 score for each reviewer dimension:

| Reviewer | Main Question | Score | Findings | Revision Target |
| --- | --- | --- | --- | --- |
| Compliance officer | Can this pass formal and qualification review? | 0-5 | blockers/warnings | clause/chapter |
| Technical architect | Is the technical solution feasible and responsive? | 0-5 | gaps/risks | chapter/diagram |
| Scoring evaluator | Does it maximize rubric points? | 0-5 | weak points | scoring item |
| Delivery lead | Can the team deliver and operate it? | 0-5 | staffing/schedule/service | chapter/table |
| Commercial/legal reviewer | Are commitments controlled and contract-safe? | 0-5 | legal/business risks | clause/appendix |

After review, output:

1. Overall score and pass/fail risk.
2. Top blockers.
3. Highest-score-impact revisions.
4. Evidence needed from the user.
5. Recommendation: continue drafting, revise, or stop for user confirmation.
