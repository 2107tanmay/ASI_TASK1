from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import List, Dict
import hashlib
from datetime import datetime

# Set a reasonable precision for financial calculations
getcontext().prec = 28

# Helper to compute a deterministic hash of inputs (sorted key/value)
def compute_input_hash(data: Dict) -> str:
    """Create a SHA‑256 hash of the ordered JSON representation of *data*.
    The hash is used to guarantee reproducibility of calculation runs.
    """
    # Ensure deterministic ordering
    items = sorted(data.items())
    flat = "|".join(f"{k}:{v}" for k, v in items)
    return hashlib.sha256(flat.encode("utf-8")).hexdigest()

# Example data structures expected by the engine (values are Decimal)

def calculate_noi(passing_income: Decimal, outgoings_recovery: Decimal, land_tax: Decimal,
                  holding_costs: Decimal, capex: Decimal) -> Decimal:
    """Net Operating Income = (Passing Income * Recovery %) - Land Tax - Holding Costs - Capex.
    *outgoings_recovery* is a percentage expressed as a decimal (e.g., 0.92).
    """
    return (passing_income * outgoings_recovery) - land_tax - holding_costs - capex

def calculate_initial_yield(noi: Decimal, total_cost: Decimal) -> Decimal:
    """Net Initial Yield = NOI / Total Cost.
    Returns a decimal fraction (e.g., 0.0455 for 4.55%).
    """
    if total_cost == 0:
        raise ZeroDivisionError("Total cost cannot be zero for yield calculation")
    return noi / total_cost

def calculate_irr(cash_flows: List[Decimal], guess: Decimal = Decimal("0.1")) -> Decimal:
    """Compute the internal rate of return (IRR) using the Newton‑Raphson method.
    *cash_flows* is a list where index 0 is the initial outflow (negative) and subsequent
    entries are annual cash inflows. Returns a decimal fraction (e.g., 0.0705 for 7.05%).
    """
    # Simple deterministic implementation – limited to 30 iterations
    irr = guess
    for _ in range(30):
        npv = sum(cf / ((1 + irr) ** i) for i, cf in enumerate(cash_flows))
        d_npv = sum(-i * cf / ((1 + irr) ** (i + 1)) for i, cf in enumerate(cash_flows))
        if d_npv == 0:
            break
        new_irr = irr - npv / d_npv
        if abs(new_irr - irr) < Decimal("1e-12"):
            irr = new_irr
            break
        irr = new_irr
    return irr.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)

def calculate_terminal_value(year_11_noi: Decimal, exit_cap: Decimal) -> Decimal:
    """Terminal Value = Year 11 NOI divided by the exit cap rate.
    *exit_cap* is a decimal fraction (e.g., 0.0455 for 4.55%).
    """
    if exit_cap == 0:
        raise ZeroDivisionError("Exit cap cannot be zero for terminal value calculation")
    return year_11_noi / exit_cap

def run_sensitivity(base_inputs: Dict, rent_growth_rates: List[Decimal], exit_caps: List[Decimal]) -> Dict:
    """Execute a 3×3 sensitivity grid.
    *base_inputs* must contain the required keys for the underlying calculations:
        - passing_income
        - outgoings_recovery
        - land_tax
        - holding_costs
        - capex
        - total_cost
        - year_11_noi (or a method to derive it)
    Returns a nested dict of IRR values keyed by (rent_growth, exit_cap).
    """
    results = {}
    for rg in rent_growth_rates:
        # Adjust the passing income for rent growth (simple linear increase)
        adjusted_income = base_inputs["passing_income"] * (Decimal("1") + rg)
        for ec in exit_caps:
            # Re‑calculate NOI with the adjusted income
            noi = calculate_noi(
                passing_income=adjusted_income,
                outgoings_recovery=base_inputs["outgoings_recovery"],
                land_tax=base_inputs["land_tax"],
                holding_costs=base_inputs["holding_costs"],
                capex=base_inputs["capex"],
            )
            # Build cash‑flow list for IRR (simplified: year‑0 negative total cost,
            # years 1‑10 NOI, year 11 NOI + terminal value)
            cash_flows = [ -base_inputs["total_cost"] ]
            cash_flows.extend([noi] * 10)
            terminal = calculate_terminal_value(year_11_noi=noi, exit_cap=ec)
            cash_flows.append(noi + terminal)
            irr = calculate_irr(cash_flows)
            results.setdefault(str(rg), {})[str(ec)] = irr
    return results
