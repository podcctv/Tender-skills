# OpenBidKit-derived bid controls

本文件把公开项目 OpenBidKit_Yibiao 中与标书生产流程有关、且适合移植到本 skill 的机制整理为可执行规则。它不是对该项目的完整复刻，也不改变招标文件优先原则。

参考来源：

- 项目说明与能力边界：[FB208/OpenBidKit_Yibiao](https://github.com/FB208/OpenBidKit_Yibiao)
- 需求分析任务编排：`client/src/features/technical-plan/services/bidAnalysisWorkflow.ts`
- 技术方案状态与来源类型：`client/src/features/technical-plan/types.ts`
- 三轮废标/否决风险检查：`client/src/shared/prompts/rejectionPrompts.ts`
- 知识库与证据块：`client/src/features/knowledge-base/types.ts`、`knowledgeBaseService.cjs`
- 版式预设：`client/src/features/export-format/exportFormatPresets.ts`

## 1. 采用、改造与拒绝

| 来源机制 | 在本 skill 中的处理 | 原因 |
| --- | --- | --- |
| 分阶段招标文件分析任务 | 采用，转为稳定任务 ID、来源锚点和结构化产物 | 便于断点续做和逐项验收 |
| 任务状态、进度、日志和后台恢复 | 采用为本地工作区任务日志 | 长标书不应因页面关闭而丢失已完成结果 |
| 原文解析、规范化文本、来源文件哈希 | 采用为来源/证据台账 | 保留原始材料与加工结果的可追溯关系 |
| 全局事实集中维护 | 采用，但只允许有证据、占位或省略三种状态 | 减少公司名称、日期、金额、人员等跨章节冲突 |
| 知识库检索和证据块 | 采用为“项目范围内证据复用” | 防止跨项目复制、无来源套用和失效材料复用 |
| 三轮电子文件否决风险检查 | 采用，区分电子文件内容风险与线下动作 | 降低把签字、盖章、装订等线下事项误判为电子缺失 |
| 多种导出/版式预设 | 仅作为默认建议 | 当前招标文件、平台和原生模板始终优先 |
| `fabricate`/虚构事实模式 | 拒绝 | 投标文件不得由工具自动补造资质、案例、承诺或参数 |
| 自动判定“没有结构证据即废标” | 改造为证据阈值 + 人工复核 | 扫描件、图片、附件标题等结构线索不能被简单忽略 |
| 彩色主题、展示性排版 | 延后到合规格式确认之后 | 视觉效果不能改变响应顺序、固定表格和平台要求 |

## 2. 总体执行模型

每个项目按以下闭环执行：

```text
原始资料登记
  -> 来源完整性与可读性检查
  -> 分阶段分析任务
  -> 四类需求台账与证据台账
  -> 目录选择与人工确认
  -> 全局事实门禁
  -> 逐章写作与章节自检
  -> 合稿、重复/错字/逻辑检查
  -> 三轮电子文件否决风险检查
  -> 格式、签章、上传和交付复核
```

任何阶段发现以下情况，都应停在当前阶段并记录风险，不得用模板内容补齐：

- 原文、澄清文件、附件或官方表格缺失；
- 扫描件、图片、表格或公式无法可靠读取；
- 评分项、资格项、否决项或文件组成存在冲突；
- bidder-specific 的资质、业绩、人员、授权、品牌型号、价格或承诺没有证据；
- 格式/提交方式无法确认，且可能影响有效投标。

## 3. 分阶段任务注册表

### 3.1 任务合同

每项分析任务至少记录以下字段：

| 字段 | 要求 |
| --- | --- |
| `task_id` | 稳定的 ASCII ID，例如 `project_overview`、`response_file_requirements` |
| `label` | 中文任务名称 |
| `required` | 是否为当前模式必做任务 |
| `source_scope` | 参与分析的文件、章节、页码或文本区间 |
| `output_kind` | `markdown`、`json` 或 `markdown+json` |
| `status` | `pending`、`running`、`blocked`、`needs_review`、`success`、`error`、`skipped` |
| `gate` | `open`、`review_required` 或 `accepted`；与执行状态分开 |
| `result_path` | 结果文件路径 |
| `source_hashes` | 本次使用的原始/规范化材料哈希 |
| `started_at` / `completed_at` | 时间戳 |
| `retry_reason` | 失败重试或人工要求重跑的原因 |

任务输出必须能被下一阶段直接引用。不能只保留一段没有来源锚点的摘要。`success` 只表示任务执行完成，不表示其中的事实已经核实；来源不可读、缺附件或需要人工判断时应保持 `blocked`/`needs_review`，不能被后续章节生成过程自动改成成功。

### 3.2 最小任务集合

在没有明确的项目专用任务清单时，至少运行以下任务：

| 任务 ID | 主要结果 |
| --- | --- |
| `project_overview` | 项目名称、采购人/代理机构、采购方式、标包、预算/最高限价、服务期/交付期；缺失项标 `未提取到` |
| `technical_requirements` | 技术/服务需求及三级分解 |
| `qualification_requirements` | 资格条件、证明材料、有效期和主体要求 |
| `response_file_requirements` | 文件组成、固定表格、响应顺序、签章、上传、拆分和命名要求 |
| `key_dates` | 获取文件、澄清、投标、开标、有效期等时间及来源 |
| `business_terms` | 交付、付款、质保、验收、违约、服务等合同性条款 |
| `scoring_criteria` | 评分项、分值、评分口径、证据和主响应章节 |
| `invalid_bid_risks` | 仅保留有来源证据的电子文件风险，供后续三轮检查使用 |

按项目模式追加任务：

- 货物标：`procurement_list`、`parameter_response`、`brand_model`、`delivery_acceptance`；
- 软件平台标：`architecture_scope`、`function_modules`、`data_interface_security`、`implementation_acceptance`；
- 混合标：分别建立产品、平台、集成交付三条任务线；
- 服务标：`staffing_sla`、`workflow_records`、`training_handover`、`service_acceptance`。

### 3.3 缺失结果规则

- 对“原文在可读范围内未提及”“解析流程未拿到”“文件本身不可读”使用不同状态：前者是 `not_found`/`原文未提及`，第二种是 `not_extracted`/`未提取到`，第三种是 `unreadable`/`待核实`；
- 不得把“没有提及”改写成“无要求”；
- 结构化 JSON 任务必须固定字段，缺失字段填 `没有提及` 或 `待核实`，不得删除字段后假装完整；
- 对日期、金额、否决条件、资格条件、签章和文件组成，任何 `待核实` 都必须进入风险清单；
- 任务失败时保留错误日志和局部结果。除非修复了解析/来源问题，不得以空结果覆盖原结果。

## 4. 来源与证据台账

### 4.1 来源登记

对每个原始文件建立一条或多条来源记录：

```text
source_id
file_name
source_path
source_kind             # 招标文件/澄清/附件/模板/投标人资料/公开资料
content_hash
parser_label
page_or_section_anchor
authority_rank          # 适用法律/平台/招标文件/澄清/原生模板/投标人资料/默认建议
extraction_state        # extracted/not_found/not_extracted/needs_verification
superseded_by           # 被哪份后发布或更高效力来源替代
original_available      # yes/no
extracted_at
readability_status      # readable/partial/unreadable
```

保留原文件和规范化文本，不用后者替代前者。表格、图片、扫描页和附件标题要记录页码、表号、行号或图像占位信息；无法识别的文字必须标 `待核实`。

`not_found` 只能表示在可读且已核查的相关范围内没有出现或没有要求；`not_extracted` 表示解析流程没有拿到结果；`unreadable` 表示来源本身无法可靠读取；`needs_verification` 表示已有线索但不足以形成结论。四者不能互换，也不能把任一状态改写成“无要求”。

### 4.2 证据记录

任何写入正式投标正文的事实，都应能回指证据记录：

| 字段 | 示例 |
| --- | --- |
| `evidence_id` | `EV-TECH-001` |
| `claim` | 可被评审或验收核对的事实/承诺 |
| `source_id` | 来源文件 ID |
| `anchor` | 页码、条款、表格行、附件标题、投标人材料页码 |
| `evidence_status` | `tender-required`、`bidder-provided`、`public-verified`、`pending`、`present-unverified`、`conflicted`、`stale` |
| `allowed_scope` | 允许出现的项目、标包、章节或产品 |
| `validity` | 有效期、适用范围、版本或截止时间 |
| `response_location` | 主响应章节、附件或表格 |
| `review_owner` | 待人工核实的责任人 |

没有证据的内容可以作为“待提供材料”列出，但不能转为正式的确定性承诺。

### 4.3 证据状态门禁

- `tender-required`：招标文件要求响应，必须映射到正文、响应表或附件；
- `bidder-provided`：投标人已提供并确认可用于本项目；
- `public-verified`：来自可核验的公开来源，只能在允许的范围内使用；
- `pending`：待客户提供、待核验或来源不清，不得作为已满足结论；
- 证据过期、项目范围不符、主体不符、产品型号不符时，降为 `pending` 并触发补件。

## 5. 全局事实与跨章节一致性

把会在多个章节重复出现的事实集中管理，而不是让每章各自填写：

```text
fact_id
label
value
unit
source_evidence_ids
status                  # evidence-backed / placeholder / omit
                         # 生命周期还可为 conflicted / stale
project_scope
affected_chapters
last_verified_at
change_note
```

允许的生成模式只有：

1. `evidence-backed`：有合格证据，可写入正式正文；
2. `placeholder`：只在内部草稿、待补件清单和审核台账使用；
3. `omit`：没有证据且不影响结构时省略，不用模板性话术硬填。

事实的生命周期还可以进入 `conflicted` 或 `stale`：来源冲突、澄清覆盖、来源哈希变化或有效期失效时进入这两种状态；它们不得继续作为 `evidence-backed` 写入正式正文。

禁止 `fabricate`。不得自动生成或猜测公司名称、法定代表人、人员姓名、证书编号、案例、品牌型号、金额、日期、工期、SLA 或厂家承诺。

修改全局事实后：

- 找出 `affected_chapters`，重新检查这些章节；
- 清除或标记受影响的正文缓存和派生表格为过期；
- 重新运行跨章节一致性检查；
- 在变更记录中写明旧值、新值、证据和核验人；
- 未完成重生成和复核前，不得把旧缓存当作最终稿。

## 6. 目录选择与写作门禁

完整需求抽取后先生成候选目录，再让人工确认：

- 每个强制项、评分项和合同关键项必须有唯一主响应位置；
- 目录节点记录 `requirement_ids`、`evidence_ids`、`acceptance_outputs` 和 `writing_status`；
- 可选章节要明确“不选的理由”，不能因为模板存在就自动写入；
- 选定目录和页数预算后，才进入全文写作；
- 目录变更必须说明受影响的需求、证据、表格、交付物和页数预算。

章节 brief 至少包含：采购需求、来源锚点、允许主张、需补证据、正文重点、表格/流程图、验收输出和格式限制。

## 7. 项目内知识库与证据复用

知识库只用于定位材料，不是无条件复制的“范文库”。知识条目建议记录：

```text
item_id
title
resume
content
source_block_ids
source_file
content_hash
category                  # methodology/public_fact/bidder_fact/project_fact/template
verification              # candidate/verified/rejected/stale
project_id
allowed_claim_scope
validity
```

复用一段内容前必须完成：

1. 证明来源文件和证据块可追溯；
2. 证明适用于当前项目、标包、产品和时间范围；
3. 把通用方法改写成当前采购场景和验收口径；
4. 重新检查数字、名称、角色、接口、期限和承诺；
5. 在章节 brief 或证据台账中记录复用来源。

不同项目之间默认不共享项目事实。历史方案只能贡献结构、方法和表单思路，不能直接贡献客户名称、案例、人员、价格、资质或履约承诺。

## 8. 三轮电子文件否决风险检查

该检查只审电子投标文件内容和电子提交要求。纸质装订、现场携带原件、现场签到、线下盖章等另列为提交动作清单，不与电子文件缺失混为一谈。

对每一项检查使用以下状态，避免从“未发现”直接跳到“废标”：`not_applicable_electronic`（纯线下/当前电子材料不可判）、`no_evidence`（暂未见证据）、`present_unverified`（有目录/附件标题/表格/图片等存在性线索但内容未核实）、`evidence_conflict`（证据冲突）、`substantiated_risk`（明确招标依据与可定位投标文件证据同时满足）、`cleared`（已核实通过）。`present_unverified` 不代表内容合规。

### 第一轮：范围划分

- 从招标文件结构、投标文件组成、资格审查、符合性审查和评分办法中提取可能由电子文件判断的项目；
- 排除纯线下动作：现场签到、携带原件、纸质份数、装订、密封、现场递交；
- 保留与电子上传、电子签名、电子盖章、文件格式、文件大小、加密、解密、响应表和附件组成有关的项目。

### 第二轮：逐项证据核对

每个风险必须写出：要求来源、投标文件证据、缺失/不一致原因、建议动作。以下结构线索可作为“存在提交线索”，不能简单判定缺失：

- 目录项、章节标题、表格标题或表格行；
- 附件名称、固定格式名称、扫描页提示、图像占位符；
- 原文页码、条款编号、响应表中的空值；
- 电子签章/上传字段存在但状态未确认。

无法读取的图片或扫描件不等于没有材料，标为 `待核实` 并要求补充可读件。

### 第三轮：结论收敛

只保留有明确来源且可能影响电子文件有效性的风险；删除推测性风险、重复项和纯线下动作。每条 finding 使用：

```json
{
  "type": "invalidBid | rejectionItem",
  "severity": "high | medium | low",
  "title": "风险标题",
  "summary": "简要说明",
  "requirement": "招标要求及来源锚点",
  "bidEvidence": "当前文件中的证据或明确缺口",
  "riskReason": "为什么可能影响有效投标",
  "suggestion": "补件、修订或人工确认动作"
}
```

没有证据支持的风险输出空数组或进入 `待核实` 清单，不输出“可能废标”的吓阻性结论。

## 9. 可恢复任务日志

对于解析、分析、生成、合稿和导出等长任务，至少保留：

```text
run_id
stage
task_id
status
progress
started_at
updated_at
completed_at
logs
input_hashes
output_paths
partial_output_paths
error_code
retry_count
```

规则：

- 页面关闭、窗口切换或聊天中断不能自动丢弃成功任务；
- 恢复时先检查输入哈希是否变化，变化则重新确认影响范围；
- 失败任务保留局部结果和错误日志，修复后从最近安全节点重试；
- 不覆盖成功结果，生成新版本并保留版本关系；
- 重试应有原因，不对同一解析错误无限循环；
- 最终交付前，所有必做任务必须为 `success` 且 `gate=accepted`；若人工决定带风险继续，必须在独立复核记录中明确记录 `accepted-with-risk`，不得把它伪装成任务成功或事实已核实。

## 10. 版式预设：只作静默场景下的默认值

在格式台账确认招标文件、平台和原生模板均未规定时，可以从标准候选预设中选择；选择结果必须写入格式台账，并标注为 `默认建议`。紧凑评审和图文方案只作参考策略，须由用户明确选择且不得触及硬性格式：

| 预设 | 适用场景 | 主要特点 |
| --- | --- | --- |
| `standard-bid` | 普通综合投标文件 | 纵向正文、稳定层级、清晰页码和表格 |
| `formal-binding` | 需要正式装订或纸质归档 | 预留装订空间、正式封面和目录页 |
| `wide-table` | 参数、清单、接口、评分矩阵较多 | 对宽表使用横向页面或局部横页 |

参考策略：`compact-review` 控制空白和装饰、优先信息密度；`illustrated` 在技术方案需要架构图、流程图和场景说明时使用，但不以装饰替代响应内容。

预设不得覆盖以下任何明确要求：纸张、字体、字号、行距、页边距、目录/章节顺序、固定表格、页码、签字盖章、骑缝章、文件拆分、命名、加密、上传和平台制作方式。主题色、封面图和装饰元素不得进入固定响应表或影响可读性。

## 11. 交付前的四层质检

按下列顺序执行，并区分机器提示与人工结论：

1. **覆盖检查**：强制项、评分项、三级需求、合同项是否都有主响应、证据和验收关联；
2. **事实检查**：全局事实、数字、日期、名称、型号、人员、期限和承诺是否一致且有证据；
3. **文本检查**：重复段落、错别字、断句、逻辑矛盾、模板残留、占位符和 AI 味表达；
4. **提交检查**：格式台账、固定表格、签章、文件组成、大小、命名、加密、上传、解密、纸质动作和交付清单。

推荐将重复、错字和逻辑检查定义为 `warning` 或 `manual-review`，不能仅凭文本相似度自动判定废标。命中后回到对应章节和证据台账复核。

## 12. 指标的正确使用

可以统计以下诊断指标：

- 已登记来源数、可读/部分可读/不可读来源数；
- 已提取任务数、成功/失败/待核实任务数；
- 需求覆盖率、评分项证据覆盖率、三级需求响应率；
- 知识条目过滤、恢复、命中和复用数量；
- 章节重生成数量、过期缓存数量、重复/错字/逻辑检查告警数量。

这些指标只用于发现工作缺口，不能直接证明“满足招标要求”或“不会废标”。最终结论仍需回到原始招标文件、官方澄清、平台规则和投标人证据。
