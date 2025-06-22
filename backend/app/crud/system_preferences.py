from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.system_preferences import (
    SystemPreferences,
    SystemPreferencesCreate,
    SystemPreferencesUpdate,
    STATIC_ID
)

async def get_preferences(db: AsyncSession) -> Optional[SystemPreferences]:
    result = await db.exec(select(SystemPreferences))
    return result.one_or_none()

async def create_preferences(db: AsyncSession, prefs_in: SystemPreferencesCreate) -> SystemPreferences:
    existing = await get_preferences(db)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="System preferences already exist."
        )

    prefs = SystemPreferences(id=STATIC_ID, **prefs_in.model_dump())
    db.add(prefs)
    await db.commit()
    await db.refresh(prefs)
    return prefs

async def update_preferences(db: AsyncSession, prefs_in: SystemPreferencesUpdate) -> Optional[SystemPreferences]:
    prefs = await get_preferences(db)
    if not prefs:
        # Create from patch if not found
        return await create_preferences(
            db,
            SystemPreferencesCreate(**prefs_in.model_dump(exclude_unset=True))
        )
    data = prefs_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(prefs, field, value)

    prefs.touch()
    await db.commit()
    await db.refresh(prefs)
    return prefs
