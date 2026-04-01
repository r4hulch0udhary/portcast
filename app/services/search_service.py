"""
Search Service Module.

Provides the business logic layer for interpreting search queries and interfacing
with the paragraph repository to retrieve matching text paragraphs.
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.paragraph_repository import ParagraphRepository


class SearchService:
    """
    Search Service for discovering paragraphs based on criteria via Full Text Search.
    """

    def __init__(self, paragraph_repo: ParagraphRepository) -> None:
        """
        Initializes the SearchService with a ParagraphRepository.

        Args:
            paragraph_repo (ParagraphRepository): Active paragraph repository.
        """
        self.paragraph_repo = paragraph_repo

    async def search_paragraphs(
        self, session: AsyncSession, words: List[str], operator: str
    ) -> List[str]:
        """
        Searches paragraphs matching the given words and operator grouping.

        Args:
            session (AsyncSession): Active SQLAlchemy async session.
            words (List[str]): Tokens to query across the paragraphs contents.
            operator (str): Strategy to combine words ('and' | 'or').

        Returns:
            List[str]: A list of paragraphs (raw text content) matching the search.
        """
        repo = ParagraphRepository(session)
        paragraphs = await repo.search_by_words(words, operator)
        return [p.content for p in paragraphs]
