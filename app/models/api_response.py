from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

# Define a type variable that can be used for any data type
T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    status: bool
    message: str
    data: Optional[T]