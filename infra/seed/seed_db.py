from pymongo import MongoClient
from datetime import datetime
client = MongoClient("mongodb://localhost:27017")
db = client["bodymatrix_db"]
users = db["users"]
measurements = db["measurements"]

users.insert_one({"email":"test@example.com","password_hash":"<bcrypt hash>", "created_at": datetime.utcnow(), "height_cm":170})
measurements.insert_one({
  "user_id": "test@example.com",
  "type": "body",
  "timestamp": datetime.utcnow(),
  "measurements": {"shoulder_cm": 40, "chest_cm_est": 88, "waist_cm_est": 70},
})
print("seeded")
