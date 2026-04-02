"""
Dictionary Service Module.

Correlates data stored in Paragraph entities with dictionary definitions.
Features calculating heavily repeated nouns via Regex maps across all stored text
and fetching asynchronous dictionary entries.
"""

import re
from typing import List, Dict
from collections import Counter
from sqlalchemy.ext.asyncio import AsyncSession

from app.external.dictionary_api import DictionaryAPIClient
from app.repositories.paragraph_repository import ParagraphRepository
import app.cache as cache_module


class DictionaryService:
    """Service to process paragraph language parsing alongside Dictionary API references."""

    def __init__(
        self,
        dictionary_client: DictionaryAPIClient,
        paragraph_repo: ParagraphRepository,
    ) -> None:
        """
        Instantiates necessary repository and external clients.

        Args:
            dictionary_client (DictionaryAPIClient): Configured HTTP dictionary instance.
            paragraph_repo (ParagraphRepository): Active DB connection context for Paragraphs.
        """
        self.dictionary_client = dictionary_client
        self.paragraph_repo = paragraph_repo

    async def get_top_words_definitions(
        self, session: AsyncSession, top_n: int = 10
    ) -> List[Dict[str, str]]:
        """
        Aggregates all paragraphs, counts English tokens, and fetches semantic definitions.

        Args:
            session (AsyncSession): Active SQLAlchemy async unit of work session.
            top_n (int, optional): Cut-off limit of frequent words. Defaults to 10.

        Returns:
            List[Dict[str, str]]: A list mapped dict containing words mapped mapping to string descriptions.
        """
        if cache_module.dictionary_result_cache is not None:
            return cache_module.dictionary_result_cache

        repo = ParagraphRepository(session)
        top_words = await repo.get_top_words(top_n)

        definitions = []
        for word in top_words:
            definition = await self.dictionary_client.get_definition(word)
            if definition:
                definitions.append({"word": word, "definition": definition})

        cache_module.dictionary_result_cache = definitions
        return definitions
