# Phase 4 Final Audit Report

## 1. Option B IRR Inputs Used by Engine
* **Initial Investment (Year 0):** -$18,900,000
* **Initial NOI (Year 1):** $779,780
* **Rent Growth:** 2.5% (compounded annually on NOI)
* **Holding Period:** 10 years
* **Exit Cap Rate:** 4.55%

## 2. Exact Cash-Flow Series
The deterministic calculation engine produced the following cash-flow series for Option B:
* **Year 0:** -$18,900,000 (Acquisition Cost)
* **Year 1:** $779,780
* **Year 2:** $799,274.50
* **Year 3:** $819,256.36
* **Year 4:** $839,737.77
* **Year 5:** $860,731.22
* **Year 6:** $882,249.50
* **Year 7:** $904,305.73
* **Year 8:** $926,913.38
* **Year 9:** $950,086.21
* **Year 10:** $973,838.37 (Final operating cash flow)
* **Year 11 (Terminal):** $998,184.33 (Used exclusively for exit valuation)

## 3. Exact Terminal-Value Calculation
Terminal Value = Year 11 NOI / Exit Cap
Terminal Value = $998,184.33 / 0.0455 = **$21,938,117.09**
*Year 10 Total Cash Flow (Operating + Terminal) = $973,838.37 + $21,938,117.09 = **$22,911,955.46***

## 4. Exact IRR Convention & Formula
The calculation engine solves for the discount rate $r$ where the Net Present Value (NPV) equals exactly zero:
$$ NPV = \sum_{t=0}^{10} \frac{C_t}{(1+r)^t} = 0 $$
The calculation engine uses a deterministic Newton-Raphson implementation to solve for $r$.

## 5. Source-to-Input Mapping
* **-$18,900,000**: Directly from the assignment's explicitly stated Total Acquisition Cost for Option B.
* **$779,780**: Directly from the assignment's explicitly stated Option B NOI.
* **2.5%**: Directly from the specified base rent growth in the Option B sensitivity table.
* **4.55%**: Directly from the specified base exit cap in the Option B sensitivity table.
* **10 Years**: Directly from the documented 10-year holding convention.
* **Terminal Value (Year 11 / Exit Cap)**: Directly dictated by the explicit assignment convention.

## 6. Comparison Against Assignment Requirements
The engine correctly implements the assignment's requested standard formulas:
- The Initial Yield matches the documented expectation perfectly ($779,780 / $18,900,000 = 4.1258% vs 4.13%).
- Option A correctly hits its expected **7.05%** IRR.
- Option B hits **5.80%**, conflicting with the assignment's expected **6.63%**.

## 7. Documented Ambiguities Affecting IRR
- Trap 3 highlights a coverage gap where Passing Income was stated at $963,900, but only $684,369 was verified. However, applying these alternate figures directly into the formula yielded 8.54% and 2.64% respectively, neither of which matched the 6.63% assignment expectation. 
- The exact source or combination of inputs that derives the 6.63% expectation is undocumented.

## 8. Confirmation of Exclusivity
We confirm that absolutely NO undocumented assumptions (such as capex, unmentioned transaction costs, or mid-year cash flow discounting) are being used in the calculation engine.

## 9. Confirmation of Deterministic Result
We confirm that **5.80%** is the rigorous, purely deterministic mathematical result produced when running the documented Option B inputs through the documented standard conventions.

## 10. Confirmation of Unreproducibility
We confirm that the assignment's requested 6.63% IRR for Option B **cannot currently be reproduced without inventing an undocumented assumption**. 

---
**PHASE 4 BLOCKED — SOURCE SPECIFICATION DISCREPANCY**
