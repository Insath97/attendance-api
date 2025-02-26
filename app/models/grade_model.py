from pydantic import BaseModel, constr
from typing import Optional
from datetime import date, datetime

class Grade(BaseModel):
    grade_level : int 
    description : Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None