"""Celery tasks for Avito operations."""

import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery_app import celery_app
from app.core.database import async_session
from app.models.avito import AvitoAd, AvitoCompetitor, AvitoAccount
from app.services.avito_service import AvitoApiService

logger = logging.getLogger(__name__)


def run_async(coro):
    """Helper to run async code in Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.avito_tasks.sync_all_stats")
def sync_all_stats():
    """Sync statistics for all active ads from Avito API."""
    run_async(_sync_all_stats())


async def _sync_all_stats():
    async with async_session() as db:
        result = await db.execute(
            select(AvitoAd).where(AvitoAd.status == "active", AvitoAd.avito_id.isnot(None))
        )
        ads = result.scalars().all()
        service = AvitoApiService(db)
        for ad in ads:
            await service.sync_ad_stats(ad)
        logger.info("Synced stats for %d ads", len(ads))


@celery_app.task(name="app.tasks.avito_tasks.check_all_competitors")
def check_all_competitors():
    """Check all active competitors for new listings."""
    run_async(_check_all_competitors())


async def _check_all_competitors():
    async with async_session() as db:
        result = await db.execute(
            select(AvitoCompetitor).where(AvitoCompetitor.is_active == True)
        )
        competitors = result.scalars().all()
        service = AvitoApiService(db)
        for competitor in competitors:
            await service.check_competitors(competitor)
        logger.info("Checked %d competitors", len(competitors))


@celery_app.task(name="app.tasks.avito_tasks.fetch_messages")
def fetch_all_messages():
    """Fetch messages for all active accounts."""
    run_async(_fetch_all_messages())


async def _fetch_all_messages():
    async with async_session() as db:
        result = await db.execute(
            select(AvitoAccount).where(AvitoAccount.is_active == True)
        )
        accounts = result.scalars().all()
        service = AvitoApiService(db)
        for account in accounts:
            messages = await service.fetch_messages(account)
            for msg in messages:
                if msg.direction == "incoming":
                    await service.process_auto_replies(account, msg)
        logger.info("Fetched messages for %d accounts", len(accounts))
