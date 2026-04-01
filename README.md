# Portcast API

A clean-architecture, asynchronous Flask API service for fetching, storing, and searching text paragraphs.

## 📚 Module Documentation

Each component of the application has its own documentation. Explore them here:

- [**app/api**](app/api/README.md) - REST API Endpoints & Request Handling
- [**app/services**](app/services/README.md) - Core Business Logic & Caching
- [**app/repositories**](app/repositories/README.md) - Database Ops & Full-Text Search
- [**app/models**](app/models/README.md) - Database Schema Definitions
- [**app/external**](app/external/README.md) - Integration with Third-Party APIs
- [**tests**](tests/README.md) - Pytest Setup & Testing Strategy

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) (Python package manager)

### Installation

```bash
# 1. Install dependencies
uv sync

# 2. Configure Environment (Copy .env.example if available)
echo "DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/portcast" > .env
echo "TEST_DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/portcast_test" >> .env
echo "FLASK_DEBUG=True" >> .env

# 3. Run Database Migrations
uv run alembic upgrade head

# 4. Start the Application
uv run hypercorn app.main:app --bind 0.0.0.0:8000 --reload
```

## 🛠 Testing

```bash
uv run python -m pytest tests/ -v
```

## 🐳 Docker Deployment

```bash
docker-compose up --build -d
```

Visit `http://localhost:8000` to access the Vue.js frontend client or `http://localhost:8000/apidocs` for Swagger OpenAPI documentation!
