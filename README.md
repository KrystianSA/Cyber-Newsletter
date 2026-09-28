# Cyber Newsletter

Strona z formularzem zapisu do newslettera o cyberbezpieczeństwie.

- `frontend/` — statyczna strona, Vue 3 + Vite.
- `backend/` — FastAPI backend obsługujący formularz zapisu.

## Uruchomienie razem (frontend + backend)

```bash
npm install
npm run dev:all
```

Wymaga `uv` na PATH oraz uprzedniego `uv sync` w `backend/`. Frontend wystartuje pod `http://localhost:5173`, backend pod `http://localhost:8000`.

## Frontend

```bash
cd frontend
npm install
npm run dev       # dev server, http://localhost:5173
npm run build      # build produkcyjny do frontend/dist/
npm run preview   # podgląd builda produkcyjnego
```

Wynik `npm run build` trafia do `frontend/dist/` — to czysto statyczne pliki, które można wdrożyć na dowolnym hostingu statycznym (Vercel, Netlify, GitHub Pages itp.), bez potrzeby uruchamiania serwera Node.

Formularz w `frontend/src/components/NewsletterSignup.vue` wysyła zapytanie `POST` na `${VITE_API_URL ?? 'http://localhost:8000'}/subscribers` i obsługuje przypadki sukcesu, duplikatu adresu (409) oraz błędu sieci.

## Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --reload-dir app --port 8000
```

Serwer wystartuje pod `http://localhost:8000`. Interaktywna dokumentacja: `http://localhost:8000/docs`.

`--reload-dir app` ogranicza auto-reload do katalogu `app/` — bez tego uvicorn obserwuje cały working directory, w tym `.venv/`, i wpada w pętlę ciągłych restartów przy każdej zmianie w zależnościach.

### Endpointy

- `GET /health` — health check (na przyszłość pod k8s liveness/readiness probe).
- `POST /subscribers` — zapisuje adres e-mail.
  - Body: `{"email": "ktos@example.com"}`
  - `201` — zapisano, zwraca `{"email": ..., "created_at": ...}`
  - `409` — adres już istnieje w bazie
  - `422` — nieprawidłowy format adresu

### Baza danych

Na razie: SQLite, plik lokalny w `backend/data/newsletter.db` (tworzony automatycznie przy starcie, katalog `data/` jest w `.gitignore`). To rozwiązanie tymczasowe do testów — warstwa dostępu do danych jest przez SQLAlchemy, więc przejście na PostgreSQL w przyszłości sprowadza się do zmiany `SQLALCHEMY_DATABASE_URL` w `app/database.py` (i dodania sterownika, np. `psycopg`).

CORS w `app/main.py` jest skonfigurowany pod `http://localhost:5173` (domyślny port Vite dev servera).
