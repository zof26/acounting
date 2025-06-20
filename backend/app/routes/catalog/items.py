from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.core.security import require_roles
from app.models.enums import RoleEnum
from app.models.user import User

from app.models.item import ItemCreate, ItemUpdate, ItemRead
from app.crud.item import (
    get_items,
    get_item_by_id,
    create_item,
    update_item,
    delete_item,
)

router = APIRouter(prefix="/items", tags=["catalog"])

catalog_access = require_roles([RoleEnum.Accountant, RoleEnum.Admin])

@router.get("", response_model=List[ItemRead], summary="List items")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_session),
    _: User = Depends(catalog_access),
):
    return await get_items(db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemRead, summary="Get item by ID")
async def get_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(catalog_access),
):
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED, summary="Create new item")
async def create_new_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(catalog_access),
):
    return await create_item(db, item_in)

@router.patch("/{item_id}", response_model=ItemRead, summary="Update item")
async def patch_item(
    item_id: UUID,
    item_in: ItemUpdate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(catalog_access),
):
    item = await get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    return await update_item(db, item, item_in)

@router.delete("/{item_id}", status_code=204, summary="Delete item")
async def delete_item_entry(
    item_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(catalog_access),
):
    success = await delete_item(db, item_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
