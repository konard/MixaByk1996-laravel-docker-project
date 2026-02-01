"""Service for interacting with Avito API."""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.avito import (
    AvitoAccount, AvitoAd, AvitoAdStat,
    AvitoCompetitor, AvitoCompetitorSnapshot,
    AvitoMessage, AvitoAutoReply,
)

logger = logging.getLogger(__name__)


class AvitoApiService:
    """Client for the official Avito API."""

    BASE_URL = settings.AVITO_API_BASE_URL

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_token(self, account: AvitoAccount) -> str:
        """Get or refresh OAuth2 token for the account."""
        if account.access_token and account.token_expires_at and account.token_expires_at > datetime.utcnow():
            return account.access_token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": account.client_id,
                    "client_secret": account.client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()

        account.access_token = data["access_token"]
        account.token_expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600))
        await self.db.commit()
        logger.info("Refreshed token for account %s", account.name)
        return account.access_token

    async def _request(self, account: AvitoAccount, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Avito API."""
        token = await self._get_token(account)
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.BASE_URL}{path}",
                headers={"Authorization": f"Bearer {token}"},
                **kwargs,
            )
            response.raise_for_status()
            return response.json()

    # --- Ad management ---

    async def publish_ad(self, ad: AvitoAd) -> Dict[str, Any]:
        """Publish an ad to Avito."""
        account = await self.db.get(AvitoAccount, ad.account_id)
        payload = {
            "title": ad.title,
            "description": ad.description,
            "price": ad.price,
            "category": ad.category,
            "images": ad.images or [],
            **(ad.params or {}),
        }
        result = await self._request(account, "POST", "/core/v1/items", json=payload)
        ad.avito_id = str(result.get("id"))
        ad.status = "active"
        await self.db.commit()
        logger.info("Published ad %s on Avito, avito_id=%s", ad.id, ad.avito_id)
        return result

    async def update_ad(self, ad: AvitoAd) -> Dict[str, Any]:
        """Update an existing ad on Avito."""
        account = await self.db.get(AvitoAccount, ad.account_id)
        payload = {
            "title": ad.title,
            "description": ad.description,
            "price": ad.price,
        }
        result = await self._request(account, "PUT", f"/core/v1/items/{ad.avito_id}", json=payload)
        logger.info("Updated ad %s on Avito", ad.avito_id)
        return result

    async def unpublish_ad(self, ad: AvitoAd) -> Dict[str, Any]:
        """Remove ad from publication on Avito."""
        account = await self.db.get(AvitoAccount, ad.account_id)
        result = await self._request(account, "POST", f"/core/v1/items/{ad.avito_id}/hide")
        ad.status = "archived"
        await self.db.commit()
        logger.info("Unpublished ad %s from Avito", ad.avito_id)
        return result

    # --- Stats ---

    async def sync_ad_stats(self, ad: AvitoAd) -> Optional[AvitoAdStat]:
        """Fetch and save latest stats for an ad from Avito API."""
        if not ad.avito_id:
            return None
        account = await self.db.get(AvitoAccount, ad.account_id)
        try:
            data = await self._request(account, "GET", f"/core/v1/items/{ad.avito_id}/stats")
            stat = AvitoAdStat(
                ad_id=ad.id,
                date=datetime.utcnow(),
                views=data.get("views", 0),
                favorites=data.get("favorites", 0),
                contacts=data.get("contacts", 0),
                calls=data.get("calls", 0),
                messages_count=data.get("messages", 0),
            )
            self.db.add(stat)
            await self.db.commit()
            return stat
        except httpx.HTTPError as e:
            logger.error("Failed to sync stats for ad %s: %s", ad.avito_id, e)
            return None

    # --- Competitor monitoring ---

    async def check_competitors(self, competitor: AvitoCompetitor) -> List[AvitoCompetitorSnapshot]:
        """Search Avito for competitor ads and save snapshots."""
        snapshots = []
        try:
            params = {"query": competitor.search_query}
            if competitor.region:
                params["region"] = competitor.region
            if competitor.category:
                params["category"] = competitor.category

            # Use search endpoint (simplified)
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/core/v1/items",
                    params=params,
                )
                if response.status_code == 200:
                    items = response.json().get("items", [])
                    for item in items[:20]:  # limit to top 20
                        snapshot = AvitoCompetitorSnapshot(
                            competitor_id=competitor.id,
                            title=item.get("title"),
                            price=item.get("price"),
                            description=item.get("description"),
                            url=item.get("url"),
                            seller_name=item.get("seller", {}).get("name"),
                        )
                        self.db.add(snapshot)
                        snapshots.append(snapshot)
                    await self.db.commit()
        except Exception as e:
            logger.error("Failed to check competitors for %s: %s", competitor.name, e)
        return snapshots

    # --- Messages ---

    async def fetch_messages(self, account: AvitoAccount) -> List[AvitoMessage]:
        """Fetch new messages from Avito chat API."""
        messages = []
        try:
            data = await self._request(account, "GET", "/messenger/v2/accounts/chats")
            for chat in data.get("chats", []):
                chat_id = chat.get("id")
                msgs_data = await self._request(account, "GET", f"/messenger/v2/accounts/chats/{chat_id}/messages")
                for msg in msgs_data.get("messages", []):
                    message = AvitoMessage(
                        account_id=account.id,
                        chat_id=str(chat_id),
                        sender_name=msg.get("author", {}).get("name"),
                        message_text=msg.get("content", {}).get("text"),
                        direction="incoming" if msg.get("direction") == "in" else "outgoing",
                    )
                    self.db.add(message)
                    messages.append(message)
            await self.db.commit()
        except Exception as e:
            logger.error("Failed to fetch messages for account %s: %s", account.name, e)
        return messages

    async def process_auto_replies(self, account: AvitoAccount, message: AvitoMessage) -> bool:
        """Check message against auto-reply rules and send reply if matched."""
        if not message.message_text:
            return False

        result = await self.db.execute(
            select(AvitoAutoReply)
            .where(AvitoAutoReply.is_active == True)
            .order_by(AvitoAutoReply.priority.desc())
        )
        rules = result.scalars().all()

        text_lower = message.message_text.lower()
        for rule in rules:
            if rule.keyword.lower() in text_lower:
                try:
                    await self._request(
                        account, "POST",
                        f"/messenger/v2/accounts/chats/{message.chat_id}/messages",
                        json={"message": {"text": rule.reply_text}},
                    )
                    message.is_auto_replied = True
                    await self.db.commit()
                    logger.info("Auto-replied to message %s with rule %s", message.id, rule.id)
                    return True
                except Exception as e:
                    logger.error("Failed to auto-reply: %s", e)
        return False
