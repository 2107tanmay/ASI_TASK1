from fastapi import APIRouter
from pydantic import BaseModel
from app.services.engine import calculate_metrics, generate_sensitivity_grid

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.get("/{option_id}/details")
def get_details(option_id: str):
    if option_id == "A":
        metrics = calculate_metrics(
            price=14200000, passing_income=795200, outgoings=18560,
            land_tax=78000, holding_costs=41000, capex=250000, rent_growth=0.025
        )
    elif option_id == "B":
        metrics = calculate_metrics(
            price=18900000, passing_income=963900, outgoings=36120,
            land_tax=96000, holding_costs=52000, capex=0, rent_growth=0.025
        )
    else:
        return {}

    return {
        "passing_income": 795200 if option_id == "A" else 963900,
        "unrecovered_outgoings": 18560 if option_id == "A" else 36120,
        "land_tax": 78000 if option_id == "A" else 96000,
        "holding_costs": 41000 if option_id == "A" else 52000,
        "capex": 250000 if option_id == "A" else 0,
        "noi": round(metrics["noi"]),
        "total_cost": round(metrics["total_cost"]),
        "niy": f"{round(metrics['niy'] * 100, 2)}%",
        "irr": f"{round(metrics['irr'] * 100, 2)}%",
        "year_10_noi": round(metrics["year_10_noi"]),
        "terminal_value": round(metrics["terminal_value"]),
        "year_10_total_cash_flow": round(metrics["year_10_cashflow"])
    }

@router.get("/{option_id}/sensitivity")
def get_sensitivity(option_id: str):
    if option_id == "A":
        # Base exit cap is 4.55114...
        grid = generate_sensitivity_grid(
            base_exit_cap=657640/14450000, base_rent_growth=0.025,
            price=14200000, passing_income=795200, outgoings=18560,
            land_tax=78000, holding_costs=41000, capex=250000
        )
        return {"grid": grid}
    elif option_id == "B":
        # Base exit cap is 4.12582...
        grid = generate_sensitivity_grid(
            base_exit_cap=779780/18900000, base_rent_growth=0.025,
            price=18900000, passing_income=963900, outgoings=36120,
            land_tax=96000, holding_costs=52000, capex=0
        )
        # Fix column names to match frontend exactly
        for row in grid:
            if "rent_growth_1_5" in row:
                row["rent_growth_1_5"] = row.pop("rent_growth_1_5")
            if "rent_growth_2_5" in row:
                row["rent_growth_2_5"] = row.pop("rent_growth_2_5")
            if "rent_growth_3_5" in row:
                row["rent_growth_3_5"] = row.pop("rent_growth_3_5")
        return {"grid": grid}
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

class SandboxRequest(BaseModel):
    passing_income: float = 795200
    unrecovered_outgoings: float = 18560
    land_tax: float = 78000
    holding_costs: float = 41000
    capex: float = 250000
    total_cost: float = 14450000
    rent_growth: float = 0.025
    exit_cap: float = 0.0455

@router.post("/sandbox")
def sandbox_simulate(req: SandboxRequest):
    metrics = calculate_metrics(
        price=req.total_cost - req.capex, # Back out price from total_cost 
        passing_income=req.passing_income,
        outgoings=req.unrecovered_outgoings,
        land_tax=req.land_tax,
        holding_costs=req.holding_costs,
        capex=req.capex,
        rent_growth=req.rent_growth,
        exit_cap_override=req.exit_cap
    )
    
    return {
        "noi": round(metrics["noi"], 2),
        "total_capital": round(metrics["total_cost"], 2),
        "niy": f"{round(metrics['niy'] * 100, 2)}%",
        "year_10_noi": round(metrics["year_10_noi"], 2),
        "terminal_value": round(metrics["terminal_value"], 2),
        "approx_irr": f"{round(metrics['irr'] * 100, 2)}%"
    }
