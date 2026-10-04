from fastapi import APIRouter

router = APIRouter()

@router.get("/documents", tags=["documents"])
async def get_documents():
    return []
