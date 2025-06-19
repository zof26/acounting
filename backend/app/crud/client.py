from typing import Optional, List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.models.client import Client
from app.models.contact_person import ContactPerson
from app.models.document_attachment import DocumentAttachment

from app.schemas.client import ClientCreate, ClientUpdate
from app.schemas.contact_person import ContactPersonCreate
from app.schemas.document_attachment import DocumentAttachmentCreate

async def create_client(db: AsyncSession, client_in: ClientCreate) -> Client:
    client_data = client_in.model_dump(exclude={"contacts", "attachments"})
    client = Client(**client_data)
    db.add(client)
    await db.commit()
    await db.refresh(client)
    
    # Nested contact persons
    contacts: List[ContactPersonCreate] = getattr(client_in, "contacts", [])

    for contact in contacts:
        contact_model = ContactPerson(**contact.model_dump(), client_id=client.id)
        db.add(contact_model)

    # Nested document attachments
    attachments: List[DocumentAttachmentCreate] = getattr(client_in, "attachments", [])
    for attachment in attachments:
        attachment_model = DocumentAttachment(**attachment.model_dump(), client_id=client.id)
        db.add(attachment_model)

    await db.commit()
    await db.refresh(client)
    return client


async def get_client_by_id(db: AsyncSession, client_id: UUID) -> Optional[Client]:
    result = await db.exec(
        select(Client)
        .where(Client.id == client_id)
        .options(
            selectinload(Client.contacts),      # type: ignore[arg-type]
            selectinload(Client.attachments)    # type: ignore[arg-type]
        )
    )
    return result.one_or_none()

async def get_clients(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Client]:
    result = await db.exec(select(Client).offset(skip).limit(limit))
    return list(result)

async def update_client(db: AsyncSession, db_client: Client, client_in: ClientUpdate) -> Client:
    data = client_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_client, field, value)
    await db.commit()
    await db.refresh(db_client)
    return db_client

async def delete_client(db: AsyncSession, client_id: UUID) -> bool:
    client = await get_client_by_id(db, client_id)
    if not client:
        return False
    await db.delete(client)
    await db.commit()
    return True