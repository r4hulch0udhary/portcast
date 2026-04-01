from pydantic import BaseModel, Field
from typing import List

class SearchRequest(BaseModel):
    words: List[str] = Field(..., description="List of words to search for")
    operator: str = Field(..., pattern="^(and|or)$", description="Operator: 'and' or 'or'")

class SearchResponse(BaseModel):
    paragraphs: List[str] = Field(..., description="Matching paragraphs")