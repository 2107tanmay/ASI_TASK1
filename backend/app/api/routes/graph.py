from fastapi import APIRouter

router = APIRouter()

@router.get("/graph/{id}")
def get_graph(id: str):
    return {"nodes": [], "relationships": []}
