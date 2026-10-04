# Phase 4 Reconciliation Report

## 1. Inputs used in the current Option B IRR calculation
- **Initial Investment (Year 0)**: -$18,900,000 (Acquisition Cost)
- **Annual Cash Flow (NOI, Year 1-10)**: $779,780 in Year 1, compounding annually at 2.5% rent growth.
- **Exit Cap Rate**: 4.55%
- **Terminal Value**: Year 11 NOI / 4.55%
- **Mathematical Output**: 5.80%

## 2. Inputs/conventions specified by the assignment for Option B
- **Option B NOI**: $779,780
- **Total Acquisition Cost**: $18,900,000
- **Option B Passing Income**: $963,900 (Verified: $684,369, Unsupported: $279,531, Coverage gap strictly enforced)
- **Base Rent Growth**: 2.5%
- **Base Exit Cap**: 4.55%
- **Expected Initial Yield**: ≈ 4.13%
- **Expected IRR**: ≈ 6.63%

## 3. Field-by-Field Comparison & Sensitivity Brute Force
- The Initial Yield math strictly confirms the relationship between Cost and NOI: `$779,780 / $18,900,000 = 4.1258%` (≈ 4.13%).
- However, inserting these exact numbers into the stipulated 10-year holding formula yields exactly **5.80%**.
- We conducted a forensic brute-force calculation to find what numbers *would* generate the assignment's requested 6.63% sensitivity matrix:
  - If we hold Cost at $18.9M, it would require a Year 1 NOI of **~$832,330**.
  - If we hold NOI at $779,780, it would require an Acquisition Cost of **~$17,706,773**.
- Neither of those numbers are specified in the documented fixtures or instructions.
- We also tested alternative treatments (e.g. running the IRR purely on the $963,900 Passing Income without outgoings deduction), but this yielded **8.54%**.

## 4. Determination
We have exhaustively verified that the current Phase 4 implementation correctly implements the provided formulas. We have NOT omitted any documented cash-flow component, capex, holding cost, or lease assumption from the prompt. 

6.63% is not reproducible from the currently documented inputs/convention; further source clarification is required.

---
**FINAL STATUS: PHASE 4 BLOCKED — SOURCE SPECIFICATION DISCREPANCY**
