from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Subscriber
from app.schemas import (
    SubscriberCreate,
    SubscriberDeleteResponse,
    SubscriberEmailToDelete,
    SubscribeResponse,
)


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
        db.rollback()
    return SubscribeResponse(message="ok")


@app.delete(
    "/subscribers",
    response_model=SubscriberDeleteResponse,
    status_code=status.HTTP_200_OK,
)
def delete_subscriber(payload: SubscriberEmailToDelete, db: Session = Depends(get_db)):
    email_to_delete = (
        db.query(Subscriber).filter(Subscriber.email == payload.email.lower()).first()
    )
    if not email_to_delete:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Subscriber not found",
        )
    db.delete(email_to_delete)
    db.commit()
    return SubscriberDeleteResponse(message="ok")


@app.get("/subscribers", response_model=list[SubscriberCreate])
def get_subscribers(db: Session = Depends(get_db)):
    subscribers = db.query(Subscriber).all()
    return [SubscriberCreate(email=subscriber.email) for subscriber in subscribers]
