from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class AvitoAccount(Base):
    __tablename__ = "avito_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    client_id = Column(String(255), nullable=False)
    client_secret = Column(String(255), nullable=False)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    ads = relationship("AvitoAd", back_populates="account")
    templates = relationship("AvitoAdTemplate", back_populates="account")
    messages = relationship("AvitoMessage", back_populates="account")


class AvitoAdTemplate(Base):
    __tablename__ = "avito_ad_templates"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("avito_accounts.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=True)
    images = Column(JSON, nullable=True)  # list of image URLs
    params = Column(JSON, nullable=True)  # additional Avito params
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    account = relationship("AvitoAccount", back_populates="templates")


class AvitoAd(Base):
    __tablename__ = "avito_ads"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("avito_accounts.id", ondelete="CASCADE"))
    avito_id = Column(String(255), nullable=True)  # ID on Avito
    template_id = Column(Integer, ForeignKey("avito_ad_templates.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=True)
    category = Column(String(255), nullable=True)
    status = Column(String(50), default="draft")  # draft, active, blocked, archived
    campaign = Column(String(255), nullable=True)
    images = Column(JSON, nullable=True)
    params = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    account = relationship("AvitoAccount", back_populates="ads")
    stats = relationship("AvitoAdStat", back_populates="ad")


class AvitoAdStat(Base):
    __tablename__ = "avito_ad_stats"

    id = Column(Integer, primary_key=True, index=True)
    ad_id = Column(Integer, ForeignKey("avito_ads.id", ondelete="CASCADE"))
    date = Column(DateTime(timezone=True), nullable=False)
    views = Column(Integer, default=0)
    favorites = Column(Integer, default=0)
    contacts = Column(Integer, default=0)
    calls = Column(Integer, default=0)
    messages_count = Column(Integer, default=0)
    position = Column(Float, nullable=True)

    ad = relationship("AvitoAd", back_populates="stats")


class AvitoCompetitor(Base):
    __tablename__ = "avito_competitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    search_query = Column(String(255), nullable=False)
    region = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    check_interval_hours = Column(Integer, default=24)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    snapshots = relationship("AvitoCompetitorSnapshot", back_populates="competitor")


class AvitoCompetitorSnapshot(Base):
    __tablename__ = "avito_competitor_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("avito_competitors.id", ondelete="CASCADE"))
    title = Column(String(255))
    price = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    seller_name = Column(String(255), nullable=True)
    images = Column(JSON, nullable=True)
    captured_at = Column(DateTime(timezone=True), server_default=func.now())

    competitor = relationship("AvitoCompetitor", back_populates="snapshots")


class AvitoMessage(Base):
    __tablename__ = "avito_messages"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("avito_accounts.id", ondelete="CASCADE"))
    chat_id = Column(String(255), nullable=False)
    sender_name = Column(String(255), nullable=True)
    message_text = Column(Text, nullable=True)
    direction = Column(String(20), default="incoming")  # incoming, outgoing
    classification = Column(String(100), nullable=True)  # question, complaint, order, etc.
    is_auto_replied = Column(Boolean, default=False)
    forwarded_to_manager = Column(Boolean, default=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("AvitoAccount", back_populates="messages")


class AvitoAutoReply(Base):
    __tablename__ = "avito_auto_replies"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), nullable=False)
    reply_text = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
