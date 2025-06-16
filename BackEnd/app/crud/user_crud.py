from app.database import db
from app.utils.auth import hash_password
from app.schemas.user_schema import UserCreate, UserUpdate
from datetime import datetime
from bson import ObjectId

async def create_user(user: UserCreate):
    salt, passwordHash = hash_password(user.password)
    new_user = {
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email,
        "company": user.company,
        "salt": salt,
        "passwordHash": passwordHash,
        "role": "user",
        "createdAt": datetime.utcnow(),
        "status": user.status
    }
    result = await db["users"].insert_one(new_user)
    return str(result.inserted_id)

async def update_user(user_id: str, data: UserUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    return result.modified_count == 1

async def delete_user(user_id: str):
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"status": "deleted"}}
    )
    return result.modified_count == 1
