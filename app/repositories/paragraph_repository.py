from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.paragraph import Paragraph, db
from typing import List

class ParagraphRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, content: str) -> Paragraph:
        paragraph = Paragraph(content=content)
        self.session.add(paragraph)
        await self.session.commit()
        await self.session.refresh(paragraph)
        return paragraph

    async def get_all(self) -> List[Paragraph]:
        result = await self.session.execute(select(Paragraph))
        return result.scalars().all()

    async def search_by_words(self, words: List[str], operator: str) -> List[Paragraph]:
        # For simplicity, use ILIKE for case-insensitive search
        # In production, use full-text search
        query = select(Paragraph)
        if operator == "and":
            for word in words:
                query = query.where(Paragraph.content.ilike(f"%{word}%"))
        elif operator == "or":
            conditions = [Paragraph.content.ilike(f"%{word}%") for word in words]
            query = query.where(db.or_(*conditions))
        result = await self.session.execute(query)
        return result.scalars().all()