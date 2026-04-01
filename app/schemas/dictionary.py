from pydantic import BaseModel, Field
from typing import List, Dict

class WordDefinition(BaseModel):
    word: str
    definition: str

class DictionaryResponse(BaseModel):
    words: List[WordDefinition] = Field(..., description="Top words with definitions")