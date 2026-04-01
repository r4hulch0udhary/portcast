"""
Paragraph Model Module.

Defines the SQLAlchemy model representing a paragraph object inside
the PostgreSQL database. Includes the string representation mapping for
type hints.
"""

from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
import uuid

db = SQLAlchemy()


class Paragraph(db.Model):
    """
    SQLAlchemy Paragraph Table Entity.

    Attributes:
        id (str): UUID Primary Key.
        content (str): The actual raw text content.
        content_hash (str): The SHA-256 generated hash mapped from the content for checking uniqueness in DB.
        created_at (DateTime): Timestamp of when paragraph was inserted.
    """

    __tablename__ = "paragraphs"

    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content: str = Column(Text, nullable=False)
    content_hash: str = Column(String(64), nullable=False, unique=True)  # SHA256 hash
    created_at = Column(DateTime(timezone=True), server_default=func.now())
