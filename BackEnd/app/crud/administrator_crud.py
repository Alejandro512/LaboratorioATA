from app.database import db
from app.schemas.administrator_schema import AdministratorCreate
from app.schemas.administrator_schema import AdministratorUpdate
from app.utils.auth import hash_password
from datetime import datetime
from bson import ObjectId

async def create_administrator(admin: AdministratorCreate):
    salt, passwordHash = hash_password(admin.password)
    new_admin = {
        "name": admin.name,
        "lastname": admin.lastname,
        "email": admin.email,
        "salt": salt,
        "passwordHash": passwordHash,
        "role": "administrator",
        "createdAt": datetime.utcnow(),
        "status": admin.status
    }
    result = await db["administrators"].insert_one(new_admin)
    return str(result.inserted_id)

async def update_administrator(admin_id: str, data: AdministratorUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        return False  # nada que actualizar

    result = await db["administrators"].update_one(
        {"_id": ObjectId(admin_id)},
        {"$set": update_data}
    )
    return result.modified_count == 1

async def delete_administrator(admin_id: str):
    result = await db["administrators"].update_one(
        {"_id": ObjectId(admin_id)},
        {"$set": {"status": "deleted"}}
    )
    return result.modified_count == 1
