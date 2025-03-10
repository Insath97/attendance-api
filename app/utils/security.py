from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import pytz

# Password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password hash
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token creation and verification
def create_access_token(data: dict, expires_delta: timedelta = None) -> str :
    to_encode = data.copy()
    
    if expires_delta :
       expire = datetime.utcnow() + expires_delta
    else : 
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# Verify Token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload["exp"] >= datetime.utcnow().timestamp() else None
    except JWTError:
        return None
    
    
# monkey pacthing time zone
# Define the Sri Lankan timezone (UTC+5:30)
sri_lankan_timezone = pytz.timezone("Asia/Colombo")

# Monkey-patch datetime.utcnow()
def sri_lankan_now():
    # Get the current UTC time
    utc_time = datetime.utcnow()

    # Convert UTC time to Sri Lankan time
    sri_lankan_time = utc_time.replace(tzinfo=pytz.utc).astimezone(sri_lankan_timezone)

    return sri_lankan_time

