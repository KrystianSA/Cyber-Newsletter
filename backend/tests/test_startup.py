from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from app.database import engine
from app.main import app


def test_startup_creates_subscribers_table():
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS subscribers"))
    assert not inspect(engine).has_table("subscribers")

    with TestClient(app):  # start aplikacji uruchamia lifespan -> create_all
        assert inspect(engine).has_table("subscribers")
