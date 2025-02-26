from fastapi import APIRouter, HTTPException
from typing import List, Union
from app.schemas.student_schema import StudentCreateSchema, StudentResponseSchema, StudentUpdateSchema
from app.services.student_services import create_student, get_all_students, get_student_by_id, get_student_by_index_number, update_student, soft_delete_student, change_students_status
from app.models.api_response import ApiResponse


router = APIRouter()

# create student
@router.post("/students", response_model=ApiResponse[StudentResponseSchema], status_code=201)
def create_new_student(student : StudentCreateSchema):
    created_student = create_student(student)
    return ApiResponse[StudentResponseSchema](
        status=True,
        message="Student created successfully",
        data=created_student
    )
    
# get all student
@router.get("/students", response_model=ApiResponse[List[StudentResponseSchema]])
def get_all_students_route():
    students = get_all_students()
    return ApiResponse[List[StudentResponseSchema]](
        status=True,
        message="Students retrieved successfully",
        data=students
    )
    
# get student by id
@router.get("/students/{student_id}", response_model=ApiResponse[StudentResponseSchema])
def get_student(student_id: str):
    student_data = get_student_by_id(student_id)
    if not student_data:
        raise HTTPException(status_code=404, detail="Student not found")
    return ApiResponse[StudentResponseSchema](
        status=True,
        message="Student retrieved successfully",
        data=student_data
    )
    
# Update Student
@router.put("/students/{student_id}", response_model=ApiResponse[StudentResponseSchema])
def update_student_route(student_id: str, student: StudentUpdateSchema):
    updated_student = update_student(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return ApiResponse[StudentResponseSchema](
        status=True,
        message="Student updated successfully",
        data=updated_student
    )
    
# Soft Delete Student
@router.delete("/students/{student_id}", response_model=ApiResponse[None])
def delete_student_route(student_id: str):
    success = soft_delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found or already deleted")
    return ApiResponse[None](
        status=True,
        message="Student deleted successfully",
        data=None
    )
    
# Get a student by their index number.
@router.get("/students/index/{index_number}", response_model=ApiResponse[StudentResponseSchema])
def get_student_by_index(index_number: str):
    try:
        student = get_student_by_index_number(index_number)
        return ApiResponse[StudentResponseSchema](
            status=True,
            message="Student retrieved successfully",
            data=student
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Change Student Status
@router.put("/students/status", response_model=ApiResponse[dict])
def change_students_status_route(student_ids: Union[str, List[str]]):
   
    try:
        result = change_students_status(student_ids)
        return ApiResponse[dict](
            status=True,
            message=result["message"],
            data=None
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
