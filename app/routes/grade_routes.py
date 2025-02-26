from fastapi import HTTPException,APIRouter
from app.services.grade_services import create_grade, update_grade, get_all_grade, get_grade_by_id, soft_delete_grade
from app.schemas.grade_schema import GradeCreateSchema, GradeResponseSchema, GradeUpdateSchema
from typing import List
from app.models.api_response import ApiResponse

router = APIRouter()

# create grade
@router.post("/grades", response_model=ApiResponse[GradeResponseSchema], status_code=201)
def create_grade_route(grade: GradeCreateSchema):
    created_grade = create_grade(grade)
    return ApiResponse[GradeResponseSchema](
        status=True,
        message="Grade created successfull",
        data=created_grade
    )

# get all grades
@router.get("/grades", response_model=ApiResponse[List[GradeResponseSchema]])
def get_all_grade_route():
    grade = get_all_grade()
    return ApiResponse[List[GradeResponseSchema]](
        status=True,
        message="Students retrieved successfully",
        data=grade
    )
    
# get grade by id
@router.get("/grade/{grade_id}", response_model=ApiResponse[GradeResponseSchema])
def get_grade_by_id_route(grade_id: str):
    grade_date = get_grade_by_id(grade_id)
    if not grade_date:
        raise HTTPException(status_code=404, detail="Grade not found")
    return ApiResponse[GradeResponseSchema](
        status=True,
        message="Grade retrieved successfully",
        data=grade_date
    )   

# update grade
@router.put("/garade/{grade_id}", response_model=ApiResponse[GradeResponseSchema])
def update_grade_route(grade_id: str, grade: GradeUpdateSchema):
    updated_grade = update_grade(grade_id, grade)
    if not updated_grade:
        raise HTTPException(status_code=404, detail="Student not found")
    return ApiResponse[GradeResponseSchema](
        status=True,
        message="Student updated successfully",
        data=updated_grade
    )

# delete grade
@router.delete("/grades/{grade_id}", response_model=ApiResponse[None])
def delete_student_route(grade_id: str):
    success = soft_delete_grade(grade_id)
    if not success:
        raise HTTPException(status_code=404, detail="Grade not found or already deleted")
    return ApiResponse[None](
        status=True,
        message="Grade deleted successfully",
        data=None
    )