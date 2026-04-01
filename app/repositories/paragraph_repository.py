"""
Paragraph Repository Module.

Manages data persistence operations for paragraph entities via SQLAlchemy and PostgreSQL.
Includes functionality for checking existence via SHA-256 and Full-Text Search.
"""

from typing import List
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.paragraph import Paragraph


class ParagraphRepository:
    """Repository handling paragraph database interactions."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the repository with the active database session.

        Args:
            session (AsyncSession): SQLAlchemy async session bounded to the current request.
        """
        self.session = session

    async def save(self, content: str) -> Paragraph:
        """
        Saves a new paragraph to the database securely.

        Args:
            content (str): The raw text of the paragraph to be stored.

        Returns:
            Paragraph: The saved paragraph entity containing the generated UUID.
        """
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        paragraph = Paragraph(content=content, content_hash=content_hash)
        self.session.add(paragraph)
        await self.session.commit()
        await self.session.refresh(paragraph)
        return paragraph

    async def hash_exists(self, content_hash: str) -> bool:
        """
        Validates if a paragraph already exists using its generated SHA-256 hash.

        Args:
            content_hash (str): The unique hash of the given paragraph content.

        Returns:
            bool: True if paragraph exists, otherwise False.
        """
        result = await self.session.execute(
            select(Paragraph).where(Paragraph.content_hash == content_hash)
        )
        return result.scalar() is not None

    async def get_all(self) -> List[Paragraph]:
        """
        Retrieves all paragraph entries from the database.

        Returns:
            List[Paragraph]: A list of all stored paragraphs.
        """
        result = await self.session.execute(select(Paragraph))
        return result.scalars().all()

    async def search_by_words(self, words: List[str], operator: str) -> List[Paragraph]:
        """
        Returns paragraphs matching the criteria using PostgreSQL full text search natively.

        Args:
            words (List[str]): List of keywords.
            operator (str): Combination strategy ('and' or 'or').

        Returns:
            List[Paragraph]: Retrieved paragraphs matching search criteria.
        """
        # Use 'simple' config so stopwords (the, and, they…) are not stripped
        ts_vector = func.to_tsvector("simple", Paragraph.content)
        if operator == "and":
            query_str = " & ".join(w.lower() for w in words)
        else:
            query_str = " | ".join(w.lower() for w in words)

        ts_query = func.to_tsquery("simple", query_str)
        query = select(Paragraph).where(ts_vector.op("@@")(ts_query))

        result = await self.session.execute(query)
        return result.scalars().all()
