from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime


# AvitoAccount
class AvitoAccountBase(BaseModel):
    name: str
    client_id: str
    client_secret: str
    is_active: bool = True

class AvitoAccountCreate(AvitoAccountBase):
    pass

class AvitoAccountUpdate(BaseModel):
    name: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    is_active: Optional[bool] = None

class AvitoAccountResponse(AvitoAccountBase):
    id: int
    access_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# AvitoAdTemplate
class AvitoAdTemplateBase(BaseModel):
    name: str
    category: Optional[str] = None
    title: str
    description: str
    price: Optional[float] = None
    images: Optional[List[str]] = None
    params: Optional[dict] = None

class AvitoAdTemplateCreate(AvitoAdTemplateBase):
    account_id: int

class AvitoAdTemplateResponse(AvitoAdTemplateBase):
    id: int
    account_id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# AvitoAd
class AvitoAdBase(BaseModel):
    title: str
    description: str
    price: Optional[float] = None
    category: Optional[str] = None
    campaign: Optional[str] = None
    images: Optional[List[str]] = None
    params: Optional[dict] = None

class AvitoAdCreate(AvitoAdBase):
    account_id: int
    template_id: Optional[int] = None

class AvitoAdUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    status: Optional[str] = None
    campaign: Optional[str] = None
    images: Optional[List[str]] = None

class AvitoAdResponse(AvitoAdBase):
    id: int
    account_id: int
    avito_id: Optional[str] = None
    template_id: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# AvitoAdStat
class AvitoAdStatResponse(BaseModel):
    id: int
    ad_id: int
    date: datetime
    views: int
    favorites: int
    contacts: int
    calls: int
    messages_count: int
    position: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)


# AvitoCompetitor
class AvitoCompetitorBase(BaseModel):
    name: str
    search_query: str
    region: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True
    check_interval_hours: int = 24

class AvitoCompetitorCreate(AvitoCompetitorBase):
    pass

class AvitoCompetitorResponse(AvitoCompetitorBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class AvitoCompetitorSnapshotResponse(BaseModel):
    id: int
    competitor_id: int
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    url: Optional[str] = None
    seller_name: Optional[str] = None
    captured_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# AvitoMessage
class AvitoMessageResponse(BaseModel):
    id: int
    account_id: int
    chat_id: str
    sender_name: Optional[str] = None
    message_text: Optional[str] = None
    direction: str
    classification: Optional[str] = None
    is_auto_replied: bool
    forwarded_to_manager: bool
    received_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# AvitoAutoReply
class AvitoAutoReplyBase(BaseModel):
    keyword: str
    reply_text: str
    is_active: bool = True
    priority: int = 0

class AvitoAutoReplyCreate(AvitoAutoReplyBase):
    pass

class AvitoAutoReplyResponse(AvitoAutoReplyBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
