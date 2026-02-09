from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

# Many-to-many relationship table
contact_segment_association = Table(
    "contact_segment_association",
    Base.metadata,
    Column("contact_id", Integer, ForeignKey("contacts.id", ondelete="CASCADE"), primary_key=True),
    Column("segment_id", Integer, ForeignKey("contact_segments.id", ondelete="CASCADE"), primary_key=True),
)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    city = Column(String(255), nullable=True)
    interests = Column(JSON, nullable=True)
    purchase_history = Column(JSON, nullable=True)
    consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime(timezone=True), nullable=True)
    is_subscribed = Column(Boolean, default=True)
    unsubscribed_at = Column(DateTime(timezone=True), nullable=True)
    source = Column(String(100), nullable=True)  # import, manual, api
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    segments = relationship("ContactSegment", secondary=contact_segment_association, back_populates="contacts")


class ContactSegment(Base):
    __tablename__ = "contact_segments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    filters = Column(JSON, nullable=True)  # filter rules for dynamic segments
    is_dynamic = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    contacts = relationship("Contact", secondary=contact_segment_association, back_populates="segments")
    campaigns = relationship("EmailCampaign", back_populates="segment")
