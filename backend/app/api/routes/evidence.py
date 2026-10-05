from fastapi import APIRouter

router = APIRouter()

@router.get("/evidence", tags=["evidence"])
def list_evidence():
    return [
        { "id": "ev1", "metric": "Passing income - Option A", "value": 795200, "unit": "AUD/yr", "source": "independent_valuation.pdf", "page": 4, "evidence_class": "measured", "status": "verified" },
        { "id": "ev2", "metric": "Passing income - Option B", "value": 963900, "unit": "AUD/yr", "source": "lease_schedule_rent_roll.pdf", "page": 3, "evidence_class": "measured", "status": "verified" },
        { "id": "ev3", "metric": "Unrecovered outgoings - Option A", "value": 18560, "unit": "AUD/yr", "source": "property_manager_annual_summary.pdf", "page": 2, "evidence_class": "measured", "status": "verified" },
        { "id": "ev4", "metric": "Unrecovered outgoings - Option B", "value": 36120, "unit": "AUD/yr", "source": "property_manager_annual_summary.pdf", "page": 2, "evidence_class": "measured", "status": "verified" },
        { "id": "ev5", "metric": "Land tax - Option A", "value": 78000, "unit": "AUD/yr", "source": "portfolio_treasury_schedule.pdf", "page": 1, "evidence_class": "client stated", "status": "verified" },
        { "id": "ev6", "metric": "Land tax - Option B", "value": 96000, "unit": "AUD/yr", "source": "portfolio_treasury_schedule.pdf", "page": 1, "evidence_class": "client stated", "status": "verified" },
        { "id": "ev7", "metric": "Capex - Option A", "value": 250000, "unit": "AUD", "source": "contract_summary.pdf", "page": 8, "evidence_class": "estimate", "status": "verified" },
        { "id": "ev8", "metric": "Capex - Option B", "value": 0, "unit": "AUD", "source": "contract_summary.pdf", "page": 12, "evidence_class": "measured", "status": "verified" },
        { "id": "ev9", "metric": "Comparable rate (Eastern Creek)", "value": 2930, "unit": "AUD/sqm", "source": None, "page": None, "evidence_class": None, "status": "no source" },
        { "id": "ev10", "metric": "Outgoings recovery (lease schedule)", "value": 0.92, "unit": "ratio", "source": "lease_schedule_rent_roll.pdf", "page": 5, "evidence_class": "measured", "status": "conflict" },
        { "id": "ev11", "metric": "Outgoings recovery (PM summary)", "value": 0.88, "unit": "ratio", "source": "property_manager_annual_summary.pdf", "page": 2, "evidence_class": "measured", "status": "conflict" },
        { "id": "ev12", "metric": "Option B passing income - unsourced portion", "value": 279531, "unit": "AUD/yr", "source": None, "page": None, "evidence_class": None, "status": "coverage gap" },
        { "id": "ev13", "metric": "Bond rate (pack assumption)", "value": 0.0465, "unit": "%", "source": "investment_policy_minute.pdf", "page": 1, "evidence_class": "client stated", "status": "verified" }
    ]
