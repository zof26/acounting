from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.core.security import require_roles
from app.models.enums import RoleEnum
from app.models.user import User

from app.models.client import ClientCreate, ClientUpdate, ClientRead
from app.models.contact_person import ContactPersonCreate, ContactPersonUpdate, ContactPersonRead
from app.models.document_attachment import DocumentAttachmentCreate, DocumentAttachmentRead

from app.crud.client import (
    get_clients,
    get_client_by_id,
    create_client,
    update_client,
)

from app.crud.contact_person import (
    get_contacts_by_client,
    get_contact_person_by_id,
    create_contact_person,
    update_contact_person,
    delete_contact_person,
)

from app.crud.document_attachment import (
    get_attachments_by_client,
    get_attachment_by_id,
    create_attachment,
    delete_attachment,
)

router = APIRouter(prefix="/clients", tags=["clients"])

crm_required = require_roles([RoleEnum.Accountant, RoleEnum.Admin])

# --- Clients ---

@router.get("", response_model=List[ClientRead], summary="List clients")
async def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    return await get_clients(db, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientRead, summary="Get client by ID")
async def get_client(
    client_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    client = await get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED, summary="Create new client")
async def create_new_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    return await create_client(db, client_in)


@router.patch("/{client_id}", response_model=ClientRead, summary="Update client")
async def patch_client(
    client_id: UUID,
    client_in: ClientUpdate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    client = await get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Client not found")
    return await update_client(db, client, client_in)

# --- Contact Persons ---

@router.get("/{client_id}/contacts", response_model=List[ContactPersonRead], summary="List client contacts")
async def list_client_contacts(
    client_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    return await get_contacts_by_client(db, client_id)


@router.post("/{client_id}/contacts", response_model=ContactPersonRead, status_code=status.HTTP_201_CREATED, summary="Add contact to client")
async def add_contact_person(
    client_id: UUID,
    contact_in: ContactPersonCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    contact_data = contact_in.model_dump()
    contact_data["client_id"] = client_id
    return await create_contact_person(db, ContactPersonCreate(**contact_data))


@router.patch("/contacts/{contact_id}", response_model=ContactPersonRead, summary="Update contact person")
async def update_contact(
    contact_id: UUID,
    contact_in: ContactPersonUpdate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    contact = await get_contact_person_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Contact person not found")
    return await update_contact_person(db, contact, contact_in)


@router.delete("/contacts/{contact_id}", status_code=204, summary="Delete contact person")
async def delete_contact(
    contact_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    success = await delete_contact_person(db, contact_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Contact person not found")
    return None

# --- Document Attachments ---

@router.get("/{client_id}/attachments", response_model=List[DocumentAttachmentRead], summary="List client documents")
async def list_attachments(
    client_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    return await get_attachments_by_client(db, client_id)


@router.post("/{client_id}/attachments", response_model=DocumentAttachmentRead, status_code=201, summary="Add document to client")
async def add_attachment(
    client_id: UUID,
    attachment_in: DocumentAttachmentCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    attachment = DocumentAttachmentCreate(**attachment_in.model_dump())
    attachment = attachment_in.model_copy(update={"client_id": client_id})
    return await create_attachment(db, attachment)



@router.get("/attachments/{attachment_id}", response_model=DocumentAttachmentRead, summary="Get attachment by ID")
async def get_attachment(
    attachment_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    attachment = await get_attachment_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    return attachment


@router.delete("/attachments/{attachment_id}", status_code=204, summary="Delete document attachment")
async def delete_attachment_entry(
    attachment_id: UUID,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(crm_required),
):
    success = await delete_attachment(db, attachment_id)
    if not success:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    return None
