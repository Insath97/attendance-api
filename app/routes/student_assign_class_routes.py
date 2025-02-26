from fastapi import APIRouter, HTTPException, Depends
from typing import List, Union
from app.models.api_response import ApiResponse
from app.schemas.student_class_assign_schema import (
    StudentClassAssignmentCreateSchema, 
    StudentClassAssignmentUpdateSchema, 
    UnassignedStudentResponseSchema,
    StudentClassAssignmentResponseSchema
)

from app.services.students_class_assign_services import assign_students_to_class, list_unassigned_students, update_student_assignment, remove_student_assignment
from bson import ObjectId

router = APIRouter()

# Get unassigned students
@router.post("/students/assign", response_model=ApiResponse)
def assign_students_to_class_route(
    assignment_data: StudentClassAssignmentCreateSchema
):
    """
    Assign one or many students to a class for a specific academic year.
    """
    try:
        result = assign_students_to_class(assignment_data)
        return ApiResponse(
            status=True,
            message=result["message"],
            data={"assigned_count": len(result["assignments"]), "skipped": result["skipped"]}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/students/unassigned", response_model=ApiResponse[List[UnassignedStudentResponseSchema]])
def get_unassigned_students_route():
    """
    Get a list of students who are not assigned to any class or grade.
    """
    try:
        unassigned_students = list_unassigned_students()
        return ApiResponse[List[UnassignedStudentResponseSchema]](
            status=True,
            message="Unassigned students retrieved successfully",
            data=unassigned_students
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/students/assignments/{assignment_id}", response_model=ApiResponse[StudentClassAssignmentResponseSchema])
def update_student_assignment_route(
    assignment_id: str, 
    update_data: StudentClassAssignmentUpdateSchema
):
    """
    Update a student's class assignment.
    """
    try:
        result = update_student_assignment(assignment_id, update_data)
        return ApiResponse[StudentClassAssignmentResponseSchema](
            status=True,
            message="Assignment updated successfully",
            data=result
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/students/{student_id}/remove", response_model=ApiResponse)
def remove_student_assignment_route(student_id: str):
    """
    Remove a student's class assignment.
    """
    try:
        result = remove_student_assignment(student_id)
        return ApiResponse(
            status=True,
            message=result["message"],
            data=None
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

