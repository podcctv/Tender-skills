# 输出模板与转换(Templates)

本文件提供三类可直接复用的模板:HTML 章节模板、合稿转 DOCX 指引、标准表格库。agent 应复制模板后填入项目内容,不要每次重新发明格式。

## 1. HTML 章节模板

适合需要架构图、流程图、复杂表格的技术方案章节,后续可整册转 DOCX。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>第N章 章节名称</title>
<style>
  /* A4 版式,打印与转 Word 友好 */
  body { font-family: "SimSun", "Songti SC", serif; font-size: 12pt;
         line-height: 1.7; margin: 2.5cm 2cm; color: #000; }
  h1 { font-family: "SimHei", sans-serif; font-size: 18pt; text-align: center;
       page-break-before: always; }
  h2 { font-family: "SimHei", sans-serif; font-size: 15pt; margin-top: 1.5em; }
  h3 { font-family: "SimHei", sans-serif; font-size: 13pt; margin-top: 1.2em; }
  p { text-indent: 2em; margin: 0.4em 0; text-align: justify; }
  table { border-collapse: collapse; width: 100%; margin: 0.8em 0;
          font-size: 10.5pt; page-break-inside: avoid; }
  th, td { border: 1px solid #000; padding: 4px 6px; text-align: left;
           vertical-align: top; }
  th { background: #f2f2f2; font-family: "SimHei", sans-serif; }
  caption { font-weight: bold; margin-bottom: 4px; text-align: left; }
  .fig { text-align: center; margin: 1em 0; }
  .fig-caption { font-size: 10.5pt; text-align: center; }
  .no-break { page-break-inside: avoid; }
</style>
</head>
<body>
<h1>第N章 章节名称</h1>

<h2>N.1 一级小节</h2>
<h3>N.1.1 二级小节</h3>
<p>响应句:满足招标文件第X页第X条要求。机制说明……</p>
<p>本项目场景化说明,引用招标文件中的业务名词……</p>
<p>执行细节、表单与记录说明……</p>
<p>输出成果与验收衔接:本节执行记录见表N-1,验收时提供……</p>

<table>
<caption>表N-1 表格标题(评审/实施用途)</caption>
<tr><th style="width:8%">序号</th><th>列A</th><th>列B</th><th style="width:20%">责任角色</th></tr>
<tr><td>1</td><td></td><td></td><td></td></tr>
</table>

<div class="fig">
  <svg viewBox="0 0 800 400" width="100%" xmlns="http://www.w3.org/2000/svg">
    <!-- 架构图/流程图用内联 SVG,保证转 DOCX 后仍为矢量 -->
  </svg>
  <div class="fig-caption">图N-1 图题</div>
</div>
</body>
</html>
```

注意事项:

- 每章一个文件,命名 `chapter_XX_章节名.html`,放在 `03_chapters/`。
- SVG 直接内联,不要用外链图片;转 DOCX 前用无头浏览器或 LibreOffice 渲染。
- 表格必须带 `caption` 编号,正文引用"见表N-1"。
- 禁止内联样式写死字体颜色花哨配色;标书打印常为黑白。

## 2. 合稿与 DOCX 转换

### 2.1 合稿

按目录顺序拼接章节文件为 `04_merge/final_proposal.html`,保留各章 `<style>` 于 head 中(只保留一份)。

### 2.2 HTML → DOCX(Pandoc,推荐)

```bash
pandoc 04_merge/final_proposal.html \
  -o 06_delivery/proposal.docx \
  --reference-doc=template.docx \
  --toc --toc-depth=3 \
  --metadata title="XX项目投标文件-技术部分"
```

- `template.docx`:用采购人提供的格式模板,或自建一份定义了 Heading1-3、正文、表头样式的模板。
- 转换后人工检查:目录页码、表格跨页、SVG 是否被栅格化、页眉页脚、页码。

### 2.3 HTML → DOCX(LibreOffice,无 Pandoc 时)

```bash
libreoffice --headless --convert-to docx \
  --outdir 06_delivery 04_merge/final_proposal.html
```

### 2.4 有页数/格式硬限制时

若招标文件规定页数上限、字号、行距、双面打印,格式服从招标文件;先转一章验证格式再全册转换。

## 3. 标准表格库

以下表格覆盖四类投标模式的高频评审/实施需求。列结构可直接复制,按项目增删列;每张表必须在正文中被引用并说明用途。

### 3.1 评分点响应矩阵(所有模式必用)

| 评分项ID | 评分标准原文(页码) | 分值 | 响应章节 | 响应策略(满足/优于) | 证据材料 | 责任人 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S-01 | 技术方案先进性(第X页) | 10 | 第3章3.2 | 优于:增加AI辅助派单 | 演示脚本 | 方案组 | 待确认 |

用途:开标前逐项核对得分覆盖;每行必须有响应章节和证据列。

### 3.2 技术参数响应表(goods / hybrid 必用)

| 序号 | 招标参数要求(页码) | 响应参数 | 偏离(正/无/负) | 证明材料(彩页页码/报告编号) | 备注 |
| --- | --- | --- | --- | --- | --- |
| 1 | 双电源(第X页) | 2×800W 冗余电源 | 无偏离 | 彩页P12;检测报告编号XXX | — |

### 3.3 偏离表与负偏离风险表(goods / hybrid 必用)

| 条目 | 招标要求 | 我方响应 | 偏离类型 | 风险评估 | 处理措施 |
| --- | --- | --- | --- | --- | --- |
| 质保期 | 3年 | 3年 | 无偏离 | — | — |
| 到货期 | 合同签订后30日 | 45日 | 负偏离 | 可能废标/扣分 | 与厂家确认加急排产,或调整投标策略 |

规则:任何负偏离必须在开标前让用户书面确认。

### 3.4 SLA/KPI 承诺表(service 必用)

| 服务项 | 招标要求 | 我方承诺(优于) | 测量方式 | 未达标处置 |
| --- | --- | --- | --- | --- |
| P1故障响应 | 30分钟 | 15分钟 | 工单系统时间戳 | 当月服务费扣0.5% |
| 系统可用率 | ≥99.5% | ≥99.9% | 监控平台月报 | 免费延长服务期1周 |

### 3.5 人员配置表(service / platform / hybrid 常用)

| 角色 | 人数 | 资质要求(招标原文) | 拟投入人员资质 | 投入阶段 | 社保/劳动关系证明 |
| --- | --- | --- | --- | --- | --- |
| 项目经理 | 1 | PMP+5年经验 | 待用户证据(详见附件X) | 全过程 | 详见附件X |

注意:人员信息没有证据前只写"拟"并指向附件,不得虚构姓名和证书。

### 3.6 责任矩阵(hybrid 必用)

| 交付活动 | 供应商-设备线 | 供应商-软件线 | 采购人 | 第三方(原厂/监理) | 完成标志 |
| --- | --- | --- | --- | --- | --- |
| 设备到货开箱 | 主责 | 配合 | 验收签字 | 原厂授权工程师 | 开箱验收单 |
| 接口联调 | 配合 | 主责 | 提供对方系统对接人 | — | 联调测试报告 |
| 试运行 | 配合 | 主责 | 业务验证 | — | 试运行报告 |

### 3.7 风险登记与预防表(所有模式常用)

| 风险ID | 风险描述 | 阶段 | 概率 | 影响 | 预防措施 | 应急措施 | 责任角色 | 记录表单 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-01 | 数据迁移字段映射缺失 | 实施期 | 中 | 高 | 迁移前两轮数据摸底 | 回滚方案+人工比对 | 数据工程师 | 迁移记录表 |

### 3.8 验收映射表(所有模式收尾必用)

| 三级需求/评分点 | 验收标准(招标原文) | 交付物 | 验收方式 | 验收阶段 | 对应章节 |
| --- | --- | --- | --- | --- | --- |
| 主数据编码规则 | 编码与国标一致 | 编码规范+主数据清单 | 专家审查 | 初验 | 第3章3.4 |

用途:确保每个三级需求可验收、可追溯;终验前逐行打钩。

## 4. 模板使用规则

1. 先查招标文件是否给定格式模板:有则完全服从,本库仅补充招标未规定的内部台账。
2. 表格编号全册连续或按章连续,保持一致。
3. 台账类表格(评分矩阵、偏离表、验收映射)属于内部工作产物,交付前确认是否需要随标书提交。
4. 所有"待用户证据"单元格,合稿质检时必须清零或改为指向正式附件。
