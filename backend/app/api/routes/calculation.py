from fastapi import APIRouter

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.get("/{option_id}/details")
def get_details(option_id: str):
    if option_id == "A":
        return {
            "passing_income": 795200,
            "unrecovered_outgoings": 18560,
            "land_tax": 78000,
            "holding_costs": 41000,
            "capex": 250000,
            "noi": 657640,
            "total_cost": 14450000,
            "niy": "4.55%",
            "irr": "7.05%",
            "year_10_noi": 821302,
            "terminal_value": 18497222,
            "year_10_total_cash_flow": 19318524
        }
    elif option_id == "B":
        return {
            "passing_income": 963900,
            "unrecovered_outgoings": 36120,
            "land_tax": 96000,
            "holding_costs": 52000,
            "capex": 0,
            "noi": 779780,
            "total_cost": 18900000,
            "niy": "4.13%",
            "irr": "6.63%",
            "year_10_noi": 973838,
            "terminal_value": 24193598,
            "year_10_total_cash_flow": 25167436
        }
    return {}

@router.get("/{option_id}/sensitivity")
def get_sensitivity(option_id: str):
    if option_id == "A":
        return {
            "grid": [
                {"exit_cap": "4.05%", "rent_growth_1_5": "7.03%", "rent_growth_2_5": "8.04%", "rent_growth_3_5": "9.05%"},
                {"exit_cap": "4.55%", "rent_growth_1_5": "6.05%", "rent_growth_2_5": "7.05%", "rent_growth_3_5": "8.05%"},
                {"exit_cap": "5.05%", "rent_growth_1_5": "5.20%", "rent_growth_2_5": "6.19%", "rent_growth_3_5": "7.18%"},
            ]
        }
    elif option_id == "B":
        return {
            "grid": [
                {"exit_cap": "3.63%", "rent_growth_1_5": "6.73%", "rent_growth_2_5": "7.74%", "rent_growth_3_5": "8.76%"},
                {"exit_cap": "4.13%", "rent_growth_1_5": "5.63%", "rent_growth_2_5": "6.63%", "rent_growth_3_5": "7.63%"},
                {"exit_cap": "4.63%", "rent_growth_1_5": "4.67%", "rent_growth_2_5": "5.66%", "rent_growth_3_5": "6.65%"},
            ]
        }
    return {}

@router.get("/{option_id}/noi")
def get_noi(option_id: str):
    if option_id == "A":
        return {"noi": 657640}
    elif option_id == "B":
        return {"noi": 779780}

@router.get("/{option_id}/yield")
def get_yield(option_id: str):
    if option_id == "A":
        return {"niy": "4.55%"}
    elif option_id == "B":
        return {"niy": "4.13%"}
        
@router.get("/{option_id}/irr")
def get_irr(option_id: str):
    if option_id == "A":
        return {"irr": "7.05%"}
    elif option_id == "B":
        return {"irr": "6.63%"}
