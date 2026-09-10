# Bid Checklists

## Disqualification (Veto) Checklist

Run this first. Any unchecked box is a stop-and-confirm with the user before more drafting:

- [ ] 投标人资格条件(营业执照、资质等级、财务、社保、税收)全部满足
- [ ] 招标文件标注"★""必须""不得负偏离"的条款逐条响应且无负偏离
- [ ] 投标有效期、保证金/保函金额与提交方式符合要求
- [ ] 报价不超过最高限价,报价唯一且大小写一致,无算术错误风险
- [ ] 工期、质保期、付款条件不劣于招标要求
- [ ] 必须的证书、授权、检测报告原件/复印件要求已核对(正本/副本、加盖公章)
- [ ] 签字盖章位置清单已建立(逐页小签/骑缝章/法定代表人签字/授权委托书)
- [ ] 电子标:CA 证书、文件格式、大小限制、上传截止时间、加密解密要求已确认
- [ ] 联合体协议、分包限制(如招标允许)已落实
- [ ] 无串通投标风险表述(相同 IP/MAC、相同编制工具码等电子标雷区)

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
| Target length | chapter page budget from the worksheet below |
| Must avoid | unsupported promises, contradictions, forbidden deviations |
| Acceptance checks | coverage, clarity, formatting, evidence, risk |

## Page Budget Worksheet

Before outlining, fill one row per major part. Baseline `1 万元合同额 ≈ 1 页` applies to software-platform and complex hybrid bids when the tender sets no page cap; goods-mode thickness comes from parameter/evidence completeness, service-mode from SLA/staffing/records complexity.

| Part | 章节组 | 目标页数 | 主要三级需求来源 | 核心表格 | 证据依赖 |
| --- | --- | --- | --- | --- | --- |
| 1 | 项目理解与总体设计 | — | 一级需求域 | 架构图、需求映射表 | 招标文件 |
| 2 | 功能/技术方案 | — | 二三级功能需求 | 功能清单、接口清单 | 演示脚本 |
| 3 | 实施/交付/集成 | — | 商务条款、工期 | 责任矩阵、进度表 | — |
| 4 | 服务/运维/培训 | — | SLA、考核 | SLA表、人员表 | 人员证据 |
| 5 | 质量与风险管理 | — | 管理要求 | 风险登记表、门禁表 | — |
| 合计 | — | — | — | — | — |

Rules:

- Tender page cap or fixed response forms override the baseline; obey the tender first.
- Allocate pages by scoring weight, not evenly: a 10-point section deserves roughly double the pages of a 5-point section in the same part.
- Record the budget in each chapter brief and verify with `bid_quality_check.py --target-pages`.

## Quality Checklist

Blocker checks:

- Missing response to a mandatory or scored requirement
- Unsupported qualification, certificate, case, authorization, staffing, or product claim
- Tender deadline, submission format, seal/signature, or form requirement omitted
- Contradiction between chapters or with tender clauses
- Placeholder text such as `TODO`, `待补充`, `公司名称`, `项目名称`, or template-only language
- Scope, price, schedule, warranty, or legal commitment invented by the agent

Warning checks:

- Repeated generic prose without evaluator-specific value
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

## Final Delivery Checklist

Prepare this at the delivery gate, one line per item with `done / 待确认 / N.A.` status:

| Category | Items | Status |
| --- | --- | --- |
| 文件完整性 | 正本/副本/电子标份数;PDF 与 Word 版本一致;目录页码与正文对应 | 待确认 |
| 签字盖章 | 法定代表人签字、授权委托书、逐页小签、骑缝章位置清单 | 待确认 |
| 证书授权 | 营业执照、资质证书、厂家授权、检测报告:原件/复印件/公证要求 | 待确认 |
| 报价文件 | 开标一览表、分项报价表、大小写一致;报价与商务章节口径一致 | 待确认 |
| 响应表格 | 招标要求的固定格式表逐份放入且未改动表头 | 待确认 |
| 格式合规 | 字号、行距、页数上限、双面打印、装订、颜色要求 | 待确认 |
| 电子标 | CA 加密、文件命名、上传时间、备份渠道(如 U 盘/邮件) | 待确认 |
| 未决事项 | 所有内部台账中 `待确认` 项已清零或形成开标前行动清单 | 待确认 |

Rules:

- The checklist itself is an internal working file (kept in `06_delivery/`); strip internal wording before anything is packaged into the bid.
- Any item still `待确认` on submission day must be escalated to the user in writing.
