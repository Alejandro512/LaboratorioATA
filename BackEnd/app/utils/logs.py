from bson import ObjectId
from datetime import datetime
from app.database import db

async def log_sensor_action(
    sensor_id: str,
    action: str,
    actor_id: str,
    actor_role: str,
    details: dict = None  
):
    log = {
        "sensorId": ObjectId(sensor_id),
        "action": action,
        "actorId": ObjectId(actor_id),
        "actorRole": actor_role,
        "timestamp": datetime.utcnow(),
        "details": details or {}  
    }
    await db["sensorLogs"].insert_one(log)
