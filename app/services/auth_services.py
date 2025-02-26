from fastapi import HTTPException
from app.database.database import admins
from app.schemas.auth_schema import LoginSchema, TokenResponseSchema, AdminResponseSchema
from app.utils.security import hash_password, verify_password, create_access_token
from bson import ObjectId

def authenticate_admin(login_data: LoginSchema) -> TokenResponseSchema:
    # Validate email and password
    admin = admins.find_one({"email": login_data.email, "deleted_at": None})
    
    if not admin or not verify_password(login_data.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    access_token = create_access_token({"sub": str(admin["_id"])}, expires_delta=None)

    # Prepare response
    admin_response = AdminResponseSchema(
        id=str(admin["_id"]),
        name=admin["name"],
        email=admin["email"],
        image=admin["image"]
    )

    return TokenResponseSchema(access_token=access_token, token_type="bearer", admin=admin_response)

def logout():
    return {"msg": "Successfully logged out"}



