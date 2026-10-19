import os

# Musi być przed jakimkolwiek importem `app`: app.database tworzy engine przy
# imporcie, a load_dotenv() nie nadpisuje już ustawionych zmiennych.
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://test:test@localhost:5433/cyber_newsletter_test",
)
# Bezpiecznik: testy robią TRUNCATE/DROP, nigdy nie na bazie developerskiej.
assert TEST_DATABASE_URL.rsplit("/", 1)[-1].endswith("_test"), (
    "TEST_DATABASE_URL musi wskazywać na bazę o nazwie kończącej się na _test"
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import text  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Subscriber  # noqa: E402


@pytest.fixture(autouse=True)
def clean_db():
    """Znany stan początkowy: tabela istnieje i jest pusta przed każdym testem."""
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE subscribers RESTART IDENTITY"))
    yield


@pytest.fixture
def client():
    # `with` uruchamia lifespan (create_all) tak jak prawdziwy start serwera.
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def count_subscribers(db):
    def _count() -> int:
        db.expire_all()
        return db.query(Subscriber).count()

    return _count
