from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime

# assign studnets to class
class StudentClassAssignmentCreateSchema(BaseModel):
    student_ids: Union[str, List[str]] = Field(..., description="List of student IDs or a single student ID")
    grade_id: str = Field(..., description="Reference to the grade's ID")
    class_id: str = Field(..., description="Reference to the class's ID")
    academic_year: int = Field(..., description="Academic year (e.g., 2023)")
    created_at: datetime = datetime.utcnow()
    
# update assign students
class StudentClassAssignmentUpdateSchema(BaseModel):
    student_id: Optional[str] = Field(None, description="Reference to the student's ID")
    grade_id: Optional[str] = Field(None, description="Reference to the grade's ID")
    class_id: Optional[str] = Field(None, description="Reference to the class's ID")
    academic_year: Optional[int] = Field(None, description="Academic year (e.g., 2023)")
    updated_at: datetime = datetime.utcnow()
    
# response
class StudentClassAssignmentResponseSchema(BaseModel):
    id: str
    student_ids: List[str]
    grade_id: str
    class_id: str
    academic_year: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class UnassignedStudentResponseSchema(BaseModel):
    id: str
    name: str
    index_number: str