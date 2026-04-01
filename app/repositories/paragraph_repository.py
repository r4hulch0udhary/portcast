from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.paragraph import Paragraph
from typing import List
import hashlib

class ParagraphRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, content: str) -> Paragraph:
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        paragraph = Paragraph(content=content, content_hash=content_hash)
        self.session.add(paragraph)
        await self.session.commit()
        await self.session.refresh(paragraph)
        return paragraph

    async def hash_exists(self, content_hash: str) -> bool:
        result = await self.session.execute(
            select(Paragraph).where(Paragraph.content_hash == content_hash)
        )
        return result.scalar() is not None

    async def get_all(self) -> List[Paragraph]:
        result = await self.session.execute(select(Paragraph))
        return result.scalars().all()

    async def search_by_words(self, words: List[str], operator: str) -> List[Paragraph]:
        # Use PostgreSQL full-text search
        ts_vector = func.to_tsvector('english', Paragraph.content)
        if operator == "and":
            query_str = ' & '.join(words)
        elif operator == "or":
            query_str = ' | '.join(words)
        else:
            query_str = ' | '.join(words)  # default to or
        
        ts_query = func.to_tsquery('english', query_str)
        query = select(Paragraph).where(ts_vector.op('@@')(ts_query))
        
        result = await self.session.execute(query)
        return result.scalars().all()