FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc build-essential dos2unix \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
ENV PATH="/app/.venv/bin:${PATH}"

RUN uv pip install alembic gunicorn
RUN find /app/.venv/bin -type f -exec dos2unix {} \; || true

RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["bash", "-c", "uv run alembic upgrade head && uv run gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app"]
