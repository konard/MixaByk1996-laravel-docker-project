"""Initial schema - all tables.

Revision ID: 001_initial
Revises:
Create Date: 2026-02-01
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Avito accounts
    op.create_table(
        "avito_accounts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("client_id", sa.String(255), nullable=False),
        sa.Column("client_secret", sa.String(255), nullable=False),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("token_expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Avito ad templates
    op.create_table(
        "avito_ad_templates",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("avito_accounts.id", ondelete="CASCADE")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(255), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("images", sa.JSON(), nullable=True),
        sa.Column("params", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Avito ads
    op.create_table(
        "avito_ads",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("avito_accounts.id", ondelete="CASCADE")),
        sa.Column("avito_id", sa.String(255), nullable=True),
        sa.Column("template_id", sa.Integer(), sa.ForeignKey("avito_ad_templates.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("category", sa.String(255), nullable=True),
        sa.Column("status", sa.String(50), default="draft"),
        sa.Column("campaign", sa.String(255), nullable=True),
        sa.Column("images", sa.JSON(), nullable=True),
        sa.Column("params", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Avito ad stats
    op.create_table(
        "avito_ad_stats",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("ad_id", sa.Integer(), sa.ForeignKey("avito_ads.id", ondelete="CASCADE")),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("views", sa.Integer(), default=0),
        sa.Column("favorites", sa.Integer(), default=0),
        sa.Column("contacts", sa.Integer(), default=0),
        sa.Column("calls", sa.Integer(), default=0),
        sa.Column("messages_count", sa.Integer(), default=0),
        sa.Column("position", sa.Float(), nullable=True),
    )

    # Avito competitors
    op.create_table(
        "avito_competitors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("search_query", sa.String(255), nullable=False),
        sa.Column("region", sa.String(255), nullable=True),
        sa.Column("category", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("check_interval_hours", sa.Integer(), default=24),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Avito competitor snapshots
    op.create_table(
        "avito_competitor_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("competitor_id", sa.Integer(), sa.ForeignKey("avito_competitors.id", ondelete="CASCADE")),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("seller_name", sa.String(255), nullable=True),
        sa.Column("images", sa.JSON(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Avito messages
    op.create_table(
        "avito_messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("avito_accounts.id", ondelete="CASCADE")),
        sa.Column("chat_id", sa.String(255), nullable=False),
        sa.Column("sender_name", sa.String(255), nullable=True),
        sa.Column("message_text", sa.Text(), nullable=True),
        sa.Column("direction", sa.String(20), default="incoming"),
        sa.Column("classification", sa.String(100), nullable=True),
        sa.Column("is_auto_replied", sa.Boolean(), default=False),
        sa.Column("forwarded_to_manager", sa.Boolean(), default=False),
        sa.Column("received_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Avito auto replies
    op.create_table(
        "avito_auto_replies",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("keyword", sa.String(255), nullable=False),
        sa.Column("reply_text", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("priority", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Contacts
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("city", sa.String(255), nullable=True),
        sa.Column("interests", sa.JSON(), nullable=True),
        sa.Column("purchase_history", sa.JSON(), nullable=True),
        sa.Column("consent_given", sa.Boolean(), default=False),
        sa.Column("consent_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_subscribed", sa.Boolean(), default=True),
        sa.Column("unsubscribed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Contact segments
    op.create_table(
        "contact_segments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("filters", sa.JSON(), nullable=True),
        sa.Column("is_dynamic", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Contact-segment many-to-many
    op.create_table(
        "contact_segment_association",
        sa.Column("contact_id", sa.Integer(), sa.ForeignKey("contacts.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("segment_id", sa.Integer(), sa.ForeignKey("contact_segments.id", ondelete="CASCADE"), primary_key=True),
    )

    # Email templates
    op.create_table(
        "email_templates",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("html_content", sa.Text(), nullable=False),
        sa.Column("text_content", sa.Text(), nullable=True),
        sa.Column("variables", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Email campaigns
    op.create_table(
        "email_campaigns",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("template_id", sa.Integer(), sa.ForeignKey("email_templates.id", ondelete="SET NULL"), nullable=True),
        sa.Column("segment_id", sa.Integer(), sa.ForeignKey("contact_segments.id", ondelete="SET NULL"), nullable=True),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("subject_b", sa.String(255), nullable=True),
        sa.Column("ab_test_percentage", sa.Integer(), default=50),
        sa.Column("status", sa.String(50), default="draft"),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("recurrence", sa.String(50), nullable=True),
        sa.Column("sent_count", sa.Integer(), default=0),
        sa.Column("open_count", sa.Integer(), default=0),
        sa.Column("click_count", sa.Integer(), default=0),
        sa.Column("unsubscribe_count", sa.Integer(), default=0),
        sa.Column("bounce_count", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Email campaign logs
    op.create_table(
        "email_campaign_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("campaign_id", sa.Integer(), sa.ForeignKey("email_campaigns.id", ondelete="CASCADE")),
        sa.Column("contact_id", sa.Integer(), sa.ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("subject_variant", sa.String(10), default="A"),
        sa.Column("status", sa.String(50), default="sent"),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("clicked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Email link clicks
    op.create_table(
        "email_link_clicks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("log_id", sa.Integer(), sa.ForeignKey("email_campaign_logs.id", ondelete="CASCADE")),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("clicked_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # Activity logs
    op.create_table(
        "activity_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=True),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("activity_logs")
    op.drop_table("email_link_clicks")
    op.drop_table("email_campaign_logs")
    op.drop_table("email_campaigns")
    op.drop_table("email_templates")
    op.drop_table("contact_segment_association")
    op.drop_table("contact_segments")
    op.drop_table("contacts")
    op.drop_table("avito_auto_replies")
    op.drop_table("avito_messages")
    op.drop_table("avito_competitor_snapshots")
    op.drop_table("avito_competitors")
    op.drop_table("avito_ad_stats")
    op.drop_table("avito_ads")
    op.drop_table("avito_ad_templates")
    op.drop_table("avito_accounts")
