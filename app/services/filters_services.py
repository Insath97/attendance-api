from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError, PyMongoError
from app.database.database import student_class_assignments, classes, grades,students
from bson import ObjectId
from datetime import datetime
from typing import List, Union, Optional
from app.schemas.student_schema import StudentResponseSchema
from app.schemas.student_class_assign_schema import StudentClassAssignmentCreateSchema, StudentClassAssignmentResponseSchema, StudentClassAssignmentUpdateSchema

# retrieve students based on grade, class, and year.
def filter_students(grade_id: Optional[str] = None, class_id: Optional[str] = None, academic_year: Optional[int] = None):
    try:
        # Build the query based on provided filters
        query = {}
        if grade_id:
            query["grade_id"] = grade_id
        if class_id:
            query["class_id"] = class_id
        if academic_year:
            query["academic_year"] = academic_year

        # Retrieve assignments matching the query
        assignments = list(student_class_assignments.find(query))

        # Join data from students, grades, and classes collections
        result = []
        for assignment in assignments:
            student = students.find_one({"_id": ObjectId(assignment["student_id"])})
            grade = grades.find_one({"_id": ObjectId(assignment["grade_id"])})
            class_info = classes.find_one({"_id": ObjectId(assignment["class_id"])})
            if student and grade and class_info:
                result.append({
                    "student_id": str(student["_id"]),
                    "student_name": student["name"],
                    "student_index_number":student["index_number"],
                    "grade_id": str(grade["_id"]),
                    "grade_level": grade["grade_level"],
                    "class_id": str(class_info["_id"]),
                    "class_name": class_info["section_name"],
                    "academic_year": assignment["academic_year"]
                })

        return result

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
# retrieve a student's class and grade details by their index number.
def get_all_students_with_class_details():
    try:
        # Fetch all active students
        students_data = students.find({"status": True, "deleted_at": None})
        
        all_students = []
        for student in students_data:
            student_id_str = str(student["_id"])

            # Find the latest class assignment
            assignment = student_class_assignments.find_one(
                {"student_id": student_id_str, "deleted_at": None},
                sort=[("academic_year", -1)]  # Get the latest assignment
            )

            # If the student has an assignment, get grade and class details
            if assignment:
                grade = grades.find_one({"_id": ObjectId(assignment["grade_id"])})
                class_info = classes.find_one({"_id": ObjectId(assignment["class_id"])})

                student["grade_level"] = grade["grade_level"] if grade else None
                student["class_name"] = class_info["section_name"] if class_info else None
                student["academic_year"] = assignment["academic_year"]
            else:
                student["grade_level"] = None
                student["class_name"] = None
                student["academic_year"] = None

            # Convert ObjectId to string
            student["id"] = student_id_str
            all_students.append(StudentResponseSchema(**student))

        return all_students

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")