from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.core.security import require_roles
from app.models.enums import RoleEnum
from app.models.user import User

from app.models.system_preferences import (
    SystemPreferencesRead,
    SystemPreferencesCreate,
    SystemPreferencesUpdate,
)
from app.crud.system_preferences import (
    get_preferences,
    create_preferences,
    update_preferences,
)

router = APIRouter(prefix="/admin/preferences", tags=["admin"])

admin_required = require_roles([RoleEnum.Admin])


@router.get("", response_model=SystemPreferencesRead, summary="Get system preferences")
async def read_preferences(
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    prefs = await get_preferences(db)
    if not prefs:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Preferences not found")
    return prefs


@router.post(
    "", response_model=SystemPreferencesRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create system preferences",
)
async def create_system_preferences(
    prefs_in: SystemPreferencesCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    return await create_preferences(db, prefs_in)


@router.patch(
    "", response_model=SystemPreferencesRead,
    summary="Update system preferences",
)
async def update_system_preferences(
    prefs_in: SystemPreferencesUpdate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    prefs = await update_preferences(db, prefs_in)
    return prefs
