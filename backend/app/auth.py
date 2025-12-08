from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .config import JWT_SECRET
from .db import users_col

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/api/auth")

def create_token(data: dict, expires_minutes: int = 60*24):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

async def get_user_by_email(email: str):
    return await users_col.find_one({"email": email})

@router.post("/register")
async def register(payload: dict):
    if await users_col.find_one({"email": payload["email"]}):
        raise HTTPException(status_code=400, detail="User exists")
    pwd = pwd_ctx.hash(payload["password"])
    user = {"email": payload["email"], "password_hash": pwd, "created_at": datetime.utcnow()}
    res = await users_col.insert_one(user)
    return {"ok": True}

@router.post("/login")
async def login(payload: dict):
    user = await get_user_by_email(payload["email"])
    if not user or not pwd_ctx.verify(payload["password"], user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": str(user["_id"]), "email": user["email"]})
    return {"token": token}

# dependency
from fastapi import Request
async def get_current_user(request: Request):
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing auth")
    try:
        scheme, token = auth.split()
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        user = await users_col.find_one({"_id": user_id}) if False else await users_col.find_one({"email": payload.get("email")})
        # simpler: fetch by email
        if not user: raise
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
