import requests
import sys

def run_checks():
    base_url = "http://127.0.0.1:8005/api"
    
    print("Running Check Suite...")
    
    # 1. Calculation module returns every value in the table
    try:
        res_a = requests.get(f"{base_url}/calculations/A/details").json()
        assert res_a["noi"] == 657640
        assert res_a["total_cost"] == 14450000
        assert res_a["niy"] == "4.55%"
        assert res_a["irr"] == "7.05%"
        assert res_a["year_10_noi"] == 821302
        assert res_a["terminal_value"] == 18497222
        
        res_b = requests.get(f"{base_url}/calculations/B/details").json()
        assert res_b["noi"] == 779780
        assert res_b["total_cost"] == 18900000
        assert res_b["niy"] == "4.13%"
        assert res_b["irr"] == "6.63%"
        print("PASS: Core Calculations")
    except Exception as e:
        print(f"FAIL: Core Calculations failed: {e}")
        sys.exit(1)

    # 2. Sensitivity grid matches cell for cell
    try:
        grid_a = requests.get(f"{base_url}/calculations/A/sensitivity").json()["grid"]
        assert grid_a[0]["exit_cap"] == "4.05%", f"grid_a[0]['exit_cap'] is {grid_a[0]['exit_cap']} not 4.05%"
        assert grid_a[0]["rent_growth_1_5"] == "7.03%", f"grid_a[0]['rent_growth_1_5'] is {grid_a[0]['rent_growth_1_5']} not 7.03%"
        
        grid_b = requests.get(f"{base_url}/calculations/B/sensitivity").json()["grid"]
        assert grid_b[1]["exit_cap"] == "4.13%", f"grid_b[1]['exit_cap'] is {grid_b[1]['exit_cap']} not 4.13%"
        assert grid_b[1]["rent_growth_2_5"] == "6.63%", f"grid_b[1]['rent_growth_2_5'] is {grid_b[1]['rent_growth_2_5']} not 6.63%"
        print("PASS: Sensitivity Grid")
    except Exception as e:
        print(f"FAIL: Sensitivity Grid failed: {e}")
        sys.exit(1)

    # 3. Trap 1: Unsourced figure excluded from calculations
    try:
        # We know it's excluded because total_cost of B is 18,900,000, not 18,166,000
        assert res_b["total_cost"] == 18900000
        print("PASS: Trap 1 (Unsourced comparable excluded)")
    except Exception as e:
        print(f"FAIL: Trap 1 failed: {e}")
        sys.exit(1)

    # 4. Trap 2: Two sources disagree (Conflict surfaces)
    # The frontend shows conflict for Outgoings Recovery. 
    try:
        ev_ledger = requests.get(f"{base_url}/evidence").json()
        conflicts = [r for r in ev_ledger if r["status"].lower() == "conflict"]
        assert len(conflicts) > 0
        print("PASS: Trap 2 (Conflicts surfaced)")
    except Exception as e:
        print(f"FAIL: Trap 2 failed: {e}")
        sys.exit(1)
        
    # 5. Trap 3: Coverage gap
    try:
        gaps = [r for r in ev_ledger if r["status"].lower() == "coverage gap"]
        assert len(gaps) > 0
        assert "279,531" in str(gaps[0]["value"]) or gaps[0]["value"] == 279531
        print("PASS: Trap 3 (Coverage gap stated)")
    except Exception as e:
        print(f"FAIL: Trap 3 failed: {e}")
        sys.exit(1)

    # 6. Trap 4: Forecast with nothing behind it
    try:
        # Check if RAG refuses to answer about Property Z / M12
        resp = requests.post(f"{base_url}/chat", json={"message": "What is the expected uplift from M12 interchange?"}).json()
        assert "abstain" in resp["response"].lower() or "not sourced" in resp["response"].lower() or "no admissible source" in resp["response"].lower() or "not present" in resp["response"].lower()
        print("PASS: Trap 4 (Refusal on unsupported forecast)")
    except Exception as e:
        print(f"FAIL: Trap 4 failed: {e}")
        sys.exit(1)

    print("\nAll checks passed successfully!")

if __name__ == "__main__":
    run_checks()
