# Decyzje architektoniczne

## Spis treści

| ID | Tytuł | Status | Data |
|---|---|---|---|
| [ADR-001](#adr-001-testy-integracyjne-na-osobnej-bazie) | Testy integracyjne na osobnej bazie | zaakceptowana | 2026-10-19 |
| [ADR-002](#adr-002-własny-job-zbiorczy-w-ci-zamiast-zewnętrznej-akcji) | Własny job zbiorczy w CI zamiast zewnętrznej akcji | zaakceptowana | 2026-11-04 |
| [ADR-003](#adr-003-ruleset-na-main) | Ruleset na `main` | zaakceptowana | 2026-11-06 |

## ADR-001: Testy integracyjne na osobnej bazie

- **Status:** zaakceptowana
- **Data:** 2026-10-19 (testy: `816044f`; wstrzykiwanie bazy przez `create_app`: `105c7c5`, 2026-10-31)

### Kontekst

API zapisuje adresy e-mail w PostgreSQL i polega na zachowaniu bazy: unikalność (`UNIQUE`) rozróżnia wielkość liter, a duplikat kończy się `IntegrityError` obsłużonym w kodzie. Testy muszą to sprawdzać, ale nie mogą dotykać bazy deweloperskiej, bo fixture czyści tabelę (`TRUNCATE`) przed każdym testem.

### Decyzja

Testy API to testy integracyjne na prawdziwym Postgresie:

- osobna usługa `test-db` w `docker-compose.yml` (profil `test`, `127.0.0.1:5433`, dane w tmpfs, więc każde uruchomienie startuje z czystą bazą),
- adres bazy z wymaganej zmiennej `TEST_DATABASE_URL` (bez wartości domyślnej w kodzie),
- bezpiecznik: fixture `test_db` przerywa sesję (`pytest.exit`), jeśli nazwa bazy nie kończy się na `_test`,
- baza testowa trafia do aplikacji przez `create_app(connector)`, więc testy nigdy nie importują `app/main.py` ani produkcyjnego połączenia,
- w CI baza pochodzi z `services:` joba `backend-integration-test` (port 5433).

### Konsekwencje

- Testy sprawdzają realne zachowanie bazy i ograniczeń, nie jej atrapę.
- Lokalnie wymagany jest Docker i uruchomiona `test-db`; testy są wolniejsze niż z mockami.
- Błędna konfiguracja (zła nazwa bazy) zatrzymuje testy, zamiast kasować dane.

**Odrzucone alternatywy:**

- *SQLite w pamięci* — inna semantyka (m.in. rozróżnianie wielkości liter w `UNIQUE`, obsługa `IntegrityError`), więc testy mogłyby przechodzić tam, gdzie produkcja zawiedzie.
- *Mocki sesji SQLAlchemy* — nie sprawdzają prawdziwego SQL ani ograniczeń bazy; test potwierdzałby tylko, że kod wywołuje mock.
- *Baza deweloperska do testów* — `TRUNCATE` przed każdym testem kasowałby dane deweloperskie.

## ADR-002: Własny job zbiorczy w CI zamiast zewnętrznej akcji

- **Status:** zaakceptowana
- **Data:** 2026-11-04 (commit `f1717a1`)

### Kontekst

Workflow `ci.yml` ma kilka jobów (`frontend-linting`, `build-frontend`, `backend-linting`, `backend-integration-test`). Reguła ochrony gałęzi wymaga podania nazw checków, które muszą przejść. Wymieniać wszystkie joby osobno jest niewygodnie: każda zmiana listy jobów wymagałaby zmiany ustawień w GitHubie. Do tego pominięty (`skipped`) job nie powinien być traktowany jako sukces.

### Decyzja

Własny job `all-tests-check` w `ci.yml`:

- `needs` wskazuje wszystkie pozostałe joby,
- `if: always()`, żeby job uruchamiał się także wtedy, gdy któryś z poprzednich zawiedzie,
- krok kończy się błędem, gdy którykolwiek z jobów ma wynik `failure`, `cancelled` lub `skipped`.

Jako jedyny wymagany check w rulesecie służy ten job (patrz ADR-003).

### Konsekwencje

- Jedna stabilna nazwa checka do wymagania; ustawienia w GitHubie nie zmieniają się przy dodaniu jobu.
- Brak dodatkowej zależności od zewnętrznego kodu w pipeline (mniejsze ryzyko łańcucha dostaw).
- Trzeba pamiętać o dopisaniu każdego nowego joba do `needs`; inaczej nie będzie objęty bramką.

**Odrzucone alternatywy:**

- *Gotowa akcja zewnętrzna z Marketplace, która robi to samo* — dodaje zależność od cudzego kodu, a logika jest na tyle prosta (kilka linii), że łatwiej utrzymać ją we własnym workflow.
- *Wymaganie w rulesecie każdego joba osobno* — każda zmiana nazw lub listy jobów wymaga zmian poza repozytorium.

## ADR-003: Ruleset na `main`

- **Status:** zaakceptowana
- **Data:** 2026-11-06 (data spisania decyzji; ustawienie jest w GitHubie, nie w repozytorium)

### Kontekst

Gałąź `main` jest wersją, z której powstają obrazy i do której odnosi się CI (push i pull request na `main`). Bez ochrony błąd lub wypchnięcie bez przejścia CI trafiają od razu na `main`.

### Decyzja

Ruleset na `main` wymaga:

- zmian przez pull request (brak bezpośrednich pushy),
- przejścia statusu `all-tests-check` (patrz ADR-002).

### Konsekwencje

- Każda zmiana na `main` przechodzi przez CI, a widoczny wynik to jeden check.
- Dotyczy to także właściciela repozytorium: nawet drobne poprawki idą przez PR.
- Reguła zależy od nazwy checka z ADR-002; zmiana nazwy joba wymaga aktualizacji rulesetu.
- Konfiguracja żyje w ustawieniach GitHuba, a nie w repozytorium, więc ten wpis jest jej jedynym zapisem w kodzie projektu. Zmiana rulesetu wymaga nowego wpisu z odwołaniem do tego.

**Odrzucone alternatywy:**

- *Praca bezpośrednio na `main` bez ochrony* — brak gwarancji, że zmiany przeszły testy.
- *Wymaganie w rulesecie każdego joba osobno* — patrz ADR-002.
