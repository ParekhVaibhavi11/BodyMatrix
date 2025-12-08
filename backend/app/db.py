from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["bodymatrix_db"]
users_col = db["users"]
measurements_col = db["measurements"]
