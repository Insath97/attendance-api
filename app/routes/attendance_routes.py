from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.attendance_schema import AttendanceCreateSchema, AttendanceResponseSchema
from app.services.attendance_services import mark_attendance, mark_absent_students, get_attendance_by_student
from app.models.api_response import ApiResponse
from pymongo.errors import PyMongoError
from typing import List

router = APIRouter()

# Mark attendance via QR scan
@router.post("/attendance", response_model=ApiResponse[AttendanceResponseSchema], status_code=201)
def mark_attendance_route(attendance_data: AttendanceCreateSchema):
    try:
        attendance_record = mark_attendance(attendance_data)
        return ApiResponse[AttendanceResponseSchema](
            status=True,
            message="Attendance marked successfully",
            data=attendance_record
        )
    except HTTPException as e:
        raise e
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
# Background task to mark absent students
@router.post("/attendance/mark-absent", response_model=ApiResponse[None])
def mark_absent_students_route(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(mark_absent_students)
        return ApiResponse[None](
            status=True,
            message="Background task to mark absentees started",
            data=None
        )
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
# Get attendance records for a student
@router.get("/attendance/student/{student_id}", response_model=ApiResponse[List[AttendanceResponseSchema]])
def get_attendance_by_student_route(student_id: str):
    attendance_records = get_attendance_by_student(student_id)
    return ApiResponse[List[AttendanceResponseSchema]](
        status=True,
        message="Attendance records retrieved successfully",
        data=attendance_records
    )