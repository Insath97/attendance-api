import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configurations
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME","school_db")

# JWT Configurations
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Sri lanakan timezone
os.environ["TZ"] = os.getenv("TZ","Asia/Colombo")