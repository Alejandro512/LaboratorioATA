from bson import ObjectId
from fastapi import HTTPException
from app.database import db
from app.models.sensor_model import sensor_document
from app.utils.logs import log_sensor_action

async def create_sensor(data: dict, actor_id: str, actor_role: str):
    # Validar dueño en cualquier colección
    collections = ["users", "technicians", "administrators"]
    owner = None
    for col in collections:
        owner = await db[col].find_one({
            "_id": ObjectId(data["ownerUserId"]),
            "status": "active"
        })
        if owner:
            break

    if not owner:
        raise HTTPException(404, detail="El usuario propietario no existe o está inactivo")

    # Forzar ObjectId para guardar bien relacionado
    data["ownerUserId"] = ObjectId(data["ownerUserId"])

    sensor = sensor_document(data)
    result = await db["sensors"].insert_one(sensor)

    await log_sensor_action(
        sensor_id=result.inserted_id,
        action="created",
        actor_id=actor_id,
        actor_role=actor_role
    )

    return str(result.inserted_id)

async def update_sensor(sensor_id: str, updates: dict, actor_id: str, actor_role: str):
    result = await db["sensors"].update_one(
        {"_id": ObjectId(sensor_id)},
        {"$set": updates}
    )
    if result.modified_count > 0:
        await log_sensor_action(sensor_id=sensor_id, action="updated", actor_id=actor_id, actor_role=actor_role)
        return True
    return False

async def delete_sensor(sensor_id: str, actor_id: str, actor_role: str):
    result = await db["sensors"].delete_one({"_id": ObjectId(sensor_id)})
    if result.deleted_count > 0:
        await log_sensor_action(sensor_id=sensor_id, action="deleted", actor_id=actor_id, actor_role=actor_role)
        return True
    return False

async def get_sensor_by_id(sensor_id: str):
    return await db["sensors"].find_one({"_id": ObjectId(sensor_id)})

async def list_user_sensors(user_id: str):
    return await db["sensors"].find({"ownerUserId": ObjectId(user_id)}).to_list(100)

async def list_all_sensors():
    return await db["sensors"].find().to_list(100)
