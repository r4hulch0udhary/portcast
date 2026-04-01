import httpx
from typing import Optional
from app.cache import definition_cache

class DictionaryAPIClient:
    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"

    async def get_definition(self, word: str) -> Optional[str]:
        if word in definition_cache:
            return definition_cache[word]

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{word}")
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and data[0].get('meanings'):
                    meanings = data[0]['meanings']
                    if meanings and meanings[0].get('definitions'):
                        result = meanings[0]['definitions'][0].get('definition')
                        definition_cache[word] = result
                        return result

        definition_cache[word] = None
        return None