from typing import Optional, List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from collections.abc import Sequence
from app.models.item import Item, ItemCreate, ItemUpdate


async def create_item(db: AsyncSession, item_in: ItemCreate) -> Item:
    item = Item(**item_in.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_item_by_id(db: AsyncSession, item_id: UUID) -> Optional[Item]:
    result = await db.exec(
        select(Item).where(Item.id == item_id)
    )
    return result.one_or_none()


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Item]:
    result = await db.exec(
        select(Item).offset(skip).limit(limit)
    )
    return result.all()


async def update_item(db: AsyncSession, db_item: Item, item_in: ItemUpdate) -> Item:
    data = item_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_item, field, value)

    db_item.touch()
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def delete_item(db: AsyncSession, item_id: UUID) -> bool:
    item = await get_item_by_id(db, item_id)
    if not item:
        return False
    await db.delete(item)
    await db.commit()
    return True
