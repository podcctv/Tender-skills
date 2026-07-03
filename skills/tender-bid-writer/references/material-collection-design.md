# Outsourced Material Package Design

Use this reference when a bid is outsourced/commissioned and the first task is to audit the tender, ask the client for materials, and prepare the writer to draft later. The first round should produce two files only unless the user asks for more:

1. `资料清单（项目名称）.docx` — client-facing Word document.
2. `标书组织说明（项目名称）.md` — writer-facing Markdown document.

The Word document is the master communication artifact. It should feel like a practical client handoff document, not a pile of internal matrices. The Markdown file keeps the dense audit logic, scoring mapping, and drafting plan for the writer.

## Research Baseline

Different bid types need different material packages:

- Food / ingredient / canteen distribution: food operation legality, staff health, supplier channels, traceability, testing, cold chain, vehicles, warehouse, insurance, quality labels, emergency delivery, and quotation/discount forms.
- Standard goods: brand/model/specification, brochures, official screenshots, test reports, certificates, manufacturer authorization if required, warranty, delivery, installation, training, parameter response, and deviation control.
- Software / platform: requirement understanding, architecture, function matrix, screenshots/demo, data/interface/security, implementation team, project cases, testing/acceptance, training, operation support, and software copyrights only when required or scored.
- Service / outsourcing: staff roster, labor relationship, certificates, SLA/KPI, service workflow, tools, reports, escalation, continuity, transition, training, and assessment records.
- Hybrid goods + software: split product evidence, platform/function evidence, and integration delivery evidence.
- Construction-like bids: construction qualifications, safety production, personnel certificates, construction organization, schedule, quality/safety controls, machinery, and similar projects; use a construction-specific workflow if construction methods dominate.

Do not ask every client for every possible material. Start with the tender's own qualification, scoring, format, and submission requirements, then add only the bid-type increments that are justified.

## Client-Facing Word Structure

For outsourced bids, especially food/ingredient distribution projects, structure `资料清单（项目名称）.docx` like this:

1. **封面与紧急提醒**
   - Project name, package number if any, purchaser/agency if useful, response deadline, material return deadline, and contact route.
   - A short "本轮请优先处理" box listing P0 pass/fail items, signature/seal/upload risks, and pricing/discount confirmations.

2. **使用说明**
   - Explain how the client should fill, scan, name, and return materials.
   - Define `P0 必须提供/确认`, `P1 影响评分`, `P2 有则提供`, and `可暂缓/无需提供`.
   - State that final pass/fail classification follows the current tender document, not historical templates.

3. **一、必须提供或必须确认的资料**
   - Put qualification, mandatory format, rejection items, bid validity, no-deviation, authorization, deposit/payment, platform account, and signature/seal requirements here.
   - Use client language such as "必须提供，否则可能废标/无效响应" only where supported by tender clauses.
   - Recommended columns: `序号`, `资料/确认项`, `客户需提供或填写内容`, `对应招标条款/文件位置`, `优先级及缺失后果`, `格式/签章要求`, `备注`.

4. **二、评分项对应资料清单**
   - Map every scoring item to the exact material needed.
   - Include supplementary proof suggestions only when they improve authenticity or score confidence.
   - Recommended columns: `评分项`, `分值`, `评分要求摘要`, `需提供资料`, `建议补充证明`, `缺失影响`, `当前状态`.

5. **三、行业专项资料清单**
   - Add only the section that matches the current bid type.
   - For food/ingredient distribution, use the template below.
   - For other industries, use a shorter "专项资料待模板化" section and list only tender-justified increments until a dedicated template exists.

6. **四、客户需填写的基础信息与确认表**
   - Include form-like Word tables for bidder basic information, contact persons, invoicing/bank data, platform operation, online payment/B2B ability, quotation/discount confirmation, bid validity/no deviation, affiliation/fair competition, and no borrowed qualification/no subcontracting/no transfer.
   - These tables are designed for client completion, not for internal audit.

7. **五、招标文件原生表格及填报项**
   - Reproduce the tender's official response forms, quotation forms, performance tables, personnel/vehicle/warehouse tables, parameter response tables, commitment letters, and deviation tables when available.
   - If the tender source is Word/DOCX, use Word-native tables and preserve titles, order, merged cells, blank fields, units, notes, and signature/seal locations as much as practical.

8. **六、可暂缓或有则提供的补充资料**
   - Separate optional materials from P0/P1 items so the client does not waste time.
   - Explain the impact: "不影响资格，但可能影响文本饱满度/可信度/得分把握".

9. **七、回传清单与下一步**
   - Give a concise return checklist, file naming examples, deadline, second-round review process, and what will happen after materials return.
   - Include a "仍需确认的问题" table if some tender clauses are ambiguous.

## Food / Ingredient Distribution Template

Use this as the first mature industry template for canteen, food, grain/oil, fresh produce, staple/non-staple food, and ingredient distribution bids.

### P0 / Compliance And Mandatory Materials

Request only when required by the tender or needed to confirm lawful performance:

- Business license and scope matching food/supply/distribution.
- Food business license, food production license, prepackaged food filing, or equivalent, according to the tender and actual business.
- Legal representative identity, authorization letter, authorized representative identity, and authorized representative social security where required.
- Government procurement eligibility statements, credit report/screenshots, tax/social security proof, financial/audit proof, good-faith declaration, and no-major-illegal-record statement when required.
- Bid deposit/payment proof, payment account, B2B/online banking ability, platform registration/upload/operator confirmation.
- Bid validity, no-deviation/no-additional-condition confirmation, contract clause acceptance.
- Affiliation/fair competition confirmation: no interest relationship affecting fairness; no same legal representative/person in charge, controlling, or management relationship with other bidders where prohibited.
- No borrowed qualification, no transfer, no subcontracting/subcontracting boundary confirmation where prohibited.
- Signature/seal requirements for paper, electronic, or dual submission.

### Food Safety And Traceability Evidence

Request as P0 if the tender requires upload; otherwise classify as P1 or legal-baseline confirmation:

- Supplier/channel list, cooperative supplier agreements, source traceability explanation.
- Meat quarantine certificates or sample quarantine materials.
- Fruit/vegetable pesticide residue test reports or sample testing records.
- Grain/oil/dry goods quality inspection reports.
- Frozen product cold-chain traceability, cold-chain vehicle/equipment proof where applicable.
- Food safety insurance policy and invoice if scored or required.
- Food inspector/quality controller certificates, social security, labor relationship proof.
- Food testing equipment invoices/photos/calibration or use records if scored.
- Non-GMO commitment or proof for edible oil when the tender requires it.
- Package/label photos showing SC/QS, manufacturer, production date, shelf life, remaining shelf-life compliance, specification, and batch.

### Delivery Capability Evidence

- Vehicle list, driving licenses, ownership/lease contracts, vehicle photos, refrigerated/insulated vehicle proof when relevant.
- Driver/delivery staff list, identity documents, labor contracts or social security, health certificates for food-contact staff.
- Warehouse/site proof, ownership/lease contract, area proof, photos, temperature/humidity/cold storage evidence if scored.
- Emergency replenishment, temporary extra delivery, holiday/night delivery, unlisted ingredients, and canteen consumables supply capability.
- Delivery service contacts, hotline, escalation contact, and response time confirmation.

### Performance And Service Evidence

- Similar performance contracts matching the tender's period, object, amount, purchaser type, and service content.
- Award notices, invoices, acceptance forms, delivery records, settlement records, customer evaluations, or long-term supply certificates as authenticity support.
- Service plans or素材 from client: organization, procurement control, acceptance at delivery, return/replacement, complaint handling, food safety incident response, informationized delivery, anti-corruption/廉政 controls if scored.

### Quotation And Pricing Confirmation

- Final discount/downward rate, unit-price basis, category quotation, whether only one quotation is allowed, and internal cost tolerance.
- Confirm tax rate/invoice type, delivery cost, loss rate, emergency delivery cost, platform fee, deposit, and payment cycle.
- Keep internal cost sheets in the Markdown file unless the tender requires submission.

## Internal Markdown Structure

Create `标书组织说明（项目名称）.md` for the writer. Recommended order:

1. Project snapshot: name, package, purchaser, budget, submission deadline, bid type mode, submission mode.
2. Bid/no-bid risk summary: rejection items, qualification gaps, impossible commitments, deadline risks.
3. Requirement extraction: qualification, scoring, technical/service, business/contract, format/submission.
4. Scoring-response map: scoring language, score value, response strategy, evidence needed, target chapter, current status.
5. Mandatory-response map: clause, source location, response method, evidence/material, consequence, owner.
6. Proposal framework: table of contents, chapter goals, page budget, evidence dependencies.
7. Drafting boundaries: claims allowed now, claims blocked until evidence arrives, items that need client confirmation.
8. Material receipt tracker: received, usable, incomplete, expired, inconsistent, still missing.
9. Questions and next actions: client questions, purchaser clarification questions, second-round update plan.

## Output Checks

Before delivering the first round:

- There are exactly two default files: one Word client document and one internal Markdown file.
- The Word document can be sent directly to the client without exposing internal draft notes or unsupported claims.
- P0 items are visually separated from scoring and optional items.
- Every scoring item maps to a material request or a conscious "no material needed" explanation.
- Every tender-native form is preserved, recreated, or clearly listed as missing/unreadable.
- Statutory/legal baseline items are not mislabeled as rejection items unless the tender or law requires pre-bid proof.
- Electronic/paper/dual submission differences are explicit.
- Food distribution bids include license, health, supplier, traceability, testing, vehicle, warehouse, quotation, and emergency delivery checks where applicable.
