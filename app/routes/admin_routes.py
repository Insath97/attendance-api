from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.admin_shema import AdminCreateSchema, AdminResponseSchema, AdminUpdateSchema
from app.services.admin_service import create_admin, get_all_admins, get_admin_by_id, update_admin, soft_delete_admin
from app.models.api_response import ApiResponse

router = APIRouter()

# Create Admin
@router.post("/admin", response_model=ApiResponse[AdminResponseSchema], status_code=201)
def create_new_admin(admin: AdminCreateSchema):
    created_admin = create_admin(admin)
    return ApiResponse[AdminResponseSchema](
        status=True,
        message="Admin created successfully",
        data=created_admin
    )

# Get All Admins
@router.get("/admin", response_model=ApiResponse[List[AdminResponseSchema]])
def get_all_admin():
    admins = get_all_admins()
    return ApiResponse[List[AdminResponseSchema]](
        status=True,
        message="Admins retrieved successfully",
        data=admins
    )

# Get Admin By ID
@router.get("/admin/{admin_id}", response_model=ApiResponse[AdminResponseSchema])
def get_admin(admin_id: str):
    admin_data = get_admin_by_id(admin_id)
    if admin_data is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return ApiResponse[AdminResponseSchema](
        status=True,
        message="Data retrieved successfully",
        data=admin_data
    )

# Update Admin
@router.put("/admin/{admin_id}", response_model=ApiResponse[AdminResponseSchema])
async def update_admin_data(admin_id: str, admin: AdminUpdateSchema):
    data = update_admin(admin_id, admin)
    if data is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return ApiResponse[AdminResponseSchema](
        status=True,
        message="Data updated successfully", 
        data=data
    )

# Soft Delete Admin
@router.delete("/admin/{admin_id}", response_model=ApiResponse[None])
async def delete_admin(admin_id: str):
    success = soft_delete_admin(admin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Admin not found or already deleted")
    return ApiResponse[None](
        status=True,
        message="Data deleted successfully",
        data=None
    )
