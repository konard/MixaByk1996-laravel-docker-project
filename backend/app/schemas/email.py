from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    html_content: str
    text_content: Optional[str] = None
    variables: Optional[List[str]] = None

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    variables: Optional[List[str]] = None

class EmailTemplateResponse(EmailTemplateBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class EmailCampaignBase(BaseModel):
    name: str
    template_id: Optional[int] = None
    segment_id: Optional[int] = None
    subject: str
    subject_b: Optional[str] = None
    ab_test_percentage: int = 50
    scheduled_at: Optional[datetime] = None
    recurrence: Optional[str] = None

class EmailCampaignCreate(EmailCampaignBase):
    pass

class EmailCampaignUpdate(BaseModel):
    name: Optional[str] = None
    template_id: Optional[int] = None
    segment_id: Optional[int] = None
    subject: Optional[str] = None
    subject_b: Optional[str] = None
    ab_test_percentage: Optional[int] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    recurrence: Optional[str] = None

class EmailCampaignResponse(EmailCampaignBase):
    id: int
    status: str
    sent_count: int
    open_count: int
    click_count: int
    unsubscribe_count: int
    bounce_count: int
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class EmailCampaignLogResponse(BaseModel):
    id: int
    campaign_id: int
    contact_id: Optional[int] = None
    email: str
    subject_variant: str
    status: str
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
