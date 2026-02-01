"""Celery tasks for email campaign operations."""

import asyncio
import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery_app import celery_app
from app.core.database import async_session
from app.models.email import EmailCampaign
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


def run_async(coro):
    """Helper to run async code in Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.email_tasks.send_scheduled_campaigns")
def send_scheduled_campaigns():
    """Check for scheduled campaigns ready to send."""
    run_async(_send_scheduled_campaigns())


async def _send_scheduled_campaigns():
    async with async_session() as db:
        now = datetime.utcnow()
        result = await db.execute(
            select(EmailCampaign).where(
                EmailCampaign.status == "scheduled",
                EmailCampaign.scheduled_at <= now,
            )
        )
        campaigns = result.scalars().all()
        service = EmailService(db)
        for campaign in campaigns:
            await service.send_campaign(campaign)
        logger.info("Processed %d scheduled campaigns", len(campaigns))


@celery_app.task(name="app.tasks.email_tasks.send_campaign")
def send_campaign_task(campaign_id: int):
    """Send a specific campaign (used for manual sends)."""
    run_async(_send_single_campaign(campaign_id))


async def _send_single_campaign(campaign_id: int):
    async with async_session() as db:
        campaign = await db.get(EmailCampaign, campaign_id)
        if campaign:
            service = EmailService(db)
            await service.send_campaign(campaign)
