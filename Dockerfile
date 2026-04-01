FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --frozen --no-install-project

COPY . .

RUN uv sync --frozen --no-install-project --no-dev

# Use shell form CMD to run migrations and start the server safely evaluating HOST and PORT injected via .env
CMD ["sh", "-c", "uv run alembic upgrade head && uv run hypercorn app.main:app --bind ${HOST:-0.0.0.0}:${PORT:-8000}"]