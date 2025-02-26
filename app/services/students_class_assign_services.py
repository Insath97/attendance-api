from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson import ObjectId, errors
from typing import List, Union
from pymongo import UpdateOne
from datetime import datetime
from app.database.database import students, student_class_assignments
from app.schemas.student_schema import StudentResponseSchema
from app.schemas.student_class_assign_schema import (
    StudentClassAssignmentCreateSchema, 
    StudentClassAssignmentResponseSchema, 
    StudentClassAssignmentUpdateSchema, 
    UnassignedStudentResponseSchema
)

# Assign Students to Class
def assign_students_to_class(
    assignment_data: StudentClassAssignmentCreateSchema
) -> dict:
    """
    Assign one or many students to a class for a specific academic year.
    """
    try:
        # Convert single student ID to a list for uniform processing
        if isinstance(assignment_data.student_ids, str):
            student_ids = [assignment_data.student_ids]
        else:
            student_ids = assignment_data.student_ids

        # Validate ObjectId format
        try:
            student_ids = [ObjectId(sid) for sid in student_ids]
            grade_id = ObjectId(assignment_data.grade_id)
            class_id = ObjectId(assignment_data.class_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        # Validate students
        valid_students = list(students.find({"_id": {"$in": student_ids}, "status": True, "deleted_at": None}))
        if len(valid_students) != len(student_ids):
            raise HTTPException(status_code=404, detail="One or more students not found or inactive")

        # Check if students are already assigned to a class for the same academic year
        existing_assignments = student_class_assignments.find({
            "student_id": {"$in": student_ids},
            "academic_year": assignment_data.academic_year
        })
        already_assigned_students = {doc["student_id"] for doc in existing_assignments}

        # Prepare assignments for unassigned students
        assignments = [
            {
                "student_id": student_id,
                "grade_id": grade_id,
                "class_id": class_id,
                "academic_year": assignment_data.academic_year,
                "created_at": assignment_data.created_at,  # Use the timestamp from the schema
                "updated_at": None,
                "deleted_at": None
            }
            for student_id in student_ids
            if student_id not in already_assigned_students
        ]

        # Insert assignments into the collection
        if assignments:
            student_class_assignments.insert_many(assignments)

        return {
            "message": f"{len(assignments)} students assigned successfully",
            "assigned_count": len(assignments),  # Add assigned_count to the response
            "skipped": len(student_ids) - len(assignments)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# List Unassigned Students
def list_unassigned_students() -> List[UnassignedStudentResponseSchema]:
    """
    List students who are not assigned to any class or grade.
    """
    try:
        # Fetch all active students
        active_students = list(students.find({"status": True, "deleted_at": None}))

        # Fetch all assigned student IDs
        assigned_student_ids = set(student_class_assignments.distinct("student_id"))

        # Filter out unassigned students
        unassigned_students = [
            student for student in active_students 
            if student["_id"] not in assigned_student_ids
        ]

        # Convert to response schema
        return [
            UnassignedStudentResponseSchema(
                id=str(student["_id"]),
                name=student["name"],
                index_number=student["index_number"]
            )
            for student in unassigned_students
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Update Student Assignment
def update_student_assignment(
    assignment_id: str, 
    update_data: StudentClassAssignmentUpdateSchema
) -> StudentClassAssignmentResponseSchema:
    """
    Update a student's class assignment.
    """
    try:
        # Validate ObjectId format
        try:
            assignment_id = ObjectId(assignment_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        # Prepare update fields
        update_fields = {k: v for k, v in update_data.dict().items() if v is not None}
        update_fields["updated_at"] = datetime.utcnow()

        # Update the assignment
        result = student_class_assignments.update_one(
            {"_id": assignment_id},
            {"$set": update_fields}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Fetch the updated assignment
        updated_assignment = student_class_assignments.find_one({"_id": assignment_id})
        updated_assignment["id"] = str(updated_assignment["_id"])

        # Return the response
        return StudentClassAssignmentResponseSchema(**updated_assignment)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def remove_student_assignment(student_id: str) -> dict:
    """
    Remove a student's class assignment.
    """
    try:
        # Validate ObjectId format
        try:
            student_id = ObjectId(student_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")

        # Delete the assignment
        result = student_class_assignments.delete_one({"student_id": student_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student assignment not found")

        return {"message": "Student assignment removed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))