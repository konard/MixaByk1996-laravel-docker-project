from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.avito import AvitoAd, AvitoAccount
from app.models.email import EmailCampaign
from app.models.contact import Contact
from app.models.activity_log import ActivityLog

router = APIRouter()


@router.get("/")
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    """Dashboard with key metrics overview."""
    accounts_count = await db.scalar(select(func.count(AvitoAccount.id)))
    ads_count = await db.scalar(select(func.count(AvitoAd.id)))
    active_ads = await db.scalar(
        select(func.count(AvitoAd.id)).where(AvitoAd.status == "active")
    )
    contacts_count = await db.scalar(select(func.count(Contact.id)))
    subscribed_contacts = await db.scalar(
        select(func.count(Contact.id)).where(Contact.is_subscribed == True)
    )
    campaigns_count = await db.scalar(select(func.count(EmailCampaign.id)))
    sent_campaigns = await db.scalar(
        select(func.count(EmailCampaign.id)).where(EmailCampaign.status == "sent")
    )

    # Recent activity
    result = await db.execute(
        select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(10)
    )
    recent_activity = result.scalars().all()

    return {
        "avito": {
            "accounts": accounts_count or 0,
            "total_ads": ads_count or 0,
            "active_ads": active_ads or 0,
        },
        "contacts": {
            "total": contacts_count or 0,
            "subscribed": subscribed_contacts or 0,
        },
        "email": {
            "total_campaigns": campaigns_count or 0,
            "sent_campaigns": sent_campaigns or 0,
        },
        "recent_activity": [
            {
                "action": log.action,
                "entity_type": log.entity_type,
                "created_at": str(log.created_at),
            }
            for log in recent_activity
        ],
    }
