# Chapter Structure And DOCX Output Rules

Use this reference when creating outlines, chapter briefs, formal technical chapters, or DOCX deliverables. It addresses common problems: evenly expanded目录, thin priority topics, fixed paragraph counts, mechanical titles, decorative tables, and inconsistent Word formatting.

## Structure Rebalancing

- Do not expand every chapter evenly. Before outlining, classify each chapter as `light`, `standard`, `priority`, or `excellence-topic`.
- Ordinary chapters should stay light: 2-4 main subsections, shorter leaf sections, fewer tables.
- Priority chapters should go deeper: 3-6 main subsections, clear leaf sections, dedicated scoring/evidence tables.
- Sibling heading counts should vary naturally between 2 and 6. Do not make every group exactly 3 or 4 headings.
- Leaf headings should not all stop at the same level. A natural thick technical proposal may contain Heading 4, Heading 5, and Heading 6 leaves in the same chapter.
-正文 should mainly sit under leaf headings, not under every intermediate heading. Intermediate headings organize logic; leaf headings carry the writing, records, tables, and acceptance evidence.

## Six Excellence Topics

For software-platform, data-platform, integration, migration, or complex hybrid bids, treat these as priority "优于招标" topics whenever relevant:

1. 数据一致性校验
2. 接口联调
3. 新旧系统并行运行
4. 切换演练
5. 业务回退
6. 过渡期运维

Rules:

- Expand each relevant topic to 5-6 heading levels when the tender has no conflicting format limit.
- Give these topics more正文 than ordinary content: leaf sections normally contain 3-5 paragraphs, with each paragraph around 200-500 Chinese characters when the content supports it.
- Write from operational scenes: data批次、主数据、接口报文、异常回执、并行账期、演练窗口、回退触发条件、值守班次、问题复测、采购人确认.
- Each topic should include at least one evaluative table or checklist, and when it is a full chapter, at least one flowchart/process diagram.
- Connect each topic to验收: migration check report, interface joint-debug record, parallel-run comparison report, drill sign-off, rollback decision record, transition O&M issue ledger, purchaser confirmation.

##正文 Depth Rules

- Write正文 mainly at the lowest leaf level.
- Leaf正文 length varies by importance:
  - Light leaf: 1 paragraph.
  - Standard leaf: 2-3 paragraphs.
  - Priority leaf: 3-5 paragraphs.
  - Excellence-topic leaf: 3-5 paragraphs plus a table/checklist/record where useful.
- Do not fix every paragraph to the same length. A natural range is 200-500 Chinese characters per paragraph for substantive正文; shorter paragraphs are acceptable for compliance statements, table introductions, and transition text.
- Range/scope/background sections should be concise. Data, interface, rollback, parallel-run, transition O&M, acceptance, and risk-control sections should be comparatively thicker.

## Language And Heading Rules

Avoid fixed openings and template phrases:

- `本项目属于……`
- `围绕……`
- `项目经理会……`
- `从以往经验看……`
- `控制要点1`
- `细化核查1`
- `接口联调控制要点1`

Preferred writing:

- Start directly with the matter, mechanism, scene, record, or acceptance basis.
- Name the control object:报文样例、异常回执、主数据编码、并行差异、演练窗口、回退清单、值守工单.
- Use scene-based headings, for example: `报文样例核对`, `异常回执处理`, `外部值守安排`, `复测关闭口径`, `并行差异复核`, `回退触发确认`.
- Do not write mechanical numbered headings where the noun does no work. A heading should tell the evaluator what will be checked, delivered, or accepted.

## Tables And Flowcharts

- Each major chapter should include at least one flowchart/process diagram and one useful table unless the tender format prohibits it or the chapter is a short compliance/form chapter.
- Tables must support evaluation, implementation, or acceptance. Use them for:
  - responsibility matrix;
  - risk ledger;
  - acceptance mapping;
  - interface list;
  - data consistency checks;
  - issue severity and escalation;
  - delivery document list;
  - trial-run or transition O&M ledger.
- Do not create decorative tables that merely repackage slogans.
- Introduce every table or flowchart with its evaluation purpose: what scoring item, implementation decision, or acceptance record it supports.

## Word Master Template And Style Rules

For final Word chapter delivery:

- Use `投标文档格式.docx` as the Word master template when available in the project workspace or provided by the user.
- Do not manually type chapter numbers such as `第一章`, `1.1`, or `1.1.1` in heading text unless the tender's official form requires literal numbering. Let Word numbering/styles handle numbering.
- Use Word Heading 1-9 styles as the semantic heading carriers. The template should map them to `TB_01` through `TB_09`; keep that mapping rather than direct-formatting headings.
- Use `TB表格` for table-cell body text when the style exists.
- Keep diagrams and tables editable where practical; avoid flattening core proposal content into screenshots.
- If the template is missing, ask the user for `投标文档格式.docx` before final styled DOCX generation, or produce draft DOCX/Markdown while clearly marking that template application is pending.

## Per-Chapter Output Rules

- Generate each major chapter as a separate DOCX.
- Put finalized chapter files under `分章节定稿`.
- Use sortable filenames with a two-digit prefix and a short chapter name, for example:
  - `06-数据迁移与一致性校验-DG格式版.docx`
  - `07-接口联调与并行运行-DG格式版.docx`
  - `08-切换演练与业务回退-DG格式版.docx`
- Keep one chapter per file so the user can sort, review, replace, and merge later.
- After creating each chapter DOCX, render/inspect it when tooling is available and record whether template, headings, table styles, flowchart/table presence, and file naming passed.

## Chapter QC

Before declaring a chapter complete:

- Check that the chapter importance classification matches its depth.
- Check sibling heading counts vary naturally between 2 and 6.
- Check leaf levels include a mix of Heading 4/5/6 when the chapter is thick.
- Check正文 mostly appears under leaf headings.
- Check the six excellence topics, where relevant, are visibly deeper and more detailed than ordinary sections.
- Check no mechanical headings such as `控制要点1` or `细化核查1` remain.
- Check each chapter has at least one useful flowchart and one useful table, or explain why not.
- Check Word output uses the master template and styles instead of manual numbering/direct formatting.
