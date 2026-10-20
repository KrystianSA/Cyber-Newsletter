from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Subscriber
from app.schemas import SubscriberCreate, SubscribeResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Cyber Newsletter API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/subscribers", response_model=SubscribeResponse, status_code=201)
def create_subscriber(payload: SubscriberCreate, db: Session = Depends(get_db)):
    db.add(Subscriber(email=payload.email.lower()))
    try:
        db.commit()
    except IntegrityError:
        # Duplikat: ta sama odpowiedź co przy nowym adresie, żeby nie ujawniać,
        # czyj e-mail jest już na liście (enumeracja adresów).
        db.rollback()
    return SubscribeResponse(message="ok")
