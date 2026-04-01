import pytest
from app.services.search_service import SearchService
from app.repositories.paragraph_repository import ParagraphRepository


@pytest.mark.asyncio
async def test_search_paragraphs(db_session, setup_test_db):
    # Add test data
    repo = ParagraphRepository(db_session)
    await repo.save("This is a test paragraph with some words.")
    await repo.save("Another paragraph with different words.")

    service = SearchService(repo)

    # Search for "test"
    results = await service.search_paragraphs(db_session, ["test"], "or")
    assert len(results) == 1
    assert "test" in results[0].lower()

    # Search for "words"
    results = await service.search_paragraphs(db_session, ["words"], "or")
    assert len(results) == 2
