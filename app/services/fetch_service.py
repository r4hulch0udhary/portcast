from app.external.metaphorpsum import MetaphorpsumClient
from app.repositories.paragraph_repository import ParagraphRepository
from sqlalchemy.ext.asyncio import AsyncSession

class FetchService:
    def __init__(self, metaphorpsum_client: MetaphorpsumClient, paragraph_repo: ParagraphRepository):
        self.metaphorpsum_client = metaphorpsum_client
        self.paragraph_repo = paragraph_repo

    async def fetch_and_store_paragraph(self, session: AsyncSession) -> str:
        content = await self.metaphorpsum_client.fetch_paragraph()
        repo = ParagraphRepository(session)
        await repo.save(content)
        return content