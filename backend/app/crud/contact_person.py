from typing import List, Optional
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.contact_person import ContactPerson
from app.models.contact_person import ContactPersonCreate, ContactPersonUpdate

async def create_contact_person(db: AsyncSession, contact_in: ContactPersonCreate) -> ContactPerson:
    contact = ContactPerson(**contact_in.model_dump())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def get_contact_person_by_id(db: AsyncSession, contact_id: UUID) -> Optional[ContactPerson]:
    result = await db.exec(select(ContactPerson).where(ContactPerson.id == contact_id))
    return result.one_or_none()

async def get_contacts_by_client(db: AsyncSession, client_id: UUID) -> List[ContactPerson]:
    result = await db.exec(select(ContactPerson).where(ContactPerson.client_id == client_id))
    return list(result)

async def update_contact_person(
    db: AsyncSession, db_contact: ContactPerson, contact_in: ContactPersonUpdate
) -> ContactPerson:
    data = contact_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_contact, field, value)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def delete_contact_person(db: AsyncSession, contact_id: UUID) -> bool:
    contact = await get_contact_person_by_id(db, contact_id)
    if not contact:
        return False
    await db.delete(contact)
    await db.commit()
    return True