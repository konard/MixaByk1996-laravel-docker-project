"""Tests for database models."""

import pytest
from app.models.avito import AvitoAccount, AvitoAd, AvitoAdStat, AvitoCompetitor, AvitoAutoReply
from app.models.email import EmailTemplate, EmailCampaign, EmailCampaignLog
from app.models.contact import Contact, ContactSegment
from app.models.activity_log import ActivityLog


class TestAvitoModels:
    def test_avito_account_creation(self):
        account = AvitoAccount(
            name="Test Account",
            client_id="test_client_id",
            client_secret="test_secret",
            is_active=True,
        )
        assert account.name == "Test Account"
        assert account.client_id == "test_client_id"
        assert account.is_active is True

    def test_avito_ad_creation(self):
        ad = AvitoAd(
            title="Test Ad",
            description="Test description",
            price=1000.0,
            category="electronics",
            status="draft",
        )
        assert ad.title == "Test Ad"
        assert ad.price == 1000.0
        assert ad.status == "draft"

    def test_avito_ad_stat_creation(self):
        stat = AvitoAdStat(
            ad_id=1,
            views=100,
            favorites=10,
            contacts=5,
            calls=3,
            messages_count=7,
        )
        assert stat.views == 100
        assert stat.favorites == 10

    def test_avito_competitor_creation(self):
        competitor = AvitoCompetitor(
            name="Competitor 1",
            search_query="laptop",
            region="Moscow",
            is_active=True,
        )
        assert competitor.name == "Competitor 1"
        assert competitor.search_query == "laptop"

    def test_avito_auto_reply_creation(self):
        rule = AvitoAutoReply(
            keyword="цена",
            reply_text="Цена указана в объявлении.",
            is_active=True,
            priority=1,
        )
        assert rule.keyword == "цена"
        assert rule.is_active is True


class TestEmailModels:
    def test_email_template_creation(self):
        template = EmailTemplate(
            name="Welcome",
            subject="Добро пожаловать!",
            html_content="<h1>Привет, {имя}!</h1>",
            variables=["имя"],
        )
        assert template.name == "Welcome"
        assert "{имя}" in template.html_content

    def test_email_campaign_creation(self):
        campaign = EmailCampaign(
            name="New Year Sale",
            subject="Новогодние скидки!",
            subject_b="Скидки до 50%!",
            ab_test_percentage=50,
            status="draft",
        )
        assert campaign.name == "New Year Sale"
        assert campaign.status == "draft"
        assert campaign.ab_test_percentage == 50

    def test_email_campaign_log_creation(self):
        log = EmailCampaignLog(
            campaign_id=1,
            contact_id=1,
            email="test@example.com",
            subject_variant="A",
            status="sent",
        )
        assert log.email == "test@example.com"
        assert log.status == "sent"


class TestContactModels:
    def test_contact_creation(self):
        contact = Contact(
            email="user@example.com",
            name="Иван Иванов",
            city="Москва",
            consent_given=True,
            is_subscribed=True,
        )
        assert contact.email == "user@example.com"
        assert contact.consent_given is True

    def test_contact_segment_creation(self):
        segment = ContactSegment(
            name="VIP Clients",
            description="High-value customers",
            is_dynamic=False,
        )
        assert segment.name == "VIP Clients"
        assert segment.is_dynamic is False


class TestActivityLog:
    def test_activity_log_creation(self):
        log = ActivityLog(
            action="ad_published",
            entity_type="AvitoAd",
            entity_id=1,
            details={"avito_id": "12345"},
        )
        assert log.action == "ad_published"
        assert log.entity_type == "AvitoAd"
