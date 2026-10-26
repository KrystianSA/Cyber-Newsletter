from pydantic import BaseModel, EmailStr


class SubscriberCreate(BaseModel):
    email: EmailStr


class SubscribeResponse(BaseModel):
    message: str


class SubscriberEmailToDelete(BaseModel):
    email: EmailStr


class SubscriberDeleteResponse(BaseModel):
    message: str
