from fastapi import APIRouter
from datetime import datetime, timezone
from app.core.config import settings
import platform
import os

router = APIRouter(prefix="/status", tags=["System"])

# Cache server start time
STARTED_AT = datetime.now(timezone.utc)

@router.get("/meta", include_in_schema=False)
def get_meta():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "started_at": STARTED_AT.isoformat(),
        "runtime": {
            "python_version": platform.python_version(),
            "system": platform.system(),
            "release": platform.release(),
        },
        "features": {
            "einvoice": settings.ENABLE_EINVOICE,
            "elster": settings.ENABLE_ELSTER,
            "banking": settings.ENABLE_BANKING,
        },
        "deployment": {
            "build_hash": os.getenv("BUILD_HASH", "unknown"),
            "build_time": os.getenv("BUILD_TIME", "unknown"),
        },
    }
