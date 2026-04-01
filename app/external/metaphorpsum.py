"""
Metaphorpsum External Client.

Responsible for requesting and parsing random filler text strings
using the Metaphorpsum HTTP API via httpx asynchronously.
"""

import httpx


class MetaphorpsumClient:
    """Client for retrieving random generated text paragraphs."""

    BASE_URL = "http://metaphorpsum.com"

    async def fetch_paragraph(self, sentences: int = 50) -> str:
        """
        Connects externally to obtain random sentences representing a new paragraph.

        Args:
            sentences (int, optional): Approximate word block count to fetch. Defaults to 50.

        Returns:
            str: Raw paragraph content block response.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/paragraphs/1/{sentences}")
            response.raise_for_status()
            return response.text.strip()
