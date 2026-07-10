# Human Bid Prose Style

Use this reference when drafting or revising formal technical proposal chapters, especially when the output sounds like AI, template prose, or流水账. The goal is not to make the text casual; it is to make it read like a bid chapter jointly revised by a project manager, technical lead, quality lead, and delivery lead.

## Main Symptoms To Remove

Avoid repeated chapter openings and filler phrases such as:

- `本节围绕……展开响应`, `本章节将从……方面进行阐述`, `围绕……进行说明`.
- `全过程`, `全链路`, `全角色`, `全闭环`, `全维度`, `全场景` when they are used as slogans.
- `建立健全机制`, `持续优化能力`, `切实保障`, `有效提升`, `全面推进`, `不断完善`, `充分发挥`.
- Paragraphs that repeat the heading, then add `一是、二是、三是` without project-specific work, owner, record, or acceptance output.
- Tables that only list abstract measures and cannot be used by an evaluator, purchaser, or project team.

These phrases may appear occasionally when the tender itself uses them, but they must not carry the chapter. If a paragraph still works after deleting all project nouns, it is probably too generic.

## Required Paragraph Shape

For formal response正文, write most paragraphs in this practical order:

1. **Tender requirement or project scene**: identify the exact procurement object, service boundary, platform module, delivery link, inspection point, or scoring expectation.
2. **Our execution method**: state what the bidder will actually do, in what stage, with what role or team.
3. **Record or evidence**: name the form, ledger, meeting minutes, test record, delivery receipt, sign-off sheet, issue ticket, inspection report, or acceptance material.
4. **Acceptance or scoring value**: explain how the work supports review, implementation, delivery, contract performance, or final acceptance.

Do not begin every section by explaining "what this chapter will discuss." Start with the purchaser's requirement or the operational scene.

## Before / After Pattern

Weak:

`本节围绕供货服务保障展开响应，通过全过程管理、全链路协同和闭环控制，切实提升服务质量。`

Better:

`采购文件要求中标供应商按采购人实际用餐安排完成主副食品配送。我方将把每日订单确认、备货复核、装车检查、到货验收和异常退换货作为五个固定控制点，由项目负责人统一调度，仓储分拣员、配送司机和现场对接人分别在《配送任务单》《装车复核表》《到货签收单》《异常处置记录》中签字留痕。上述记录随月度结算资料一并归档，用于证明配送时效、数量一致性和质量问题处理结果。`

## Bid-Type Language Anchors

Use nouns and evidence that fit the bid type:

- **Food / ingredient distribution**:订单、备货、分拣、装车、冷链、车辆消杀、健康证、供应商台账、进货查验、检测报告、检疫证明、标签保质期、签收单、退换货记录、临时加送、应急补货、月度结算.
- **Standard goods**:品牌型号、规格参数、彩页、检测报告、合格证、厂家授权、到货验收、安装调试、培训签到、质保单、备品备件、偏离表.
- **Software / platform**:业务角色、功能边界、数据对象、主数据、接口报文、权限策略、联调环境、迁移批次、测试用例、缺陷单、演示脚本、上线回退、验收用例.
- **Service / operations**:服务台、工单、值班表、SLA、巡检记录、日报周报月报、问题升级、知识库、培训签到、考核表、满意度、交接清单.
- **Hybrid projects**:设备到货、软件部署、网络配置、接口联调、系统测试、培训、试运行、最终验收, with a responsibility matrix connecting both tracks.

## Rewrite Rules

- Replace slogans with the concrete control point. `闭环管理` becomes `问题登记、责任分派、整改复核、结果归档`.
- Replace broad claims with owner and stage. `加强沟通` becomes `项目经理每周组织采购人、仓储负责人、配送负责人召开履约例会，并形成会议纪要`.
- Replace "will improve" with an acceptance output. `提升质量` becomes `形成《质量问题整改台账》，整改完成后由采购人现场确认`.
- Keep some natural variation in paragraph length. Formal bid prose can be long, but every paragraph should carry a distinct job.
- When a chapter has many subsections, do not use the same opening sentence pattern repeatedly. Vary between requirement-based, scene-based, risk-based, and record-based openings.
- Preserve evaluator-friendly tables, but introduce each table with what decision or score it supports.

## Chapter Rewrite Pass

After drafting each formal chapter, run a human-prose pass:

1. Highlight repeated section openings and replace at least 70% of them with requirement/scene openings.
2. Count slogan phrases. If a slogan appears more than twice in a chapter, rewrite most occurrences into concrete process language.
3. For every 3-5 paragraphs, ensure at least one named role, one named record/form, and one acceptance or scoring link appear.
4. Check whether a real project manager could execute the text. If not, add stage, owner, record, and acceptance material.
5. Remove statements that sound impressive but cannot be evidenced, inspected, signed, uploaded, or accepted.
