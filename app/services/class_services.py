from fastapi import HTTPException
from app.database.database import classes
from pymongo.errors import DuplicateKeyError, PyMongoError
from app.schemas.class_schema import classCreateSchema, ClassUpdateSchema, ClassResponseSchema
from bson import ObjectId, errors
from typing import List
from datetime import datetime

def create_class(cls: classCreateSchema) -> ClassResponseSchema:
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(cls.grade_id):
            raise HTTPException(status_code=400, detail="Invalid grade_id format")

        # Check if class already exists
        existing_class = classes.find_one({
            "grade_id": ObjectId(cls.grade_id), 
            "section_name": cls.section_name
        })

        if existing_class:
            raise HTTPException(status_code=400, detail="Class already exists for this grade and section.")

        # Prepare class data
        class_data = cls.model_dump()
        class_data["grade_id"] = ObjectId(cls.grade_id)
        class_data["created_at"] = datetime.utcnow()
        class_data["description"] = f"Class {cls.section_name} for grade {cls.grade_id}"  # Add missing description

        # Insert into database
        result = classes.insert_one(class_data)

        # Convert ObjectId to string for response
        class_data["id"] = str(result.inserted_id)
        class_data["grade_id"] = str(class_data["grade_id"])

        return ClassResponseSchema(**class_data)

    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Duplicate key error: Grade already exists.")

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
# get all classes
def get_all_classes() -> List[ClassResponseSchema]:
    try:
        class_list = list(classes.find({"deleted_at": None}))  

        if not class_list:
            raise HTTPException(status_code=404, detail="No classes found.")

        for cls in class_list:
            cls["id"] = str(cls["_id"])  # Convert ObjectId to string
            del cls["_id"]

            # Convert grade_id ObjectId to string if it's an ObjectId
            if isinstance(cls.get("grade_id"), ObjectId):
                cls["grade_id"] = str(cls["grade_id"])

            # Ensure 'description' exists, otherwise add a default
            if "description" not in cls:
                cls["description"] = f"Class {cls['section_name']} for grade {cls['grade_id']}"

        return [ClassResponseSchema(**cls) for cls in class_list]

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    
# Get Class by ID
def get_class_by_id(class_id: str) -> ClassResponseSchema:
    try:
        if not ObjectId.is_valid(class_id):
            raise HTTPException(status_code=400, detail="Invalid class ID.")

        cls = classes.find_one({"_id": ObjectId(class_id), "deleted_at": None})
        
        if not cls:
            raise HTTPException(status_code=404, detail="Class not found.")
    
        cls["id"] = str(cls["_id"])
        return ClassResponseSchema(**cls)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# get class by grade
def get_classes_by_grade(grade_id: str) -> List[ClassResponseSchema]:
    try:
        # Validate grade_id
        if not ObjectId.is_valid(grade_id):
            raise HTTPException(status_code=400, detail="Invalid grade ID.")

        # Find all classes for the given grade_id
        class_list = list(classes.find({"grade_id": ObjectId(grade_id), "deleted_at": None}))

        if not class_list:
            raise HTTPException(status_code=404, detail="No classes found for this grade.")

        # Convert MongoDB documents to Pydantic models
        for cls in class_list:
            cls["id"] = str(cls["_id"])  # Convert ObjectId to string
            del cls["_id"]  # Remove the MongoDB _id field

        return [ClassResponseSchema(**cls) for cls in class_list]

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
# Update Class
def update_class(class_id: str, cls: ClassUpdateSchema) -> ClassResponseSchema:
    try:
        if not ObjectId.is_valid(class_id):
            raise HTTPException(status_code=400, detail="Invalid class ID.")

        update_data = {k: v for k, v in cls.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = classes.update_one(
            {"_id": ObjectId(class_id), "deleted_at": None},
            {"$set": update_data}
        )
        
        if result.matched_count:
            return get_class_by_id(class_id)
        else:
            raise HTTPException(status_code=404, detail="Class not found or no changes made.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Soft Delete Class
def soft_delete_class(class_id: str):
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(class_id):
            raise HTTPException(status_code=400, detail="Invalid class ID format")

        # Check if the class exists and is not already deleted
        cls = classes.find_one({"_id": ObjectId(class_id), "deleted_at": None})

        if not cls:
            raise HTTPException(status_code=404, detail="Class not found or already deleted")

        # Soft delete by setting `deleted_at`
        result = classes.update_one(
            {"_id": ObjectId(class_id)},
            {"$set": {"deleted_at": datetime.utcnow()}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to delete class")

        return {"message": "Class deleted successfully"}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")