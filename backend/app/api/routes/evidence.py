from fastapi import APIRouter

router = APIRouter()

@router.get("/evidence", tags=["evidence"])
def list_evidence():
    return [
        {
            "id": "A-NOI-001", "label": "Net operating income", "value": 657640, "unit": "AUD/yr", "option": "A", "sourceDoc": "D4", "page": 2, "extract": "Net property income 657,640", "class": "Measured", "status": "Verified", "usedInCalc": True
        }
    ]
