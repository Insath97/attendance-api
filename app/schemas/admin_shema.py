from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Admin Create Schema (For Creating New Admin)
class AdminCreateSchema(BaseModel):
    image: Optional[str] = Field(None,description="Profile image URL of the admin")
    name : str = Field(..., min_length=5, max_length=100, description="Admin's Full name")
    email: EmailStr = Field(..., email=True, description="Admin's Email Address")
    password: str = Field(..., min_length=8, max_length=50, description="Admin's Password")
    
# Admin Update Schema (For Updating Admin)
class AdminUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8, max_length=50)
    image: Optional[str] = None
        
# Response schema
class AdminResponseSchema(BaseModel):
    id: str 
    name: str
    email: EmailStr
    image: Optional[str] = None
    created_at: datetime
    
   
   