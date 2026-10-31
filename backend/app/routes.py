from collections.abc import Iterator

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Subscriber
from app.schemas import (
    SubscriberCreate,
    SubscriberDeleteResponse,
    SubscriberEmailToDelete,
    SubscribeResponse,
)

router = APIRouter()


def get_db(request: Request) -> Iterator[Session]:
    yield from request.app.state.connector.get_db()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/subscribers", response_model=SubscribeResponse, status_code=201)
def create_subscriber(payload: SubscriberCreate, db: Session = Depends(get_db)):
    db.add(Subscriber(email=payload.email.lower()))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    return SubscribeResponse(message="ok")


@router.delete(
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


@router.get("/subscribers", response_model=list[SubscriberCreate])
def get_subscribers(db: Session = Depends(get_db)):
    subscribers = db.query(Subscriber).all()
    return [SubscriberCreate(email=subscriber.email) for subscriber in subscribers]
