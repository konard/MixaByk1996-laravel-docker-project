"""Service for email campaign sending and tracking."""

import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import aiosmtplib
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.config import settings
from app.models.email import EmailCampaign, EmailTemplate, EmailCampaignLog, EmailLinkClick
from app.models.contact import Contact, ContactSegment, contact_segment_association

logger = logging.getLogger(__name__)


class EmailService:
    """Handles email template rendering, sending, and tracking."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _personalize(self, content: str, contact: Contact) -> str:
        """Replace personalization variables in content."""
        replacements = {
            "{имя}": contact.name or "",
            "{город}": contact.city or "",
            "{email}": contact.email,
            "{последние_закупки}": ", ".join(contact.purchase_history or []),
        }
        result = content
        for key, value in replacements.items():
            result = result.replace(key, value)
        return result

    def _add_tracking(self, html: str, campaign_id: int, contact_id: int) -> str:
        """Add open tracking pixel and click tracking to email HTML."""
        tracking_pixel = (
            f'<img src="{settings.AVITO_API_BASE_URL.replace("api.avito.ru", "localhost")}'
            f'/api/v1/email/track/open/{campaign_id}/{contact_id}" '
            f'width="1" height="1" style="display:none" />'
        )
        html += tracking_pixel
        return html

    def _add_unsubscribe_link(self, html: str, contact_id: int) -> str:
        """Add mandatory unsubscribe link (152-FZ / GDPR compliance)."""
        unsubscribe_url = f"/api/v1/email/unsubscribe/{contact_id}"
        unsubscribe_html = (
            f'<div style="text-align:center;margin-top:20px;font-size:12px;color:#999;">'
            f'<a href="{unsubscribe_url}">Отписаться от рассылки</a>'
            f'</div>'
        )
        html += unsubscribe_html
        return html

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """Send a single email via SMTP."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        msg["To"] = to_email

        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER or None,
                password=settings.SMTP_PASSWORD or None,
                use_tls=True if settings.SMTP_PORT == 465 else False,
                start_tls=True if settings.SMTP_PORT == 587 else False,
            )
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, e)
            return False

    async def get_segment_contacts(self, segment_id: int) -> List[Contact]:
        """Get all subscribed contacts in a segment."""
        result = await self.db.execute(
            select(Contact)
            .join(contact_segment_association)
            .where(
                contact_segment_association.c.segment_id == segment_id,
                Contact.is_subscribed == True,
                Contact.consent_given == True,
            )
        )
        return result.scalars().all()

    async def send_campaign(self, campaign: EmailCampaign) -> Dict[str, int]:
        """Send an email campaign to all contacts in the segment."""
        stats = {"sent": 0, "failed": 0}

        if not campaign.segment_id:
            logger.warning("Campaign %s has no segment", campaign.id)
            return stats

        # Get template
        template = None
        if campaign.template_id:
            template = await self.db.get(EmailTemplate, campaign.template_id)

        html_content = template.html_content if template else f"<p>{campaign.subject}</p>"
        text_content = template.text_content if template else campaign.subject

        # Get contacts
        contacts = await self.get_segment_contacts(campaign.segment_id)

        campaign.status = "sending"
        await self.db.commit()

        for i, contact in enumerate(contacts):
            # A/B testing: determine subject variant
            use_variant_b = (
                campaign.subject_b
                and i < len(contacts) * (campaign.ab_test_percentage / 100)
            )
            subject = campaign.subject_b if use_variant_b else campaign.subject
            variant = "B" if use_variant_b else "A"

            # Personalize content
            personalized_html = self._personalize(html_content, contact)
            personalized_html = self._add_tracking(personalized_html, campaign.id, contact.id)
            personalized_html = self._add_unsubscribe_link(personalized_html, contact.id)
            personalized_text = self._personalize(text_content or "", contact)

            # Send
            success = await self.send_email(
                contact.email, subject, personalized_html, personalized_text
            )

            # Log
            log = EmailCampaignLog(
                campaign_id=campaign.id,
                contact_id=contact.id,
                email=contact.email,
                subject_variant=variant,
                status="sent" if success else "failed",
            )
            self.db.add(log)

            if success:
                stats["sent"] += 1
            else:
                stats["failed"] += 1

        campaign.sent_count = stats["sent"]
        campaign.status = "sent"
        await self.db.commit()
        logger.info("Campaign %s sent: %d sent, %d failed", campaign.id, stats["sent"], stats["failed"])
        return stats

    async def track_open(self, campaign_id: int, contact_id: int) -> None:
        """Record email open event."""
        result = await self.db.execute(
            select(EmailCampaignLog).where(
                EmailCampaignLog.campaign_id == campaign_id,
                EmailCampaignLog.contact_id == contact_id,
            )
        )
        log = result.scalar_one_or_none()
        if log and not log.opened_at:
            log.opened_at = datetime.utcnow()
            log.status = "opened"
            # Update campaign open count
            campaign = await self.db.get(EmailCampaign, campaign_id)
            if campaign:
                campaign.open_count = (campaign.open_count or 0) + 1
            await self.db.commit()

    async def track_click(self, campaign_id: int, contact_id: int, url: str) -> None:
        """Record link click event."""
        result = await self.db.execute(
            select(EmailCampaignLog).where(
                EmailCampaignLog.campaign_id == campaign_id,
                EmailCampaignLog.contact_id == contact_id,
            )
        )
        log = result.scalar_one_or_none()
        if log:
            log.clicked_at = datetime.utcnow()
            log.status = "clicked"
            click = EmailLinkClick(log_id=log.id, url=url)
            self.db.add(click)
            campaign = await self.db.get(EmailCampaign, campaign_id)
            if campaign:
                campaign.click_count = (campaign.click_count or 0) + 1
            await self.db.commit()

    async def unsubscribe(self, contact_id: int) -> bool:
        """Unsubscribe a contact."""
        contact = await self.db.get(Contact, contact_id)
        if contact:
            contact.is_subscribed = False
            contact.unsubscribed_at = datetime.utcnow()
            await self.db.commit()
            return True
        return False
