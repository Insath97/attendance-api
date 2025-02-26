from bson import ObjectId, errors
from typing import List
from datetime import datetime, date
from fastapi import HTTPException, status
from app.database.database import students, grades, classes, student_class_assignments, attendance
from pymongo.errors import DuplicateKeyError, PyMongoError
from app.schemas.attendance_schema import AttendanceCreateSchema, AttendanceResponseSchema

def validate_student(student_id: str):
    if not students.find_one({"_id": ObjectId(student_id)}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found!")

def validate_grade(grade_id: str):
    if not grades.find_one({"_id": ObjectId(grade_id)}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found!")

def validate_class(class_id: str):
    if not classes.find_one({"_id": ObjectId(class_id)}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found!")

def mark_attendance(attendance_data: AttendanceCreateSchema) -> AttendanceResponseSchema:
    student_id = attendance_data.student_id
    grade_id = attendance_data.grade_id
    class_id = attendance_data.class_id
    today_date = str(attendance_data.scan_date)
    scan_time = attendance_data.time

    validate_student(student_id)
    validate_grade(grade_id)
    validate_class(class_id)

    existing_attendance = attendance.find_one({
        "student_id": student_id,
        "scan_date": today_date
    })

    if existing_attendance:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attendance already marked for today!")

    new_attendance = {
        "student_id": student_id,
        "grade_id": grade_id,
        "class_id": class_id,
        "scan_date": today_date,
        "time": scan_time,
        "status": "P",
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "deleted_at": None
    }

    result = attendance.insert_one(new_attendance)
    new_attendance["id"] = str(result.inserted_id)
    return AttendanceResponseSchema(**new_attendance)

def mark_absent_students():
    today_date = str(date.today())
    all_students = students.find({}, {"_id": 1, "grade_id": 1, "class_id": 1})

    for student in all_students:
        student_id = str(student["_id"])
        grade_id = student.get("grade_id", "N/A")
        class_id = student.get("class_id", "N/A")

        existing_attendance = attendance.find_one({"student_id": student_id, "scan_date": today_date})

        if not existing_attendance:
            absent_record = {
                "student_id": student_id,
                "grade_id": grade_id,
                "class_id": class_id,
                "scan_date": today_date,
                "time": "00:00:00",
                "status": "A",
                "created_at": datetime.utcnow(),
                "updated_at": None,
                "deleted_at": None
            }
            attendance.insert_one(absent_record)

    return {"message": "Absent students marked successfully!"}

# Get attendance records for a student
def get_attendance_by_student(student_id: str) -> List[AttendanceResponseSchema]:
  
    try:
        ObjectId(student_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid student ID format")

    records = list(attendance.find({"student_id": student_id}))

    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found for this student")

    return [
        AttendanceResponseSchema(
            id=str(record["_id"]),
            student_id=record["student_id"],
            grade_id=record["grade_id"],
            class_id=record["class_id"],
            scan_date=record["date"],
            time=record["time"],
            status=record["status"],
            created_at=record.get("created_at", datetime.utcnow()),
            updated_at=record.get("updated_at"),
            deleted_at=record.get("deleted_at"),
        )
        for record in records
    ]