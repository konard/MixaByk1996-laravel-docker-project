from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List, Any
from datetime import datetime


class ContactBase(BaseModel):
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None
    consent_given: bool = False

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None
    is_subscribed: Optional[bool] = None

class ContactResponse(ContactBase):
    id: int
    is_subscribed: bool
    source: Optional[str] = None
    consent_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ContactSegmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    filters: Optional[dict] = None
    is_dynamic: bool = False

class ContactSegmentCreate(ContactSegmentBase):
    pass

class ContactSegmentResponse(ContactSegmentBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ContactImportResponse(BaseModel):
    imported: int
    skipped: int
    errors: List[str]
