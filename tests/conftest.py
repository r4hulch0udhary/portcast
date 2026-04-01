import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.paragraph import db
from app.config import config

# Test database URL
TEST_DATABASE_URL = config.test_database_url

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def setup_test_db():
    """Set up test database tables."""
    # Create tables in test DB
    test_engine = create_async_engine(TEST_DATABASE_URL)
    async with test_engine.begin() as conn:
        await conn.run_sync(db.metadata.create_all)

    yield

    # Clean up tables after tests
    async with test_engine.begin() as conn:
        await conn.run_sync(db.metadata.drop_all)
    await test_engine.dispose()

@pytest_asyncio.fixture
async def db_session(setup_test_db):
    """Provide a test database session."""
    engine = create_async_engine(TEST_DATABASE_URL)
    connection = await engine.connect()
    transaction = await connection.begin()
    
    async_session = AsyncSession(bind=connection, expire_on_commit=False)
    
    yield async_session
    
    await async_session.close()
    await transaction.rollback()
    await connection.close()
    await engine.dispose()