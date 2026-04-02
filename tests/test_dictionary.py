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

    results = await service.get_top_words_definitions(db_session, top_n=10)

    # Should only have definitions for the word 'test' based on the mock
    assert len(results) == 1
    assert results[0]["word"] == "test"
    assert results[0]["definition"] == "Definition of test"
