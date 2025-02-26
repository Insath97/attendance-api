from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class Guardian(BaseModel):
    guardian_name : str
    relationship: str
    contact_number: str
    guardian_email : Optional[EmailStr] = None
    
class Student(BaseModel):
    image: Optional[str] = None
    name : str
    dob: datetime
    address: str
    city: str
    index_number: str
    nic: Optional[str] = None
    guardians: List[Guardian]
    status: bool = Field(default=True)
    join_year: Optional[int] = None
    leaving_year: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None