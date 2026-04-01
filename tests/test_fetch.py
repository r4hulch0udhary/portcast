import pytest
from app.services.fetch_service import FetchService
from app.external.metaphorpsum import MetaphorpsumClient
from app.repositories.paragraph_repository import ParagraphRepository
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_fetch_and_store_paragraph(db_session, setup_test_db):
    # Mock the client
    mock_client = MetaphorpsumClient()
    mock_client.fetch_paragraph = AsyncMock(return_value="Test paragraph content.")

    repo = ParagraphRepository(db_session)
    service = FetchService(mock_client, repo)

    result = await service.fetch_and_store_paragraph(db_session)

    assert result == "Test paragraph content."
    # Check if saved
    paragraphs = await repo.get_all()
    assert len(paragraphs) == 1
    assert paragraphs[0].content == "Test paragraph content."
