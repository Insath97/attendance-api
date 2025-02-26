from fastapi import HTTPException, APIRouter
from app.services.class_services import create_class, get_all_classes, get_class_by_id, update_class, soft_delete_class, get_classes_by_grade
from app.schemas.class_schema import ClassResponseSchema, classCreateSchema, ClassUpdateSchema
from typing import List
from app.models.api_response import ApiResponse

router = APIRouter()

# create class 
@router.post("/classes", response_model=ApiResponse[ClassResponseSchema], status_code=201)
def create_class_route(cls: classCreateSchema):
    created_class = create_class(cls)
    return ApiResponse[ClassResponseSchema](
        status=True,
        message="Class created successfully",
        data=created_class
    )
    
# Get All Classes
@router.get("/classes", response_model=ApiResponse[List[ClassResponseSchema]])
def get_all_classes_route():
    classes = get_all_classes()
    return ApiResponse[List[ClassResponseSchema]](
        status=True,
        message="Classes retrieved successfully",
        data=classes
    )

# Get Class by ID
@router.get("/classes/{class_id}", response_model=ApiResponse[ClassResponseSchema])
def get_class_by_id_route(class_id: str):
    class_data = get_class_by_id(class_id)
    if not class_data:
        raise HTTPException(status_code=404, detail="Class not found")
    return ApiResponse[ClassResponseSchema](
        status=True,
        message="Class retrieved successfully",
        data=class_data
    )

# get class by grade
@router.get("/grades/{grade_id}/classes", response_model=ApiResponse[List[ClassResponseSchema]])
def get_classes_by_grade_route(grade_id: str):
   
    classes = get_classes_by_grade(grade_id)
    return ApiResponse[List[ClassResponseSchema]](
        status=True,
        message="Classes retrieved successfully.",
        data=classes
    )
    
# Update Class
@router.put("/classes/{class_id}", response_model=ApiResponse[ClassResponseSchema])
def update_class_route(class_id: str, cls: ClassUpdateSchema):

    updated_class = update_class(class_id, cls)
    if not updated_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return ApiResponse[ClassResponseSchema](
        status=True,
        message="Class updated successfully",
        data=updated_class
    )
    
# Soft Delete Class
@router.delete("/classes/{class_id}", response_model=ApiResponse[None])
def delete_class_route(class_id: str):

    success = soft_delete_class(class_id)
    if not success:
        raise HTTPException(status_code=404, detail="Class not found or already deleted")
    return ApiResponse[None](
        status=True,
        message="Class deleted successfully",
        data=None
    )