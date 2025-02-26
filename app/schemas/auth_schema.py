from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class AdminResponseSchema(BaseModel):
    id: str 
    name: str
    email: EmailStr
    image: Optional[str] = None

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., email=True, description="Admin's Email Address")
    password: str = Field(..., min_length=8, max_length=50, description="Admin's Password")
    
class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    admin: AdminResponseSchema