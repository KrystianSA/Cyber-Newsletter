# Cyber Newsletter

Strona z formularzem zapisu do newslettera o cyberbezpieczeństwie. Adresy e-mail trafiają do bazy PostgreSQL.

## Technologie

- **Frontend:** Vue 3, Vite
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
- **Baza danych:** PostgreSQL (Docker Compose)
- **Narzędzia:** npm, uv
- **AI:** projekt zbudowany z pomocą [Claude Code](https://claude.com/claude-code) (asystent AI do programowania w terminalu)

## Uruchomienie

Wymagane: Node.js, [uv](https://docs.astral.sh/uv/), Docker.

```bash
cp .env.example     # uzupełnij dane dostępowe do bazy
npm install
(cd backend && uv sync)
npm run db:up            # PostgreSQL w Dockerze
npm run dev:all          # frontend + backend
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (dokumentacja API: `/docs`)
