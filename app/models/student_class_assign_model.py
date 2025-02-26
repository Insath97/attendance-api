from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class StudentClassAssignment(BaseModel):
    student_id: str
    grade_id: str
    class_id: str
    academic_year: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None