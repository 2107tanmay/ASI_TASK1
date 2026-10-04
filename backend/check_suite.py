import requests

def run_tests():
    base = "http://127.0.0.1:8000/api"
    
    # Check A
    a_details = requests.get(f"{base}/calculations/A/details").json()
    assert a_details["passing_income"] == 795200
    assert a_details["unrecovered_outgoings"] == 18560
    assert a_details["land_tax"] == 78000
    assert a_details["holding_costs"] == 41000
    assert a_details["capex"] == 250000
    assert a_details["noi"] == 657640
    assert a_details["total_cost"] == 14450000
    assert a_details["niy"] == "4.55%"
    assert a_details["irr"] == "7.05%"
    assert a_details["year_10_noi"] == 821302
    assert a_details["terminal_value"] == 18497222
    assert a_details["year_10_total_cash_flow"] == 19318524

    # Check B
    b_details = requests.get(f"{base}/calculations/B/details").json()
    assert b_details["passing_income"] == 963900
    assert b_details["unrecovered_outgoings"] == 36120
    assert b_details["land_tax"] == 96000
    assert b_details["holding_costs"] == 52000
    assert b_details["capex"] == 0
    assert b_details["noi"] == 779780
    assert b_details["total_cost"] == 18900000
    assert b_details["niy"] == "4.13%"
    assert b_details["irr"] == "6.63%"
    assert b_details["year_10_noi"] == 973838
    assert b_details["terminal_value"] == 24193598
    assert b_details["year_10_total_cash_flow"] == 25167436

    # Sensitivities
    a_sens = requests.get(f"{base}/calculations/A/sensitivity").json()
    assert a_sens["grid"][1]["exit_cap"] == "4.55%"
    assert a_sens["grid"][1]["rent_growth_2_5"] == "7.05%"

    b_sens = requests.get(f"{base}/calculations/B/sensitivity").json()
    assert b_sens["grid"][1]["exit_cap"] == "4.13%"
    assert b_sens["grid"][1]["rent_growth_2_5"] == "6.63%"

    # Traps
    traps = requests.get(f"{base}/traps").json()
    assert traps["trap_1"]["status"] == "unverified, no admissible source"
    assert traps["trap_2"]["noi_92"] == 657640
    assert traps["trap_2"]["noi_88"] == 648360
    assert traps["trap_3"]["verified_income"] == 684369
    assert traps["trap_4"]["status"] == "not sourced, evidence required"
    
    print("Pass")

if __name__ == "__main__":
    run_tests()
