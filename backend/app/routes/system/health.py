from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session
from app.db.session import get_session

router = APIRouter(prefix="/status", tags=["System"])

@router.get("/health", include_in_schema=False)
def health_check():
    return {"status": "ok"}

@router.get("/db", include_in_schema=False)
def db_health(session: Session = Depends(get_session)):
    try:
        session.connection().execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception as e:
        return {"database": "unreachable", "error": str(e)}
