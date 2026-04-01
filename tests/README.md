# Tests Strategy

The test suite (`tests/`) validates the application using `pytest` combined with `pytest-asyncio` for asynchronous endpoint testing.

## 🧪 Structure

- **`conftest.py`**: A centralized fixture setup that prepares specific test databases. It handles setting up and tearing down the `portcast_test` PostgreSQL instance securely before and after test sessions, ensuring an isolated environment without affecting the primary DB.
- **`test_*.py`**: Individual test files that target specific features:
  - `test_dictionary.py`: Validates caching logic, frequency analysis, and external client integrations for word parsing.
  - `test_fetch.py`: Validates content fetching, duplicate checking constraints using hashes, and DB saves.
  - `test_search.py`: Specifically tests queries containing varying operators like `AND`/`OR`.

## ⚙️ Running Tests

To run the whole test suite against your test DB setup:

```bash
uv run python -m pytest tests/ -v
```

This will give you a detailed output of what passes/fails across the tests.
