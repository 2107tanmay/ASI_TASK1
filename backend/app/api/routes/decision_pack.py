from fastapi import APIRouter

router = APIRouter()

@router.get("/decision-pack", tags=["decision-pack"])
async def get_decision_pack():
    return {
        "status": "ok",
        "decision": "Commit AUD 14m to 19m",
        "options": ["A", "B", "C", "D"]
    }
