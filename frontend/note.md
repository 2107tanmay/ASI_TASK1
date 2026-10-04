# Note: Judgment Debt Prototype

**To:** Sameer Chib, ASI Intelligence  
**From:** Tanmay Gangurde  
**Date:** 1 October 2026  

## What was cut
To deliver a flawless single-path prototype within the 3-day timebox, the following were intentionally excluded from this iteration:
1. **Real LLM Extraction**: The system currently runs on fixture data and a deterministic calculation module. Real LLM extraction using OCR or PDF parsing was mocked. A real LLM should only draft the narrative behind an adapter—it must never calculate.
2. **Dynamic Traps Resolution**: While conflicts, gaps, and missing sources are successfully trapped and blocked, the interactive UI to resolve them (e.g. overriding a conflict manually) was cut to focus purely on the evidence ledger's display logic.
3. **Multi-tenancy and Auth**: Excluded as per the brief. The prototype assumes one Principal and one Analyst.
4. **Integration**: No external API or property management system integrations were built; all data comes strictly from the static drop.

## What I would build next
1. **Interactive Resolution Pipeline**: Building the Analyst UI to click a conflict row (e.g., the 92% vs 88% outgoings recovery) and enter a "Human Override" with an audit timestamp and basis, which instantly unblocks the calculation engine.
2. **LLM Citation Engine**: Integrating the LLM solely for prose drafting, strictly constrained so that every quantitative claim in its output is regex-matched against the evidence ledger. If the model hallucinates a number not in the ledger, the pipeline aborts.
3. **Vector/Bounding-Box Document Viewer**: Hooking up the "Page X" links in the ledger to open the actual PDF file side-by-side with a highlight overlay on the exact extracted figure.

## Where I would make the system refuse to answer
The system's core value is abstention over hallucination. It will rigidly refuse to answer when:
- **No Document Basis (Trap 1/4)**: A figure (like the $2,930/sqm comparable, or the M12 rezoning uplift) is manually typed into the intake narrative but cannot be found in an admissible document.
- **Unresolved Conflicts (Trap 2)**: Two documents provide different numbers for the same metric (e.g., outgoings recovery). The system will return "blocked" for the final output until a human decides.
- **Incomplete Sets (Trap 3)**: If a dataset is partially missing (e.g., 29% of leases), the system refuses to interpolate or extrapolate a "likely" total. It calculates only on the verified subset.
- **Arithmetic by Model**: The system will refuse any workflow where an LLM is asked to sum, multiply, or compound rates. All math happens in the isolated Python `calculation/engine.py` module.
