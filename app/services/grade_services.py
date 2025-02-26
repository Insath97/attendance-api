from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError, PyMongoError
from app.schemas.grade_schema import GradeCreateSchema, GradeUpdateSchema, GradeResponseSchema
from app.database.database import grades
from bson import ObjectId
from typing import List, Union
from datetime import datetime, date

# create grade 
def create_grade(grade: GradeCreateSchema) -> GradeResponseSchema:
    try:
        # Check if the grade already exists
        existing_grade = grades.find_one({"grade_level": grade.grade_level})
        if existing_grade:
            raise HTTPException(status_code=400, detail="Grade already exists. Please use a different grade.")

        # Convert to dictionary and add timestamps
        grade_data = grade.model_dump()
        grade_data["created_at"] = datetime.utcnow()
        grade_data["updated_at"] = None
        grade_data["deleted_at"] = None

        # Insert the new grade into MongoDB
        result = grades.insert_one(grade_data)
        grade_data["id"] = str(result.inserted_id)  # Convert ObjectId to string

        # Return response
        return GradeResponseSchema(**grade_data)

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Duplicate key error: Grade already exists.")

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# get all grade
def get_all_grade() -> GradeResponseSchema:
    try:
        grade_list = list(grades.find({"deleted_at": None}))  
      
        if not grade_list:
            raise HTTPException(status_code=404, detail="No grades found.")

        for grade in grade_list:
            grade["id"] = str(grade["_id"]) 
            del grade["_id"]  

        return [GradeResponseSchema(**grade) for grade in grade_list]

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# get grade by id 
def get_grade_by_id(grade_id: str) -> GradeResponseSchema:
    try:
        grade_list = grades.find_one({"_id":ObjectId(grade_id), "deleted_at": None})
        
        if not grade_list :
            raise HTTPException(status_code=404, detail="Student not found")
    
        grade_list["id"] = str(grade_list["_id"])
        return GradeResponseSchema(**grade_list)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
# update grade
def update_grade(grade_id: str, grade: GradeUpdateSchema) -> GradeResponseSchema:
    
    try:
        update_data = {k: v for k, v in grade.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = grades.update_one(
            {"_id": ObjectId(grade_id), "deleted_at": None},
            {"$set": update_data}
        )
        
        if result.matched_count:
            return get_grade_by_id(grade_id)
    
        else:
            raise HTTPException(status_code=404, detail="Grade not found or no changes made")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# soft delete
def soft_delete_grade(grade_id: str):
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(grade_id):
            raise HTTPException(status_code=400, detail="Invalid grade ID format")

        # Check if the grade exists and is not already deleted
        grade = grades.find_one({"_id": ObjectId(grade_id), "deleted_at": None})

        if not grade:
            raise HTTPException(status_code=404, detail="Grade not found or already deleted")

        # Soft delete by setting `deleted_at`
        result = grades.update_one(
            {"_id": ObjectId(grade_id)},
            {"$set": {"deleted_at": datetime.utcnow()}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to delete grade")

        return {"message": "Grade deleted successfully"}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
   


    
          