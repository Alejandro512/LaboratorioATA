from fastapi import APIRouter, Depends, HTTPException
from app.schemas.sensor_schema import SensorCreate, SensorUpdate, SensorOut
from app.crud import sensor_crud
from app.utils.dependencies import get_current_user
from app.utils.roles import is_user, is_technician, is_admin
from app.database import db
from bson import ObjectId

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)

@router.post("/", response_model=dict)
async def create_sensor_route(data: SensorCreate, current_user=Depends(get_current_user)):
    if is_user(current_user):
        if data.ownerUserId != current_user["sub"]:  # ✅ usar 'sub'
            raise HTTPException(403, "No puedes crear sensores para otro usuario")
    elif is_technician(current_user):
        ticket = await db["tickets"].find_one({
            "assignedTechId": ObjectId(current_user["sub"]),  # ✅ usar 'sub'
            "requesterId": ObjectId(data.ownerUserId),
            "status": {"$in": ["open", "in_progress"]}
        })
        if not ticket:
            raise HTTPException(403, "No tienes un ticket autorizado para este usuario")
    elif not is_admin(current_user):
        raise HTTPException(403, "Acceso denegado")

    new_id = await sensor_crud.create_sensor(
        data.dict(),
        actor_id=current_user["sub"],   # ✅ usar 'sub'
        actor_role=current_user["role"]
    )

    return {"id": new_id, "message": "Sensor creado correctamente"}

@router.get("/", response_model=list[SensorOut])
async def get_sensors(current_user=Depends(get_current_user)):
    if is_admin(current_user):
        return await sensor_crud.list_all_sensors()
    elif is_user(current_user):
        return await sensor_crud.list_user_sensors(current_user["sub"])  # ✅ usar 'sub'
    else:
        raise HTTPException(403, "Acceso denegado")

@router.put("/{sensor_id}", response_model=dict)
async def update_sensor(sensor_id: str, updates: SensorUpdate, current_user=Depends(get_current_user)):
    sensor = await sensor_crud.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(404, "Sensor no encontrado")
    if current_user["role"] == "user" and str(sensor["ownerUserId"]) != current_user["sub"]:  # ✅ usar 'sub'
        raise HTTPException(403, "Solo el propietario puede modificar este sensor")

    updated = await sensor_crud.update_sensor(
        sensor_id,
        updates.dict(exclude_unset=True),
        current_user["sub"],   # ✅ usar 'sub'
        current_user["role"]
    )
    if not updated:
        raise HTTPException(400, "No se realizaron cambios")

    return {"message": "Sensor actualizado"}

@router.delete("/{sensor_id}", response_model=dict)
async def delete_sensor(sensor_id: str, current_user=Depends(get_current_user)):
    sensor = await sensor_crud.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(404, "Sensor no encontrado")
    if current_user["role"] == "user" and str(sensor["ownerUserId"]) != current_user["sub"]:  # ✅ usar 'sub'
        raise HTTPException(403, "Solo el propietario puede eliminar este sensor")

    deleted = await sensor_crud.delete_sensor(
        sensor_id,
        current_user["sub"],   # ✅ usar 'sub'
        current_user["role"]
    )
    if not deleted:
        raise HTTPException(400, "No se pudo eliminar")

    return {"message": "Sensor eliminado"}
