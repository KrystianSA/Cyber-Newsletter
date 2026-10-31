import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class DatabaseConnector:
    def __init__(self, database_url_env: str):
        self.database_url = os.environ.get(database_url_env)
        if not self.database_url:
            raise ValueError(f"Environment variable '{database_url_env}' is not set.")

        self.database_url = os.environ[database_url_env].replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
        self.engine = create_engine(self.database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
