from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date, time

class AttendanceCreateSchema(BaseModel):
    student_id: str = Field(..., description="Reference to student ID")
    grade_id: str = Field(..., description="Reference to grade ID")
    class_id: str = Field(..., description="Reference to class ID")
    scan_date: date = Field(default_factory=date.today, description="Attendance date")
    time: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"), description="Scan time")
    status: str = Field(default="P", description="Attendance status ('P' for present)")
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
class AttendanceResponseSchema(BaseModel):
    id: str
    student_id: str
    grade_id: str
    class_id: str
    scan_date: date
    time: str
    status: str
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None