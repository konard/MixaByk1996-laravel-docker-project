from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    html_content = Column(Text, nullable=False)
    text_content = Column(Text, nullable=True)
    variables = Column(JSON, nullable=True)  # list of variable names used
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    campaigns = relationship("EmailCampaign", back_populates="template")


class EmailCampaign(Base):
    __tablename__ = "email_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id", ondelete="SET NULL"), nullable=True)
    segment_id = Column(Integer, ForeignKey("contact_segments.id", ondelete="SET NULL"), nullable=True)
    subject = Column(String(255), nullable=False)
    subject_b = Column(String(255), nullable=True)  # A/B test variant
    ab_test_percentage = Column(Integer, default=50)
    status = Column(String(50), default="draft")  # draft, scheduled, sending, sent, cancelled
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    recurrence = Column(String(50), nullable=True)  # daily, weekly, monthly, null
    sent_count = Column(Integer, default=0)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    unsubscribe_count = Column(Integer, default=0)
    bounce_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    template = relationship("EmailTemplate", back_populates="campaigns")
    segment = relationship("ContactSegment", back_populates="campaigns")
    logs = relationship("EmailCampaignLog", back_populates="campaign")


class EmailCampaignLog(Base):
    __tablename__ = "email_campaign_logs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("email_campaigns.id", ondelete="CASCADE"))
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="SET NULL"), nullable=True)
    email = Column(String(255), nullable=False)
    subject_variant = Column(String(10), default="A")  # A or B
    status = Column(String(50), default="sent")  # sent, delivered, opened, clicked, bounced, failed
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    campaign = relationship("EmailCampaign", back_populates="logs")
    clicks = relationship("EmailLinkClick", back_populates="log")


class EmailLinkClick(Base):
    __tablename__ = "email_link_clicks"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("email_campaign_logs.id", ondelete="CASCADE"))
    url = Column(Text, nullable=False)
    clicked_at = Column(DateTime(timezone=True), server_default=func.now())

    log = relationship("EmailCampaignLog", back_populates="clicks")
