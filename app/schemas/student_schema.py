from pydantic import BaseModel, EmailStr, Field, constr, validator
from datetime import datetime, date
from typing import Optional, List

PHONE_REGEX = r"^(?:\+94|0)?7[0-9]{8}$"

class Guardian(BaseModel):
    name : str = Field(..., description="Guardian Name")
    relationship: str = Field(..., description="Relation Name")
    contact_number: str = Field(..., min_length=1, max_length=20, pattern=PHONE_REGEX ,description="Guardian Phone Number")
    guardian_email : Optional[EmailStr] = Field(None, email=True, description="Guardian Email")
    

# Student Create Schema
class StudentCreateSchema(BaseModel):
    image : str = Field(None, description="Student Image")
    name : str = Field(..., description="Student Name")
    dob: date = Field(..., description="Date of birth")
    address: str = Field(..., min_length=1, max_length=200, description="Student's address")
    city: str = Field(..., min_length=1, max_length=50, description="Student's city")
    index_number: str = Field(..., min_length=1, max_length=20, description="Unique index number")
    nic: Optional[str] = Field(None, pattern=r"^([0-9]{9}[Vv]|[0-9]{12})$", min_length=10, max_length=12, description="Sri Lankan NIC (10 or 12 digits)")
    guardians: List[Guardian] = Field(..., description="List of guardians (at least one required)")
    status: bool = Field(default=True, description="Student status (active/inactive)")
    join_year: Optional[int] = Field(None, ge=2000, le=2100, description="Year student joined")
    created_at: datetime = datetime.utcnow() 
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    @validator('dob', pre=True)
    def convert_dob_to_datetime(cls, value):
        if isinstance(value, date):  # Convert date to datetime if it's a date object
            return datetime.combine(value, datetime.min.time())
        return value

    @validator('dob')
    def validate_dob(cls, value:date):
        if value >= date.today():
            raise ValueError("Date of birth must be in the past!")
        return value
    
    @validator("guardians")
    def validate_guardians(cls, value):
        if len(value) < 1:
            raise ValueError("At least one guardian is required")
        return value
    

# Student Update Schema
class StudentUpdateSchema(BaseModel):
    image: Optional[str] = Field(None, description="Student Image URL (optional)")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Student's full name (optional)")
    dob: Optional[date] = Field(None, description="Date of birth (optional)")

    address: Optional[str] = Field(None, min_length=1, max_length=200, description="Student's address (optional)")
    city: Optional[str] = Field(None, min_length=1, max_length=50, description="Student's city (optional)")

    index_number: Optional[str] = Field(None, min_length=1, max_length=20, description="Student's unique index number (optional)")
    nic: Optional[str] = Field(None, pattern=r"^([0-9]{9}[Vv]|[0-9]{12})$", min_length=10, max_length=12, description="Sri Lankan NIC (10 or 12 digits) (optional)")
    guardians: Optional[List[Guardian]] = Field(None, description="List of guardians (optional)")
    status: Optional[bool] = Field(None, description="Status of the student (active/inactive)")

    join_year: Optional[int] = Field(None, ge=2000, le=2100, description="Year the student joined (optional)")
    leaving_year: Optional[int] = Field(None, ge=2000, le=2100, description="Year the student left (optional)")

    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when data is updated")

    @validator('dob', pre=True)
    def convert_dob_to_datetime(cls, value):
        if isinstance(value, date):  # Convert date to datetime if it's a date object
            return datetime.combine(value, datetime.min.time())
        return value

    @validator('dob', always=True)
    def validate_dob(cls, value):
        if value and value >= date.today():
            raise ValueError("Date of birth must be in the past!")
        return value

    @validator("guardians")
    def validate_guardians(cls, value):
        if value and len(value) < 1:
            raise ValueError("At least one guardian is required")
        return value

    @validator("status", always=True)
    def validate_status(cls, value):
        if value is not None and value not in [True, False]:
            raise ValueError("Status must be either True or False.")
        return value
    
    
# Student Response Schema
class StudentResponseSchema(BaseModel):
    id : str
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
    
    


