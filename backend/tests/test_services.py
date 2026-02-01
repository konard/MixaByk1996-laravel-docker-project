"""Tests for service layer."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.email_service import EmailService
from app.services.contact_service import ContactImportService
from app.models.contact import Contact
from app.models.email import EmailTemplate


class TestEmailService:
    def test_personalize(self):
        db = AsyncMock()
        service = EmailService(db)
        contact = MagicMock()
        contact.name = "Иван"
        contact.city = "Москва"
        contact.email = "ivan@example.com"
        contact.purchase_history = ["Ноутбук", "Телефон"]

        result = service._personalize(
            "Привет, {имя}! Вы из {город}. Последние покупки: {последние_закупки}",
            contact,
        )
        assert "Иван" in result
        assert "Москва" in result
        assert "Ноутбук" in result

    def test_add_unsubscribe_link(self):
        db = AsyncMock()
        service = EmailService(db)
        html = "<p>Test content</p>"
        result = service._add_unsubscribe_link(html, contact_id=42)
        assert "unsubscribe/42" in result
        assert "Отписаться" in result

    def test_add_tracking(self):
        db = AsyncMock()
        service = EmailService(db)
        html = "<p>Content</p>"
        result = service._add_tracking(html, campaign_id=1, contact_id=2)
        assert "track/open/1/2" in result


class TestContactImportService:
    @pytest.mark.asyncio
    async def test_import_csv(self):
        db = AsyncMock()
        # Mock execute to return no existing contacts
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        db.execute.return_value = mock_result
        db.flush = AsyncMock()

        service = ContactImportService(db)
        csv_content = b"email,name,city\ntest@example.com,Test User,Moscow\n"
        stats = await service.import_csv(csv_content)
        assert stats["imported"] == 1
        assert stats["skipped"] == 0

    @pytest.mark.asyncio
    async def test_import_csv_missing_email(self):
        db = AsyncMock()
        service = ContactImportService(db)
        csv_content = b"name,city\nTest User,Moscow\n"
        stats = await service.import_csv(csv_content)
        assert stats["imported"] == 0
        assert stats["skipped"] == 1
