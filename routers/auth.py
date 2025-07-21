from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import timedelta, datetime
from jose import jwt, JWTError
from passlib.context import CryptContext
from pymongo import MongoClient
import os
from models import User

router = APIRouter()
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["GEO"]
users_collection = db["Users"]

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Schemas ---
class AccountType(str, Enum):
    free = "free"
    pro = "pro"
    pro_plus = "pro plus"

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None
    account_type: AccountType = AccountType.free

class SignInRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(email: str, password: str):
    user_data = users_collection.find_one({"email": email})
    if not user_data:
        return False
    if not verify_password(password, user_data["hashed_password"]):
        return False
    user_data["id"] = str(user_data["_id"])
    return User(**user_data)


@router.post("/signup")
def signup(request: SignupRequest):
    if users_collection.find_one({"email": request.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(request.password)
    users_collection.insert_one({
        "email": request.email,
        "hashed_password": hashed,
        "full_name": request.full_name,
        "account_type": request.account_type,
        "disabled": False
    })
    return {"msg": "User created successfully"}

@router.post("/signin", response_model=Token)
def signin(request: SignInRequest):
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signout")
def signout():
    return {"msg": "Client should delete the JWT token"}
