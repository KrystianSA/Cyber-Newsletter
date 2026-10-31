import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import DatabaseConnector
from app.factory import create_app
from app.models import Base, Subscriber


@pytest.fixture(scope="session")
def test_db():
    connector = DatabaseConnector("TEST_DATABASE_URL")
    if not connector.engine.url.database.endswith("_test"):
        pytest.exit("TEST_DATABASE_URL musi wskazywać bazę kończącą się na _test")
    return connector


@pytest.fixture(scope="session")
def app(test_db):
    return create_app(test_db)


@pytest.fixture(autouse=True)
def clean_db(test_db):
    Base.metadata.create_all(bind=test_db.engine)
    with test_db.engine.begin() as conn:
        conn.execute(text("TRUNCATE subscribers RESTART IDENTITY"))


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db(test_db):
    session = test_db.SessionLocal()
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
