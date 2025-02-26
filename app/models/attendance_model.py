from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time

class Attendance(BaseModel):
    student_id: str
    grade_id: str
    class_id: str
    index_number: str
    date: date
    time: time
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    