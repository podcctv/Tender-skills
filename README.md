# Tender-skills

面向投标/售前方案编制的可移植 AI skill。核心 skill 名称为 `tender-bid-writer`，用于让 Codex、OpenClaw、Hermes 等 agent 从招标文件中抽取需求、生成投标方案框架、编写章节、合稿质检、模拟专家评审并输出交付清单。

流程将“需求抽取 -> 章节 brief -> 人工确认 -> 逐章编写 -> 合稿 -> 质检 -> 多专家评审 -> 多轮修订 -> 最终交付”固化为一个可复用的 skill。

## 仓库结构

```text
skills/
  tender-bid-writer/
    SKILL.md
    agents/
      openai.yaml
    references/
      workflow.md
      checklists.md
      platform-compatibility.md
    scripts/
      bid_quality_check.py
```

- `SKILL.md`：skill 主入口，定义触发场景和执行流程。
- `agents/openai.yaml`：Codex/OpenAI 系产品可读取的 UI 元数据。
- `references/workflow.md`：投标全流程、阶段门和推荐产物结构。
- `references/checklists.md`：需求台账、章节 brief、质检、专家评审模板。
- `references/platform-compatibility.md`：Codex、OpenClaw、Hermes 适配说明。
- `scripts/bid_quality_check.py`：可选的本地质检脚本。

## GitHub 同步约定

- 远端仓库统一使用 `https://github.com/podcctv/Tender-skills.git`。
- 工作分支统一使用 ASCII 名称，默认使用 `codex/tender-skills`。
- 不要使用中文、空格或不可见字符作为分支名，避免 GitHub 出现 hidden character warning 或 head ref 转义提示。
- 后续提交、推送和 PR 都应基于 `codex/tender-skills` 分支进行，除非维护者明确指定其他 ASCII 分支名。

## 适用场景

使用这个 skill 处理以下任务：

- 分析招标文件、评分办法、技术规范、商务条款、资格要求。
- 将采购需求拆解到三级：一级需求域/系统边界，二级功能或服务事项，三级最小响应单元。
- 生成投标技术方案、服务方案、实施方案、运维方案、培训方案等框架。
- 建立评分点/响应点/证据材料的追踪矩阵。
- 按厚标书标准逐章编写 HTML、Markdown 或 DOCX 目标稿件。
- 合稿后进行占位符、漏项、证据缺口和一致性检查。
- 模拟合规、技术、评分、交付、商务/法务等多专家评审。

## 核心写作标准

- 招标文件是唯一事实源。不得编造资质、证书、案例、人员、价格、工期、授权、签章状态或第三方承诺。
- 采购需求必须先细化到三级。第三级应能直接对应正文小节、响应证据、交付物或验收点。
- 无招标页数硬限制时，按项目价值和复杂度规划整标篇幅，可用 `1 万元 ≈ 1 页` 作为基础测算；重大项目原则上不低于约 `300-500 页`。
- 最小正式正文小节通常不少于 `3-5 段`。每段应有机制、场景、执行细节、表单记录、风险控制或验收支撑，不能只换说法重复标题。
- 表格必须服务评审和落地，例如需求响应矩阵、接口联调检查表、数据质量检查表、风险预防表、交付文档清单、验收映射表。
- 正式章节不得出现 `TODO`、`待确认`、`公司名称`、`项目名称：填写`、`如有证据再补` 等内部草稿痕迹。

## 安装到 Codex

### 自然语言安装

可以直接把下面这句话发给支持读写本地文件的 agent：

```text
请从 https://github.com/podcctv/Tender-skills 获取投标 skill，并将 skills/tender-bid-writer 安装到当前工具可发现的 skills 目录中；安装后用 $tender-bid-writer 作为调用名称。
```

### 方式一：放入 Codex skills 目录

将 `skills/tender-bid-writer` 复制到 Codex 可发现的 skills 目录。

Windows 常见路径：

```powershell
Copy-Item -Recurse ".\skills\tender-bid-writer" "$env:USERPROFILE\.codex\skills\tender-bid-writer"
```

macOS / Linux 常见路径：

```bash
cp -R ./skills/tender-bid-writer ~/.codex/skills/tender-bid-writer
```

然后在 Codex 中使用：

```text
Use $tender-bid-writer to analyze this tender package and produce the requirement ledger.
```

中文也可以：

```text
使用 $tender-bid-writer 分析这个招标文件，先抽取评分标准、资格要求、技术参数和商务条款。
```

### 方式二：在当前工作区显式引用

如果不想安装到全局目录，可以保留本仓库结构，并在提示词中说明：

```text
Use $tender-bid-writer from ./skills/tender-bid-writer to create the proposal outline and chapter briefs.
```

## 在 OpenClaw 中使用

OpenClaw 的 skill 形态通常也是一个包含 `SKILL.md` 的目录。使用方式：

1. 克隆本仓库。
2. 将 `skills/tender-bid-writer` 放入 OpenClaw 当前配置的 skills 目录，或在 OpenClaw 配置中添加该目录为外部 skill 路径。
3. 在任务中显式调用：

```text
Use $tender-bid-writer to extract all mandatory and scored requirements from the tender documents.
```

如果 OpenClaw 当前环境不支持执行本地 Python 脚本，也可以正常使用 skill 主流程；质检脚本中的规则可由 agent 按清单手工执行。

## 在 Hermes 中使用

Hermes 如果支持文件型 skill 或知识/工具指令包，可直接使用 `skills/tender-bid-writer` 目录。

如果 Hermes 需要单独 manifest，可按下面映射：

| 本仓库字段 | Hermes 中建议映射 |
| --- | --- |
| `SKILL.md` frontmatter `name` | skill/tool name |
| `SKILL.md` frontmatter `description` | trigger / routing description |
| `SKILL.md` body | execution instructions |
| `references/` | lazy-loaded supporting docs |
| `scripts/` | local tools, if command execution is available |

推荐调用方式：

```text
Use tender-bid-writer to build a MECE proposal outline, create chapter briefs, and wait for confirmation before drafting.
```

## 分阶段使用指南

不要一上来要求 agent 直接写完整标书。推荐按阶段推进，每个阶段都留下可追溯产物。

### 1. 资料接收与工作区整理

目标：确认招标文件、附件、图纸、澄清文件、响应格式、模板和证据材料是否齐全。

推荐提示词：

```text
使用 $tender-bid-writer 整理当前工作区的招标资料。请识别招标文件、附件、澄清文件、格式模板和证据材料，建立 00_source 到 06_delivery 的工作目录，并列出缺失或无法读取的文件。
```

阶段产物：资料清单、缺失文件清单、风险提示、工作目录。

### 2. 需求抽取与三级细化

目标：先抽取评分标准、资格要求、技术参数、采购需求、商务条款和格式要求，再把采购需求细化到三级。

三级拆解建议：

| 层级 | 含义 | 示例 |
| --- | --- | --- |
| 一级 | 需求域、系统边界、平台或服务大类 | 数据中台、交易服务平台、运维服务 |
| 二级 | 功能、服务事项、控制对象或交付物组 | 数据治理、接口联调、故障响应 |
| 三级 | 最小响应单元，可写正文、可检查、可验收 | 主数据编码规则、接口异常重试机制、P1 故障处置记录 |

推荐提示词：

```text
使用 $tender-bid-writer 抽取招标文件中的评分标准、资格要求、技术参数、采购需求和商务条款。采购需求必须细化到三级，并为每个三级需求标注来源页码/条款、响应章节、证据材料和验收关联。
```

阶段产物：评分台账、资格台账、技术参数台账、商务条款台账、采购需求三级分解表、证据矩阵。

### 3. 整体篇幅规划与章节 brief

目标：在写正文前先确定整标厚度、章节结构、每章目标、证据边界和验收输出。

规则：

- 若招标文件有页数上限、格式模板或固定响应表，优先服从招标文件。
- 若无硬限制，按 `1 万元 ≈ 1 页` 规划整体篇幅，并结合复杂度向上调整。
- 重大项目整套技术/商务响应原则上不低于约 `300-500 页`。
- 每个三级采购需求应有一个主响应位置，不能散落在多个章节无人负责。

推荐提示词：

```text
使用 $tender-bid-writer 基于需求台账生成投标文件整体框架和章节 brief。请给出整标页数预算、每章目标页数、三级采购需求映射、拟使用表格、证据需求和验收支撑材料。先不要写正文，等我确认框架。
```

阶段产物：目录框架、页数预算表、章节 brief、需求-章节映射表、证据需求清单。

### 4. 逐章厚标书正文编写

目标：按确认后的 brief 一章一章写，不写泛化模板。

正文要求：

- 每个最小正式正文小节至少 `3-5 段`，除非是固定格式表、符合性声明或招标文件要求短答。
- 优先使用 `机制 + 场景 + 表单 + 输出成果` 结构。
- 平台型软件项目要写到系统边界、数据链路、接口联调、数据迁移、主数据、质量追溯、业务连续性、演示功能等专项。
- 表格要能支撑评分、实施或验收，不能只是装饰。

推荐提示词：

```text
使用 $tender-bid-writer 按已确认的章节 brief 编写《质量管理方案》正文。请覆盖对应三级采购需求，每个最小小节不少于 3-5 段，并加入质量指标表、阶段门禁表、问题分级表、验收映射表和过程记录说明。
```

阶段产物：单章正文、章节表格、过程记录模板、验收映射材料。

### 5. 章节自检与补强

目标：每章完成后先评审，不要直接合稿。

检查重点：

- 是否覆盖评分项、强制要求和三级采购需求。
- 是否存在无证据承诺、草稿痕迹或虚构材料。
- 是否有足够项目场景，而不是通用软件工程模板。
- 每个最小正文小节是否达到 `3-5 段` 且内容实。
- 是否形成可验收、可追踪的输出物。

推荐提示词：

```text
使用 $tender-bid-writer 对刚完成的章节做章级评审。请检查评分覆盖、三级采购需求覆盖、3-5 段正文要求、证据缺口、草稿痕迹、跨章节冲突和验收追踪关系，并给出修订清单。
```

阶段产物：章级评审表、修订清单、证据缺口清单。

### 6. 合稿质检与专家评审

目标：合并章节后，从合规、技术、评分、交付、商务/法务角度模拟评审。

推荐提示词：

```text
使用 $tender-bid-writer 合并已确认章节并运行质检。请输出漏项、短章节、占位符、证据缺口、三级需求未响应项、页数不足项和跨章节冲突，再模拟五类专家评审并给出提分修订计划。
```

阶段产物：合稿文件、QC 报告、专家评审意见、提分修订计划。

### 7. 最终交付

目标：形成提交前清单，确认签章、附件、格式和未决事项。

推荐提示词：

```text
使用 $tender-bid-writer 准备最终交付清单。请核对最终文件、附件、响应表、证据材料、签章要求、格式要求、未决确认事项和提交风险。
```

阶段产物：最终交付清单、签章清单、附件清单、未决风险清单。

## 本地质检脚本

`scripts/bid_quality_check.py` 是一个无第三方依赖的辅助脚本，可以扫描草稿中的明显风险：

- `TODO`、`TBD`、`待补充`、`待确认` 等占位符。
- 过短章节。
- 需求文件和方案正文之间的覆盖缺口。
- 证书、资质、授权、案例、人员等证据引用不足。

示例：

```bash
python skills/tender-bid-writer/scripts/bid_quality_check.py \
  --workspace ./my-bid-workspace \
  --proposal ./my-bid-workspace/03_chapters \
  --requirements ./my-bid-workspace/01_requirements \
  --out ./my-bid-workspace/05_qc/qc_report.md
```

脚本只做机器粗筛，不能替代人工复核。正式投标前必须人工核对否决项、评分标准、格式要求、签章要求和所有证据材料。

## 安全边界

这个 skill 明确要求：

- 以招标文件为唯一事实源。
- 不编造资质、证书、案例、价格、工期、授权、签章状态或第三方承诺。
- 对缺失信息标记 `待确认`。
- 涉及否决项、资格风险、法律/商务承诺时先要求人工确认。

## 快速提示词

```text
Use $tender-bid-writer to analyze the tender files in this workspace. First create requirement ledgers for scoring criteria, qualification requirements, technical specifications, and business clauses. Do not draft the full proposal until I confirm the outline and chapter briefs.
```

中文版本：

```text
使用 $tender-bid-writer 分析当前工作区的招标文件。先抽取评分标准、资格要求、技术参数和商务条款，生成需求台账、方案框架和章节 brief。等我确认后再开始逐章编写。
```
