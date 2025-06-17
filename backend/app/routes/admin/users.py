from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.core.security import require_roles
from app.models.enums import RoleEnum
from app.models.user import User
from app.schemas.user import UserRead, UserCreate, UserAdminUpdate
from app.crud.user import (
    create_user,
    get_user_by_id,
    get_users,
    update_user_admin,
    delete_user,
    get_user_by_email
)

router = APIRouter(prefix="/admin/users", tags=["admin"])

admin_required = require_roles([RoleEnum.Admin])

@router.get("", response_model=List[UserRead], summary="List all users")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required)
):
    return await get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead, summary="Get user by ID")
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required)
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Create a new user")
async def create_user_admin(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required)
):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    return await create_user(db, user_in)

@router.patch("/{user_id}", response_model=UserRead, summary="Update user fields (admin only)")
async def update_user_by_admin(
    user_id: UUID,
    user_in: UserAdminUpdate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required)
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    return await update_user_admin(db, user, user_in)

@router.delete("/{user_id}", status_code=204, summary="Delete user")
async def delete_user_by_admin(
    user_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(admin_required)
):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return None