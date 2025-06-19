from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.core.security import require_roles
from app.models.enums import RoleEnum
from app.models.user import User
from app.schemas.client import ClientRead, ClientCreate, ClientUpdate
from app.crud.client import (
    get_clients,
    get_client_by_id,
    create_client,
    update_client,
    delete_client,
)

router = APIRouter(prefix="/admin/clients", tags=["admin"])

admin_required = require_roles([RoleEnum.Admin])

@router.get("", response_model=List[ClientRead], summary="List all clients")
async def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    return await get_clients(db, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientRead, summary="Get client by ID")
async def get_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    client = await get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED, summary="Create new client")
async def create_new_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    return await create_client(db, client_in)


@router.patch("/{client_id}", response_model=ClientRead, summary="Update client fields")
async def patch_client(
    client_id: UUID,
    client_in: ClientUpdate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    client = await get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Client not found")

    return await update_client(db, client, client_in)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete client")
async def delete_client_by_admin(
    client_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required),
):
    deleted = await delete_client(db, client_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Client not found")
    return None
