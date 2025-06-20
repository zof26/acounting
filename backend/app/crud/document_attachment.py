from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.document_attachment import DocumentAttachment
from app.models.document_attachment import DocumentAttachmentCreate

async def create_attachment(db: AsyncSession, attachment_in: DocumentAttachmentCreate) -> DocumentAttachment:
    attachment = DocumentAttachment(**attachment_in.model_dump())
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)
    return attachment

async def get_attachment_by_id(db: AsyncSession, attachment_id: UUID) -> Optional[DocumentAttachment]:
    result = await db.exec(select(DocumentAttachment).where(DocumentAttachment.id == attachment_id))
    return result.one_or_none()

async def get_attachments_by_client(db: AsyncSession, client_id: UUID) -> List[DocumentAttachment]:
    result = await db.exec(select(DocumentAttachment).where(DocumentAttachment.client_id == client_id))
    return list(result)

async def delete_attachment(db: AsyncSession, attachment_id: UUID) -> bool:
    attachment = await get_attachment_by_id(db, attachment_id)
    if not attachment:
        return False
    await db.delete(attachment)
    await db.commit()
    return True