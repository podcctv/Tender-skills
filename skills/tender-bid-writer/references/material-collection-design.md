# Material Collection Package Design

Use this reference when producing outsourced bid intake packages, client material request lists, or tender-native fill-in packages. The goal is to make the client understand exactly what to upload, what to fill, what to sign/seal, and what can be skipped.

## Core Pattern

Structure the client-facing package in three parts, then add tender-native forms and submission controls as needed:

1. **Qualification and Regulatory Baseline**
   - Start with statutory/general eligibility items when the project is a government procurement or regulated industry bid.
   - Then extract tender-stated qualification items, mandatory attachments, enterprise information, personnel credentials, licenses, deposits, platform status, signature/seal requirements, and credit checks.
   - Separate `tender-required upload evidence` from `regulatory/legal operation confirmation`.
   - If the tender does not require a document but a law/regulation may require the capability for lawful performance, do not automatically mark it as `must-provide-or-reject`. Mark it as `legal-baseline-confirmation` or `must-respond-can-commit` unless the tender, law, or purchaser instruction requires pre-bid evidence upload.

2. **Scoring Evidence**
   - Extract every scoring item, score value, scoring threshold, proof material, and "no proof no score" condition.
   - Ask for evidence at the same grain as the scoring rule: contract count and dates, vehicles by type, personnel count and certificates, warehouse area, software copyright, demonstrations, SLA records, etc.
   - Distinguish `scoring-critical` evidence from optional credibility evidence.
   - Include "supplementary proof" when it helps prove authenticity, such as invoices, acceptance forms, delivery records, client evaluations, screenshots, or audit reports.

3. **Bid-Type Increment Pack**
   - Add only the evidence families that fit the bid type and industry.
   - Do not ask every client for every possible material. Use type-specific increments to keep collection easy.

## Tender-Native First

When the tender provides official forms, tables, quotation schedules, or response formats:

- Reproduce those forms in the client package before adding generic checklists.
- Preserve form titles, columns, units, notes, package numbers, signature/seal locations, quotation units, and original row grain.
- Add helper prompts in a separate "填写说明/我方备注" column or in a writer-control table, not inside the official form structure.
- For Word/DOCX tender sources, produce the client package as a `.docx` with Word-native tables. Add `.xlsx` only for large repeated rows.

## Material Necessity Classification

Use these labels consistently:

| Label | Meaning | Client message |
| --- | --- | --- |
| `must-provide-or-reject` | Tender, qualification, signature/seal, deposit, deadline, or mandatory attachment requirement. Missing it may cause rejection or invalid bid. | "必须提供，否则可能废标/无效响应。" |
| `legal-baseline-confirmation` | Law/regulation requires the capability or lawful status for performance, but tender does not clearly require upload as a bid attachment. | "请确认具备；如有证明建议提供。未提供不一定废标，但会影响合规与履约风险。" |
| `must-respond-can-commit` | Requirement must be answered, but a formal commitment/plan can satisfy it unless tender asks for attachment proof. | "必须响应，可先承诺，证据越充分越好。" |
| `scoring-critical` | Missing evidence normally loses points or weakens a scored claim. | "不一定废标，但会丢分或降低得分把握。" |
| `optional-supporting` | Helps polish credibility, not required for compliance or scoring. | "时间紧可省略。" |
| `not-needed-now` | Not requested by the tender or not useful at the current stage. | "暂不索要，避免增加客户负担。" |

## Regulatory Baseline Rule

For legal or regulatory items:

- Prefer current primary/official sources when the answer affects compliance, rejection risk, or lawful performance.
- Do not treat a statutory operation obligation as a pre-bid upload requirement unless the tender or regulation requires proof at bidding stage.
- If the tender is silent but performance would be unlawful without a license/certificate/health status, add it to the client question list and material package as `legal-baseline-confirmation`.
- If the tender explicitly requires the document, upgrade it to `must-provide-or-reject`.
- If a scoring item gives points for the document or capability, classify the evidence as `scoring-critical`.

Common examples:

- Government procurement projects: use the Government Procurement Law Article 22 conditions as the baseline for civil capacity, commercial reputation, financial/accounting system, equipment/professional capability, tax/social security payment records, no major illegal record, and other legal/administrative conditions.
- Food, catering, ingredient supply, canteen distribution: check lawful food operation status, food business/production license or prepackaged-food filing as applicable, employee health certificates for direct food-contact work, traceability, purchase inspection, testing/inspection, cold-chain evidence, non-GMO commitments where required, and packaging label evidence.
- Industry-regulated services: check whether the service can be legally performed without sector licenses, operator certificates, safety certificates, filing, insurance, or staff credentials.

## Recommended Client Package Architecture

Use this order for easy client cooperation:

1. **封面/使用说明**
   - Project name, deadline, submission mode, urgent P0 reminder, how to return materials.

2. **第一部分：资格项与法规基线确认**
   - Tender-stated qualification items.
   - Government procurement or sector-law baseline items.
   - Enterprise information form.
   - Platform/account/deposit/signature-seal requirements.
   - Personnel, license, health, safety, inspection, and legal-operation confirmations.

3. **第二部分：评分项资料清单**
   - Score item, points, threshold, required evidence, supplementary evidence, current status, score risk.
   - Include "no proof no score" language when tender says so.

4. **第三部分：按投标类型增补**
   - Add only relevant type-specific evidence packs.
   - Keep the type increment after qualification and scoring so the client sees essentials first.

5. **第四部分：采购文件原生表单**
   - Tender-native forms and fill-in tables, or a pointer to a companion workbook.

6. **第五部分：签字盖章/提交方式清单**
   - Submission type (`electronic-bid`, `paper-bid`, `dual-bid`), signature/seal mode, scan/upload, CA/electronic seal, binding/envelope if relevant, operator, deadline, consequence.

## Bid-Type Increment Matrix

| Bid type / scenario | Add these evidence families |
| --- | --- |
| Standard goods supply | Product specs, model/brand consistency, brochures, test reports, certificates, manufacturer authorization if required, warranty, delivery plan, parameter response, deviation table, packaging/label evidence. |
| Food / canteen / ingredient supply | Food business/production license or prepackaged filing, staff health certificates, meat quarantine, pesticide residue tests, grain/oil/dry goods quality reports, cold-chain traceability, supplier/channel list, package labels, non-GMO proof/commitment, warehouse and vehicle proof, emergency replenishment, unlisted ingredient supply capability. |
| Service operation / outsourcing | Staffing roster, labor relationship/social security, certificates, shift plan, SLA/KPI, service workflow, tools, escalation, reports, continuity plan, training, assessment records. |
| Software / platform | Software copyrights if scored/required, product screenshots, demo environment, architecture, function matrix, data/interface/security evidence, implementation team, project cases, testing/acceptance records, operation support. |
| Hybrid goods + software/integration | Product evidence track, platform/function evidence track, integration delivery track, deployment/joint debugging/testing/training/acceptance records, responsibility matrix. |
| Construction / engineering-like bid | Licenses, safety production permit, personnel certificates, project manager/engineer certificates, construction organization design, schedule, safety/civilized construction, quality controls, equipment, similar projects. Use a construction-specific workflow when detailed construction methods are central. |

## Sample-Inspired Food Procurement Structure

The "fire rescue canteen ingredient distribution" sample uses an effective pattern:

- Title note: project name, special fees, material format, deadline.
- Qualification section:
  - Government Procurement Law baseline.
  - Business license, authorization, social security, tax payment, audit/credit proof, deposit, SME declaration, food license/filing.
  - Enterprise information.
  - Personnel health certificates.
  - Product testing reports.
- Scoring section:
  - Performance cases with contracts/award notices plus invoices or履约 proof.
  - Vehicle score with ownership/lease proof, driving license, vehicle photos, driver social security/labor proof, health certificates.
  - Personnel score with ID, labor contract, health certificate, social security.
  - Warehouse score with area thresholds, photos, ownership/lease proof.
  - Solution/service score with supply channel agreements, supplier materials, test reports, hotline contacts.
- Tender-native quotation forms:
  - Opening list with average discount/downward rate, deposit method and amount.
  - Itemized quotation table by food category, preserving units and notes.

Generalize this pattern instead of copying project-specific materials into unrelated bids.

## Output Checks

Before delivering a material package, verify:

- P0 items are visually separated from scoring and optional items.
- The client can see exactly what to fill, upload, sign, seal, and confirm.
- Every scoring item maps to a required or optional proof item.
- Every tender-native form is preserved or clearly referenced.
- Statutory/legal items are not over-labeled as rejection items unless tender or law requires pre-bid proof.
- The package avoids asking for low-value materials when time is short.
