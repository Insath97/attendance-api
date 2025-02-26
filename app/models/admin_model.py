from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class AdminModel(BaseModel):
    image: Optional[str] = None
    name: str
    email: EmailStr
    email_verified_at: Optional[datetime] = None
    password: str
    remember_token: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    