"""
Paragraph Fetching Service Module.

Ties the external HTTP call logic retrieving text segments from metaphorpsum
into storing it using SQLAlchemy while preventing loops mapping hashes.
"""

import hashlib
from sqlalchemy.ext.asyncio import AsyncSession

from app.external.metaphorpsum import MetaphorpsumClient
from app.repositories.paragraph_repository import ParagraphRepository
from app.cache import invalidate_dictionary_cache


class FetchService:
    """
    Coordinator business logic for paragraph ingestions and validity checks.
    """

    def __init__(
        self,
        metaphorpsum_client: MetaphorpsumClient,
        paragraph_repo: ParagraphRepository,
    ) -> None:
        """
        Instantiates specific client interfaces enabling fetch flows.

        Args:
            metaphorpsum_client (MetaphorpsumClient): Remote text HTTP dependency.
            paragraph_repo (ParagraphRepository): Active DB connection context bounded to request.
        """
        self.metaphorpsum_client = metaphorpsum_client
        self.paragraph_repo = paragraph_repo

    async def fetch_and_store_paragraph(self, session: AsyncSession) -> str:
        """
        Executes a loop to pull paragraphs online securely mapping and saving onto DB.
        Includes a 10-attempt safeguard logic preventing cyclic loop requests on duplicates.

        Args:
            session (AsyncSession): SQLAlchemy commit control block.

        Raises:
            Exception: System failure grabbing unique generated paragraphs repeatedly.

        Returns:
            str: Safely preserved raw fetched payload string.
        """
        repo = ParagraphRepository(session)
        max_attempts = 10  # Prevent infinite loop
        for _ in range(max_attempts):
            content = await self.metaphorpsum_client.fetch_paragraph()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            if not await repo.hash_exists(content_hash):
                await repo.save(content)
                invalidate_dictionary_cache()
                return content
        raise Exception("Unable to fetch a unique paragraph after multiple attempts")
