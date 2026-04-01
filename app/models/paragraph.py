from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
import uuid

db = SQLAlchemy()


class Paragraph(db.Model):
    __tablename__ = "paragraphs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
