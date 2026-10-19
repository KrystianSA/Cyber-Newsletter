FROM ghcr.io/astral-sh/uv:0.13.1-python3.13-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app/backend
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY backend/app ./app

FROM python:3.13-slim-bookworm
RUN useradd --system --create-home app
WORKDIR /app/backend
COPY --from=builder --chown=app:app /app/backend /app/backend
ENV PATH="/app/backend/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
