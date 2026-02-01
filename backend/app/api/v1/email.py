from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.email import EmailTemplate, EmailCampaign, EmailCampaignLog
from app.schemas.email import (
    EmailTemplateCreate, EmailTemplateUpdate, EmailTemplateResponse,
    EmailCampaignCreate, EmailCampaignUpdate, EmailCampaignResponse,
    EmailCampaignLogResponse,
)
from app.services.email_service import EmailService

router = APIRouter()


# --- Templates ---

@router.get("/templates", response_model=List[EmailTemplateResponse])
async def list_templates(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailTemplate))
    return result.scalars().all()

@router.post("/templates", response_model=EmailTemplateResponse, status_code=201)
async def create_template(data: EmailTemplateCreate, db: AsyncSession = Depends(get_db)):
    template = EmailTemplate(**data.model_dump())
    db.add(template)
    await db.flush()
    await db.refresh(template)
    return template

@router.get("/templates/{template_id}", response_model=EmailTemplateResponse)
async def get_template(template_id: int, db: AsyncSession = Depends(get_db)):
    template = await db.get(EmailTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put("/templates/{template_id}", response_model=EmailTemplateResponse)
async def update_template(template_id: int, data: EmailTemplateUpdate, db: AsyncSession = Depends(get_db)):
    template = await db.get(EmailTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(template, key, value)
    await db.flush()
    await db.refresh(template)
    return template

@router.delete("/templates/{template_id}", status_code=204)
async def delete_template(template_id: int, db: AsyncSession = Depends(get_db)):
    template = await db.get(EmailTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    await db.delete(template)

@router.get("/templates/{template_id}/preview", response_class=HTMLResponse)
async def preview_template(template_id: int, db: AsyncSession = Depends(get_db)):
    template = await db.get(EmailTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template.html_content


# --- Campaigns ---

@router.get("/campaigns", response_model=List[EmailCampaignResponse])
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailCampaign))
    return result.scalars().all()

@router.post("/campaigns", response_model=EmailCampaignResponse, status_code=201)
async def create_campaign(data: EmailCampaignCreate, db: AsyncSession = Depends(get_db)):
    campaign = EmailCampaign(**data.model_dump())
    db.add(campaign)
    await db.flush()
    await db.refresh(campaign)
    return campaign

@router.get("/campaigns/{campaign_id}", response_model=EmailCampaignResponse)
async def get_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    campaign = await db.get(EmailCampaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/campaigns/{campaign_id}", response_model=EmailCampaignResponse)
async def update_campaign(campaign_id: int, data: EmailCampaignUpdate, db: AsyncSession = Depends(get_db)):
    campaign = await db.get(EmailCampaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(campaign, key, value)
    await db.flush()
    await db.refresh(campaign)
    return campaign

@router.delete("/campaigns/{campaign_id}", status_code=204)
async def delete_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    campaign = await db.get(EmailCampaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    await db.delete(campaign)

@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    campaign = await db.get(EmailCampaign, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.status not in ("draft", "scheduled"):
        raise HTTPException(status_code=400, detail="Campaign cannot be sent in current status")
    service = EmailService(db)
    stats = await service.send_campaign(campaign)
    return {"status": "sent", **stats}

@router.get("/campaigns/{campaign_id}/logs", response_model=List[EmailCampaignLogResponse])
async def get_campaign_logs(campaign_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EmailCampaignLog).where(EmailCampaignLog.campaign_id == campaign_id)
    )
    return result.scalars().all()


# --- Tracking ---

@router.get("/track/open/{campaign_id}/{contact_id}")
async def track_open(campaign_id: int, contact_id: int, db: AsyncSession = Depends(get_db)):
    """Tracking pixel endpoint for email opens."""
    service = EmailService(db)
    await service.track_open(campaign_id, contact_id)
    # Return 1x1 transparent GIF
    gif = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
    return Response(content=gif, media_type="image/gif")

@router.get("/track/click/{campaign_id}/{contact_id}")
async def track_click(campaign_id: int, contact_id: int, url: str, db: AsyncSession = Depends(get_db)):
    """Click tracking endpoint - redirects to target URL."""
    service = EmailService(db)
    await service.track_click(campaign_id, contact_id, url)
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=url)

@router.get("/unsubscribe/{contact_id}", response_class=HTMLResponse)
async def unsubscribe(contact_id: int, db: AsyncSession = Depends(get_db)):
    """Unsubscribe endpoint (152-FZ / GDPR compliance)."""
    service = EmailService(db)
    success = await service.unsubscribe(contact_id)
    if success:
        return "<html><body><h2>Вы успешно отписались от рассылки.</h2><p>Вы больше не будете получать письма.</p></body></html>"
    raise HTTPException(status_code=404, detail="Contact not found")
