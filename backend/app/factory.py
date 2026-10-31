from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import DatabaseConnector
from app.models import Base
from app.routes import router


def create_app(connector: DatabaseConnector) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=connector.engine)
        yield

    app = FastAPI(title="Cyber Newsletter API", lifespan=lifespan)
    app.state.connector = connector
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)  # trasy z APIRouter, bez globalnego engine
    return app
