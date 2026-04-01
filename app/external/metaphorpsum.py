import httpx

class MetaphorpsumClient:
    BASE_URL = "http://metaphorpsum.com"

    async def fetch_paragraph(self, sentences: int = 50) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/paragraphs/1/{sentences}")
            response.raise_for_status()
            return response.text.strip()