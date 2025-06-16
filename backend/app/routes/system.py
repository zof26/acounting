from fastapi import APIRouter

router = APIRouter(prefix="/status", tags=["System"])

@router.get("/health", include_in_schema=False)
def health_check():
    return {"status": "ok"}
