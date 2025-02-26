from app.database.database import students
from app.schemas.student_schema import StudentCreateSchema, StudentResponseSchema, StudentUpdateSchema
from bson import ObjectId
from fastapi import HTTPException
from typing import List, Union
from pymongo import UpdateOne
from datetime import datetime, date

# create student function
def create_student(student: StudentCreateSchema) -> StudentResponseSchema:
    
    existing_student_index = students.find_one({"index_number": student.index_number})
    
    if existing_student_index:
        raise HTTPException(status_code=400, detail="Index number already exists. Please use a different index number.")
    
    student_data = student.dict()
    
    if isinstance(student_data["dob"], date):
        student_data["dob"] = datetime.combine(student_data["dob"], datetime.min.time())
        
    student_data["deleted_at"] = None  # Soft delete handling
    
    result = students.insert_one(student_data)
    
    student_data["id"] = str(result.inserted_id)
    
    return StudentResponseSchema(**student_data)

# get all student
def get_all_students() -> StudentResponseSchema:
    student_list = students.find({"status": True, "deleted_at": None}).to_list(None)
    
    if not student_list:
        raise HTTPException(status_code=404, detail="No students found.")
    
    response_data = []
    for student in student_list:
        student["id"] = str(student["_id"]) 
        del student["_id"]
        
    response_data = [StudentResponseSchema(**student) for student in student_list]
    return response_data

# get student by id
def get_student_by_id(student_id: str) -> StudentResponseSchema:
    student = students.find_one({"_id":ObjectId(student_id), "status": True, "deleted_at": None})
    
    if not student :
        raise HTTPException(status_code=404, detail="Student not found")
    
    student["id"] = str(student["_id"])
    return StudentResponseSchema(**student)

# get student by index number
def get_student_by_index_number(index_number: str) -> StudentResponseSchema:
    student = students.find_one({"index_number": index_number, "status": True, "deleted_at": None})
    
    if not student :
        raise HTTPException(status_code=404, detail="Student not found")
    
    student["id"] = str(student["_id"])
    return StudentResponseSchema(**student)

# student update
def update_student(student_id : str, student : StudentUpdateSchema) -> StudentResponseSchema :
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    
    if "dob" in update_data and isinstance(update_data["dob"], date):
        update_data["dob"] = datetime.combine(update_data["dob"], datetime.min.time())
        
    update_data["updated_at"] = datetime.utcnow()
    
    result = students.update_one(
        {"_id": ObjectId(student_id), "status": True, "deleted_at": None},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found or inactive")
    
    return get_student_by_id(student_id)

# student soft delete
def soft_delete_student(student_id : str):
    student = students.find_one({"_id": ObjectId(student_id), "deleted_at": None})
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or already deleted")
    
    result = students.update_one(
        {"_id": ObjectId(student_id)}, 
        {"$set": {"deleted_at": datetime.utcnow()}}  # Mark the student as deleted
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to delete student")
    
    return {"message": "Student deleted successfully"}
    
# Change the status of either a single or multiple students to 
def change_students_status(student_ids: Union[str, List[str]]) -> dict:
    if isinstance(student_ids, str):
        # Single student ID, update status to False
        result = students.update_one(
            {"_id": ObjectId(student_ids), "deleted_at": None},
            {"$set": {"status": False}}
        )

        # If the student was not found or status was not changed
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found or already inactive")

        return {"message": "Student status changed to False successfully"}

    elif isinstance(student_ids, list):
        # Multiple student IDs, update status to False for each
        update_operations = [
            UpdateOne({"_id": ObjectId(student_id), "deleted_at": None}, {"$set": {"status": False}})
            for student_id in student_ids
        ]
        
        # Perform the batch update (bulk_write)
        result = students.bulk_write(update_operations)

        # If no students were modified, return an error
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="No students found or already inactive")

        return {"message": f"{result.modified_count} students' status changed to inactive successfully"}

    else:
        raise HTTPException(status_code=400, detail="Invalid input, must be a list or string")



      
    