from pydantic import BaseModel, constr, Field
from typing import Optional
from datetime import datetime

# create class 
class classCreateSchema(BaseModel):
    grade_id: str = Field(..., description="Reference to the grade's ID")
    section_name: str = Field(..., description="Class section name (e.g., A, B, C, F)")
    created_at: datetime = datetime.utcnow()

# update class
class ClassUpdateSchema(BaseModel):
    grade_id: Optional[str] = Field(..., description="Reference to the grade's ID")
    section_name: Optional[str] = Field(..., description="Class section name (e.g., A, B, C, F)")
    updated_at: datetime = datetime.utcnow()
    
# response schema
class ClassResponseSchema(BaseModel):
    id: str
    grade_id : str
    section_name: str
    description : Optional[str]
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None