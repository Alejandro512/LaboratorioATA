from fastapi import APIRouter, HTTPException, Depends
from app.schemas.technician_schema import TechnicianCreate, TechnicianUpdate
from app.crud.technician_crud import create_technician, update_technician, delete_technician
from app.utils.dependencies import get_current_user
from app.database import db

router = APIRouter()

@router.post("/", summary="Crear técnico")
async def create(tech: TechnicianCreate, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    new_id = await create_technician(tech)
    return {"id": new_id, "message": "Técnico creado correctamente"}

@router.put("/{tech_id}", summary="Actualizar técnico")
async def update(tech_id: str, data: TechnicianUpdate, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    updated = await update_technician(tech_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Técnico no encontrado o sin cambios")
    return {"message": "Técnico actualizado"}

@router.delete("/{tech_id}", summary="Eliminar técnico (soft)")
async def delete(tech_id: str, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    deleted = await delete_technician(tech_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    return {"message": "Técnico eliminado correctamente (soft delete)"}

# 🛠️ Crear un solo Tecnico (solo administrador)
@router.post("/", summary="Crear técnico (solo administrador)")
async def create(tech: TechnicianCreate, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    new_id = await create_technician(tech)
    return {"id": new_id, "message": "Técnico creado correctamente"}

# 🛠️ Obtener un técnico (solo administrador)
@router.get("/", summary="Listar técnicos (solo administrador)")
async def list_technicians(current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    technicians = await db["technicians"].find({"status": {"$ne": "deleted"}}).to_list(100)
    for tech in technicians:
        tech["id"] = str(tech["_id"])
        del tech["_id"]
    return technicians