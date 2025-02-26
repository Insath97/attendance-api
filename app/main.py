from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.auth_middleware import JWTAuthenticationMiddleware
from app.routes import admin_routes, auth_routes, student_routes, grade_routes, class_routes, student_assign_class_routes, attendance_routes
from datetime import datetime
from app.utils.security import sri_lankan_now

app = FastAPI(title="School Management API", version="1.0", description="API for managing school attendance, bell systems, and other school-related operations.")

# Allow only specific domains
""" origins = [
    "https://yourfrontenddomain.com", 
] 
 """
# Add JWT authentication middleware globally
""" app.add_middleware(
    JWTAuthenticationMiddleware,
    CORSMiddleware,
    allow_origins=origins,  # Specify the domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],

    ) """

# add time zone
datetime.utcnow() == sri_lankan_now()

# Include the authentication routes
app.include_router(auth_routes.router)

# Include Attendance Routes
app.include_router(attendance_routes.router)

# Include Student Assign to Class
app.include_router(student_assign_class_routes.router) 

# Include Admin Routes
app.include_router(admin_routes.router)

# Include Students Routes
app.include_router(student_routes.router)

# Include Grade Routes
app.include_router(grade_routes.router)

# Include Class Routes
app.include_router(class_routes.router)


    
# Root Endpoint (Optional)
@app.get("/")
def home():
    return {"message": "Welcome to School Management API"}

@app.get("/time")
def get_time():
    return {"current_time": sri_lankan_now()}