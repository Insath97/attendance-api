from pydantic import BaseModel, constr, Field, validator
from typing import Optional
from datetime import date, datetime

# create schema
class GradeCreateSchema(BaseModel):
    grade_level : int = Field(..., description="Grade level, e.g., 1, 2, 3")
    description : Optional[str] = Field(None, description="Optional description for the grade")
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

# update schema
class GradeUpdateSchema(BaseModel):
    grade_level : Optional[int] = Field(..., description="Grade level, e.g., 1, 2, 3")
    description : Optional[str] = Field(None, description="Optional description for the grade")
    updated_at: Optional[datetime] = datetime.utcnow()

# response schema
class GradeResponseSchema(BaseModel):
    id: str
    grade_level : int 
    description : Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None