from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.system_preferences import (
    SystemPreferences,
    SystemPreferencesCreate,
    SystemPreferencesUpdate,
)


async def get_preferences(db: AsyncSession) -> Optional[SystemPreferences]:
    result = await db.exec(select(SystemPreferences).limit(1))
    return result.one_or_none()


async def create_preferences(
    db: AsyncSession, prefs_in: SystemPreferencesCreate
) -> SystemPreferences:
    existing = await get_preferences(db)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="System preferences already exist.")

    prefs = SystemPreferences(**prefs_in.model_dump())
    db.add(prefs)
    await db.commit()
    await db.refresh(prefs)
    return prefs


async def update_preferences(
    db: AsyncSession, prefs_in: SystemPreferencesUpdate
) -> Optional[SystemPreferences]:
    prefs = await get_preferences(db)
    if not prefs:
        return None

    data = prefs_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(prefs, field, value)

    prefs.touch()
    await db.commit()
    await db.refresh(prefs)
    return prefs
