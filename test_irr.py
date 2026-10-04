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

def check(noi, passing, cost):
    cfs = [-cost]
    current_noi = noi
    current_passing = passing
    for i in range(1, 11):
        cfs.append(current_noi)
        current_noi *= 1.025
        current_passing *= 1.025
    terminal_value = current_passing / 0.0455
    cfs[10] += terminal_value
    print(f"IRR: {irr(cfs)*100:.2f}%")

check(779780, 963900, 18900000)
