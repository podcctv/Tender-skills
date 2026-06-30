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

## 适用场景

使用这个 skill 处理以下任务：

- 分析招标文件、评分办法、技术规范、商务条款、资格要求。
- 生成投标技术方案、服务方案、实施方案、运维方案、培训方案等框架。
- 建立评分点/响应点/证据材料的追踪矩阵。
- 逐章编写 HTML、Markdown 或 DOCX 目标稿件。
- 合稿后进行占位符、漏项、证据缺口和一致性检查。
- 模拟合规、技术、评分、交付、商务/法务等多专家评审。

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

## 推荐投标工作流

1. **资料接收**：收集招标文件、附件、图纸、澄清文件、响应格式和模板。
2. **需求抽取**：输出评分标准、资格要求、技术参数、商务条款、格式要求、证据矩阵。
3. **框架与 brief**：按 MECE 原则生成章节框架和每章 brief，先让人工确认。
4. **逐章编写**：按 brief 分章生成内容；有图表时优先 HTML，便于嵌入 SVG。
5. **章节自检**：检查需求覆盖、占位符、证据缺口、跨章节一致性。
6. **合稿质检**：合并章节并输出 QC 报告。
7. **专家评审**：从合规、技术、评分、交付、商务/法务五个角度评审。
8. **迭代修订**：按得分和风险继续修改，直到达到目标质量。
9. **交付清单**：输出最终文件、附件、签章、格式、未决事项清单。

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
