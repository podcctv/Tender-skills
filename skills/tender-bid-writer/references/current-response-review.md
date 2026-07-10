# Current Response File Review

Use this reference when the user provides an existing response/bid/proposal file and asks what is missing, what is risky, what still needs to be requested from the bidder/client, or whether the current version can be submitted.

## Review Goal

Review the current response file against the tender source of truth. Separate:

- missing items that may cause rejection or invalid response;
- incomplete fields, placeholders, dates, signatures, seals, scans, or upload issues;
- evidence that appears present but still needs validity, clarity, entity, expiry, or completeness verification;
- scoring or credibility evidence that is useful but not a hard gate;
- optional polish that can be skipped if time is short.

Do not assume an embedded image is compliant just because an attachment caption exists. Mark image-only evidence as "present, needs visual/validity check" unless the content has been inspected.

## Required Inputs

1. Tender/procurement source text, forms, annexes, and clarifications.
2. Current response/proposal file, usually `.docx` or `.pdf`.
3. Extracted response text and table content.
4. Embedded media/image inventory when the file contains scanned licenses, screenshots, contracts, IDs, deposit vouchers, or certificates.

If any input is missing, state the limitation and continue with the evidence available.

## Review Procedure

1. **Classify the bid and submission mode**
   - Record bid type mode and submission mode (`electronic-bid`, `paper-bid`, or `dual-bid`).
   - Identify whether the current review is pre-submission QC, client supplement collection, or final upload check.

2. **Check required response composition**
   - Compare the tender's required response file composition against the current response file.
   - Check every official form, table, commitment letter, quotation form, performance table, certificate attachment, deposit proof, signature/seal item, and upload requirement.
   - Preserve tender-native names when reporting gaps.

3. **Check field completeness and placeholders**
   - Look for blank cells, underscores, unfilled dates, missing contact details, empty quotation fields, empty bank/account fields, missing person names, missing telephone numbers, and template remnants.
   - Treat pricing, signature/seal, authorization, deposit, qualification, and mandatory form blanks as P0 unless the tender allows omission.

4. **Check pass/fail qualifications**
   - Business license, legal subject consistency, business scope, mandatory license/permit, authorization, identity documents, credit report, deposit, similar performance contract, no-joint-bid requirement, affiliation/fair-competition restrictions, no borrowed qualification, no transfer, and no subcontracting.
   - Classify each item as `missing`, `incomplete`, `present-needs-check`, `covered`, or `not-applicable`.

5. **Check price and platform consistency**
   - Verify final quotation/discount/downward rate is filled, unique, consistent with platform quotation, and follows tender thresholds.
   - Flag obviously incomplete amount-in-words/amount-in-figures fields.
   - If price score dominates, ask for internal cost tolerance confirmation, but keep internal cost sheets out of the formal bid unless required.

6. **Check evidence validity and scan usability**
   - For images and scans, check whether the document is clear, upright, uncropped, unexpired, entity-consistent, and relevant to the tender requirement.
   - For contracts, ensure at least the cover/title page, parties, subject matter, amount or scale, term, and signature/seal pages are present.
   - For screenshots/reports, prefer official downloadable reports over screenshots when the tender asks for a report.

7. **Check financial tables**
   - Do not invent missing years or accounting data.
   - Verify unit conversion, formulas, and year coverage.
   - If the tender form has multiple years but only one year is supplied, mark the missing years as P0/P1 depending on whether the tender makes them mandatory.

8. **Check industry-specific commitments**
   - For food/canteen/ingredient distribution, check food license, staff health certificates, meat quarantine, pesticide residue testing, grain/oil/dry goods quality reports, cold-chain traceability, purchase inspection ledgers, supplier channels, vehicles, warehouse/site, emergency replenishment, and service contacts.
   - Classify legal operation evidence as `legal-baseline-confirmation` unless the tender requires pre-bid upload.

9. **Check commitment and commercial risk**
   - Flag commitments that exceed tender requirements or create broad liability, such as fixed liquidated damages, double compensation, unconditional penalties, very short response times, or all-cost indemnities.
   - Ask the client to confirm before keeping strong commercial commitments.

10. **Run deterministic checks when available**
   - Use `scripts/bid_quality_check.py` for placeholder and coverage hints.
   - Treat script output as a signal, not a substitute for tender-specific manual review.

## Output Shape

For a current response review, produce one review report by default:

`响应文件当前版本评审与补件清单.md`

If the user needs to send it to the client, also create a Word version:

`响应文件当前版本补件清单.docx`

Recommended sections:

1. Overall conclusion: can submit now or not; top 3-8 reasons.
2. P0 must-fix / must-request list: pass/fail, validity, price, signature/seal, mandatory attachments.
3. P1 scoring or delivery-confidence list: evidence that affects score, trust, or contract performance.
4. P2 optional polish list.
5. Client material request list: grouped by enterprise info, qualification, finance, performance, food safety/delivery, signature/seal/submission.
6. Direct edits to current file: fields to fill, text to revise, images to rotate/replace, dates to fix, commitments to soften/confirm.
7. Final upload checklist: PDF clarity, page order, signature/seal, platform quotation, deposit proof, file naming, and deadline.

## Priority Rules

- **P0**: mandatory response item, qualification, price, deposit, signature/seal, authorization, official form, response deadline, or scan usability that may cause rejection/invalid response.
- **P1**: scoring-critical or credibility-critical evidence, legal-operation baseline evidence, delivery capability, service contact, and incomplete but not clearly disqualifying information.
- **P2**: optional proof, polish, formatting, or supporting records that are useful but can be deferred.

## Common Current-File Findings

- Quotation/discount field left blank.
- Date fields still show "year/month/day" placeholders.
- Signatures/seals are not yet applied because the file is a working draft.
- Bidder profile table has blank contact, bank, account, personnel, or project leader fields.
- Authorization letter names the same person as both legal representative and authorized representative without clarifying who will sign.
- Credit report screenshots are present but the tender asks for a current-year official report.
- Business license or certificate scan is rotated, blurred, cropped, expired, or not entity-consistent.
- Performance table lists contracts but contract scans lack amount, term, subject, or seal pages.
- Financial table has only one year while the tender form has multiple years.
- Food safety commitments are strong but health certificates, testing samples, quarantine proof, traceability, vehicles, or ledgers are not attached.
- Commercial commitments go beyond tender requirements and need client confirmation.
