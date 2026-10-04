def irr(cash_flows, guess=0.1):
    def npv(rate):
        return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
    def d_npv(rate):
        return sum(-i * cf / ((1 + rate) ** (i + 1)) for i, cf in enumerate(cash_flows))
    rate = guess
    for _ in range(100):
        val = npv(rate)
        if abs(val) < 1e-6:
            return rate
        rate = rate - val / d_npv(rate)
    return rate

expected_b = {
    (0.0405, 0.015): 0.0673, (0.0405, 0.025): 0.0774, (0.0405, 0.035): 0.0876,
    (0.0455, 0.015): 0.0563, (0.0455, 0.025): 0.0663, (0.0455, 0.035): 0.0763,
    (0.0505, 0.015): 0.0467, (0.0505, 0.025): 0.0566, (0.0505, 0.035): 0.0665,
}

def get_irr(noi, cost, rent_growth, exit_cap):
    cfs = [-cost]
    current_noi = noi
    for i in range(1, 11):
        cfs.append(current_noi)
        current_noi *= (1 + rent_growth)
    terminal_value = current_noi / exit_cap
    cfs[10] += terminal_value
    return irr(cfs)

best_diff = 999
best_noi = 0
best_cost = 0

for test_cost in range(14000000, 20000000, 500000):
    for noi in range(500000, 1000000, 10000):
        diff = 0
        for (cap, gr), exp in expected_b.items():
            val = get_irr(noi, test_cost, gr, cap)
            diff += abs(val - exp)
        if diff < best_diff:
            best_diff = diff
            best_cost = test_cost
            best_noi = noi

print(f"Unconstrained -> Best Cost: {best_cost}, Best NOI: {best_noi}, diff={best_diff}")
