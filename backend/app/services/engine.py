def compute_irr(cash_flows, guess=0.1):
    rate1 = -0.99
    rate2 = 1.0
    # binary search for IRR
    for _ in range(100):
        rate = (rate1 + rate2) / 2
        npv = sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
        if npv > 0:
            rate1 = rate
        else:
            rate2 = rate
    return rate

def calculate_metrics(price, passing_income, outgoings, land_tax, holding_costs, capex, rent_growth, exit_cap_override=None):
    noi = passing_income - outgoings - land_tax - holding_costs
    total_cost = price + capex
    niy = noi / total_cost if total_cost > 0 else 0
    
    exit_cap = exit_cap_override if exit_cap_override is not None else niy
    
    # Year 10 NOI is Year 1 NOI * (1 + rent_growth)^9
    year_10_noi = noi * ((1 + rent_growth) ** 9)
    
    # Year 11 NOI is Year 1 NOI * (1 + rent_growth)^10
    year_11_noi = noi * ((1 + rent_growth) ** 10)
    terminal_value = year_11_noi / exit_cap if exit_cap > 0 else 0
    
    year_10_cashflow = year_10_noi + terminal_value
    
    # Calculate IRR
    cash_flows = [-total_cost]
    for year in range(1, 10):
        # Year 1 is index 1, cf is noi * (1+g)^0
        # Year 9 is index 9, cf is noi * (1+g)^8
        cash_flows.append(noi * ((1 + rent_growth) ** (year - 1)))
    cash_flows.append(year_10_cashflow)
    
    irr = compute_irr(cash_flows)
    
    return {
        "noi": noi,
        "total_cost": total_cost,
        "niy": niy,
        "year_10_noi": year_10_noi,
        "terminal_value": terminal_value,
        "year_10_cashflow": year_10_cashflow,
        "irr": irr
    }

def generate_sensitivity_grid(base_exit_cap, base_rent_growth, price, passing_income, outgoings, land_tax, holding_costs, capex):
    exit_caps = [base_exit_cap - 0.005, base_exit_cap, base_exit_cap + 0.005]
    rent_growths = [base_rent_growth - 0.01, base_rent_growth, base_rent_growth + 0.01]
    
    grid = []
    for e_cap in exit_caps:
        row = {"exit_cap": f"{round(e_cap * 100, 2)}%"}
        for r_growth in rent_growths:
            metrics = calculate_metrics(price, passing_income, outgoings, land_tax, holding_costs, capex, r_growth, e_cap)
            # Find the corresponding column key based on the position
            # base - 1% -> "rent_growth_1_5" (if base is 2.5)
            # It's cleaner to just return the raw matrix, but we'll match the requested format
            col_key = f"rent_growth_{str(round(r_growth * 100, 1)).replace('.', '_')}"
            # Formatting IRR
            row[col_key] = f"{round(metrics['irr'] * 100, 2)}%"
        grid.append(row)
    
    return grid
