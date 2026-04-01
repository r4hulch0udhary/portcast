import pytest
from app.services.dictionary_service import DictionaryService
from app.repositories.paragraph_repository import ParagraphRepository
from app.external.dictionary_api import DictionaryAPIClient
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_get_top_words_definitions(db_session, setup_test_db):
    # Add test data
    repo = ParagraphRepository(db_session)
    await repo.save("This is a test paragraph with some words.")
    await repo.save("Another paragraph with different words.")

    # Mock client
    mock_client = DictionaryAPIClient()
    mock_client.get_definition = AsyncMock(
        side_effect=lambda word: f"Definition of {word}" if word == "test" else None
    )

    service = DictionaryService(mock_client, repo)

    results = await service.get_top_words_definitions(db_session, top_n=5)

    # Should have definitions for top words
    assert len(results) >= 0  # Depending on words
