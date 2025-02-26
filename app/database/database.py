from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from app.config.config import MONGO_URI, DATABASE_NAME

# Connect MongoDB
try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client[DATABASE_NAME]
    db.command('ping')
    print("✅ MongoDB Connection Successful!")
except OperationFailure:
    print("❌ MongoDB Connection Failed!")

# Collections
admins = db["admins"]
students = db["students"]
grades = db["grades"]
classes = db["classes"]
student_class_assignments = db["student_class_assignments"]
attendance = db["attendance "]

""" students.create_index("index_number", unique=True) """
