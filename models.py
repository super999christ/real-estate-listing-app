from datetime import datetime

from sqlalchemy import (
    Column, ForeignKey, Boolean,
    Enum, String, DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from database import Base
from schemas import Gender, Listing


class User(Base):
    """Model class for SQLAlchemy interpretation of the application's User model."""
    __tablename__ = 'users'

    id = Column(String(32), primary_key=True, index=True)
    username = Column(String(24), index=True, nullable=False, unique=True)
    full_name = Column(String(30), nullable=True)
    email = Column(EmailType, index=True, unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    date_of_birth = Column(DateTime(timezone=True), nullable=True)
    gender = Column(Enum(*[item.value for item in Gender], name='gender_types'), default='NOT_SPECIFIED')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # one-to-many relationship
    listings = relationship('Listing', back_populates='owner', cascade='all, delete-orphan', passive_deletes=True)


class Listing(Base):
    """Model class for SQLAlchemy interpretation of the application's Listing model."""
    __tablename__ = 'listings'

    id = Column(String(32), primary_key=True, index=True)
    type = Column(Enum(*[item.value for item in Listing], name='listing_types'), nullable=False)
    available_now = Column(Boolean, default=True)
    owner_id = Column(String(32), ForeignKey('users.id', ondelete='CASCADE'), index=True)
    address = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # one-to-many relationship
    owner = relationship('User', back_populates='listings')
