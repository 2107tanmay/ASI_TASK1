from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.get("/traps")
def get_traps():
    return {
        "trap_1": {"status": "unverified, no admissible source", "rate": 2930},
        "trap_2": {"noi_92": 657640, "noi_88": 648360},
        "trap_3": {"verified_income": 684369, "total_income": 963900, "excluded": 279531},
        "trap_4": {"status": "not sourced, evidence required"}
    }

