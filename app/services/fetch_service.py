from app.external.metaphorpsum import MetaphorpsumClient
from app.repositories.paragraph_repository import ParagraphRepository
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib


class FetchService:
    def __init__(
        self,
        metaphorpsum_client: MetaphorpsumClient,
        paragraph_repo: ParagraphRepository,
    ):
        self.metaphorpsum_client = metaphorpsum_client
        self.paragraph_repo = paragraph_repo

    async def fetch_and_store_paragraph(self, session: AsyncSession) -> str:
        repo = ParagraphRepository(session)
        max_attempts = 10  # Prevent infinite loop
        for _ in range(max_attempts):
            content = await self.metaphorpsum_client.fetch_paragraph()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            if not await repo.hash_exists(content_hash):
                await repo.save(content)
                return content
        raise Exception("Unable to fetch a unique paragraph after multiple attempts")
