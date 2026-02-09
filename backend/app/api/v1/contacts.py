from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.contact import Contact, ContactSegment, contact_segment_association
from app.schemas.contact import (
    ContactCreate, ContactUpdate, ContactResponse,
    ContactSegmentCreate, ContactSegmentResponse,
    ContactImportResponse,
)
from app.services.contact_service import ContactImportService

router = APIRouter()


# --- Contacts ---

@router.get("/", response_model=List[ContactResponse])
async def list_contacts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contact))
    return result.scalars().all()

@router.post("/", response_model=ContactResponse, status_code=201)
async def create_contact(data: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact = Contact(**data.model_dump(), source="manual")
    db.add(contact)
    await db.flush()
    await db.refresh(contact)
    return contact

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, key, value)
    await db.flush()
    await db.refresh(contact)
    return contact

@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    await db.delete(contact)


# --- Import ---

@router.post("/import", response_model=ContactImportResponse)
async def import_contacts(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """Import contacts from CSV or Excel file. Consent is confirmed at upload."""
    content = await file.read()
    service = ContactImportService(db)

    if file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
        stats = await service.import_excel(content)
    else:
        stats = await service.import_csv(content)

    return stats


# --- Segments ---

@router.get("/segments/", response_model=List[ContactSegmentResponse])
async def list_segments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ContactSegment))
    return result.scalars().all()

@router.post("/segments/", response_model=ContactSegmentResponse, status_code=201)
async def create_segment(data: ContactSegmentCreate, db: AsyncSession = Depends(get_db)):
    segment = ContactSegment(**data.model_dump())
    db.add(segment)
    await db.flush()
    await db.refresh(segment)
    return segment

@router.get("/segments/{segment_id}", response_model=ContactSegmentResponse)
async def get_segment(segment_id: int, db: AsyncSession = Depends(get_db)):
    segment = await db.get(ContactSegment, segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    return segment

@router.post("/segments/{segment_id}/contacts/{contact_id}", status_code=201)
async def add_contact_to_segment(segment_id: int, contact_id: int, db: AsyncSession = Depends(get_db)):
    segment = await db.get(ContactSegment, segment_id)
    contact = await db.get(Contact, contact_id)
    if not segment or not contact:
        raise HTTPException(status_code=404, detail="Segment or contact not found")
    from sqlalchemy import insert
    await db.execute(insert(contact_segment_association).values(contact_id=contact_id, segment_id=segment_id))
    return {"status": "added"}

@router.delete("/segments/{segment_id}/contacts/{contact_id}", status_code=204)
async def remove_contact_from_segment(segment_id: int, contact_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import delete
    await db.execute(
        delete(contact_segment_association).where(
            contact_segment_association.c.contact_id == contact_id,
            contact_segment_association.c.segment_id == segment_id,
        )
    )
