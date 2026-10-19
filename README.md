# Cyber Newsletter

A landing page with a signup form for a cybersecurity newsletter. Email addresses are stored in a PostgreSQL database.

<p align="center">
  <img width="600" height="450" alt="Zrzut ekranu 2026-10-19 o 20 54 06" src="https://github.com/user-attachments/assets/3c969754-9164-4168-ba84-70d90ed15c82"/>
</p>

## Tech stack

- **Frontend:** Vue 3, Vite
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL (Docker Compose)
- **Tests:** pytest (backend API tests against a separate database)
- **CI:** GitHub Actions (frontend lint and build, backend integration tests)
- **Tooling:** npm, uv
- **AI:** built with the help of [Claude Code](https://claude.com/claude-code) (an AI coding assistant for the terminal)

## Getting started

Requirements: Node.js, [uv](https://docs.astral.sh/uv/), Docker.

```bash
cp .env.example .env     # fill in the database credentials
npm install
(cd backend && uv sync)
npm run dev:all          # PostgreSQL (Docker) + backend + frontend
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (API docs: `/docs`)

## Tests

Backend tests connect to a real, separate `test-db` database (port 5433, data kept in memory), never to the development database.

```bash
docker compose --profile test up -d --wait test-db
(cd backend && uv run pytest)
docker compose --profile test down     # stop the test database
```

The database URL can be overridden with the `TEST_DATABASE_URL` variable (the database name must end with `_test`).

## CI

The [ci.yml](.github/workflows/ci.yml) workflow runs on push and pull requests to `main`:

- `frontend-linting` → `build-frontend` (the build waits for a green lint),
- `backend-integration-test` (runs in parallel; Postgres is provided via `services:`).

Environment setup lives in the `.github/actions/setup-frontend` and `setup-backend` actions. The uv version (0.13.1) is pinned in CI and in `backend/Dockerfile` — change it in both places at once.
