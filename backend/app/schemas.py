from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class SubscriberCreate(BaseModel):
    email: EmailStr


class SubscriberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    created_at: datetime
