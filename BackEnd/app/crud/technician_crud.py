from app.database import db
from app.utils.auth import hash_password
from app.schemas.technician_schema import TechnicianCreate, TechnicianUpdate
from datetime import datetime
from bson import ObjectId

async def create_technician(tech: TechnicianCreate):
    salt, passwordHash = hash_password(tech.password)
    new_tech = {
        "name": tech.name,
        "lastname": tech.lastname,
        "email": tech.email,
        "phone": tech.phone,
        "salt": salt,
        "passwordHash": passwordHash,
        "role": "technician",
        "createdAt": datetime.utcnow(),
        "status": tech.status
    }
    result = await db["technicians"].insert_one(new_tech)
    return str(result.inserted_id)

async def update_technician(tech_id: str, data: TechnicianUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    result = await db["technicians"].update_one(
        {"_id": ObjectId(tech_id)},
        {"$set": update_data}
    )
    return result.modified_count == 1

async def delete_technician(tech_id: str):
    result = await db["technicians"].update_one(
        {"_id": ObjectId(tech_id)},
        {"$set": {"status": "deleted"}}
    )
    return result.modified_count == 1
