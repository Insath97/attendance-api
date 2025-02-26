from app.database.database import admins
from app.schemas.admin_shema import AdminCreateSchema, AdminUpdateSchema, AdminResponseSchema
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from passlib.context import CryptContext

# Password Hasing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password function
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create Admin Service
def create_admin(admin: AdminCreateSchema) -> AdminResponseSchema:
    
    existing_admin = admins.find_one({"email": admin.email})
    
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already exists. Please use a different email.")

    # Convert Pydantic model to dictionary
    admin_data = admin.dict()
    admin_data["password"] = hash_password(admin_data["password"])
    admin_data["created_at"] = datetime.utcnow()
    admin_data["deleted_at"] = None  # Soft delete handling

    # Insert into MongoDB
    result = admins.insert_one(admin_data)
    
    # Convert _id to string
    admin_data["id"] = str(result.inserted_id)  # Use 'id' instead of '_id'
    
    return AdminResponseSchema(**admin_data)  # Return correct schema format

# Get All Admins Service (Exclude Soft Deleted)
def get_all_admins():
    admins_list = admins.find({"deleted_at": None}).to_list(None)
    return [
        AdminResponseSchema(
            id=str(admin["_id"]),
            name=admin["name"],
            email=admin["email"],
            image=admin.get("image"),
            created_at=admin["created_at"]
        ) for admin in admins_list
    ]
    
# Get Admin By ID Service
def get_admin_by_id(admin_id: str) -> AdminResponseSchema:
    admin =  admins.find_one({"_id": ObjectId(admin_id), "deleted_at": None})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return AdminResponseSchema(
        id=str(admin["_id"]),
        name=admin["name"],
        email=admin["email"],
        image=admin["image"],
        created_at=admin["created_at"]
    )

# Update Admin Service
def update_admin(admin_id: str, admin: AdminUpdateSchema) -> AdminResponseSchema:
    update_data = {k: v for k, v in admin.dict().items() if v is not None}
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    update_data["updated_at"] = datetime.utcnow()

    result = admins.update_one(
        {"_id": ObjectId(admin_id), "deleted_at": None},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found or deleted")

    return get_admin_by_id(admin_id)

# Soft Delete Admin Service
def soft_delete_admin(admin_id: str):
    admin = admins.find_one({"_id": ObjectId(admin_id)})  # No 'await' needed
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    result = admins.update_one(
        {"_id": ObjectId(admin_id)}, {"$set": {"deleted_at": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to delete admin")

    return {"message": "Admin deleted successfully"}