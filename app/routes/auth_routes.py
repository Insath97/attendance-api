from fastapi import APIRouter, HTTPException
from app.services.auth_services import authenticate_admin, logout
from app.schemas.auth_schema import LoginSchema, TokenResponseSchema
from app.models.api_response import ApiResponse

router = APIRouter()

@router.post("/login",response_model=ApiResponse[TokenResponseSchema])
def login(login_data: LoginSchema):
    token_data = authenticate_admin(login_data)
    
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return ApiResponse[TokenResponseSchema](
        status=True,
        message="Login successful",
        data=token_data
    )


@router.post("/logout")
def user_logout():
    return logout()
    