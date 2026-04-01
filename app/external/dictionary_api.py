import httpx
from typing import Optional

class DictionaryAPIClient:
    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"

    async def get_definition(self, word: str) -> Optional[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{word}")
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and data[0].get('meanings'):
                    # Get the first definition
                    meanings = data[0]['meanings']
                    if meanings and meanings[0].get('definitions'):
                        return meanings[0]['definitions'][0].get('definition')
            return None