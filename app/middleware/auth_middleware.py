from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth.auth import verify_token

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for docs and login routes
        if request.url.path in ["/docs", "/openapi.json", "/login","/"]:
            return await call_next(request)
        
        # Get the Authorization header
        authorization: str = request.headers.get("Authorization")
        
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Process token here (assuming verify_token function is defined)
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Continue with the request if token is valid
        return await call_next(request)
