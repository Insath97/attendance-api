from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class Classes(BaseModel):
    grade_id: str
    section_name: str
    description : Optional[str]
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
