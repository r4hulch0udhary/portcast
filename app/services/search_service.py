from app.repositories.paragraph_repository import ParagraphRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class SearchService:
    def __init__(self, paragraph_repo: ParagraphRepository):
        self.paragraph_repo = paragraph_repo

    async def search_paragraphs(self, session: AsyncSession, words: List[str], operator: str) -> List[str]:
        repo = ParagraphRepository(session)
        paragraphs = await repo.search_by_words(words, operator)
        return [p.content for p in paragraphs]