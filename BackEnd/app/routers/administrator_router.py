from fastapi import APIRouter, HTTPException, Depends
from app.schemas.administrator_schema import AdministratorCreate, AdministratorUpdate
from app.crud.administrator_crud import create_administrator, update_administrator, delete_administrator
from app.utils.dependencies import get_current_user  # ← token JWT

router = APIRouter()

@router.post("/", summary="Crear un nuevo administrador")
async def create(admin: AdministratorCreate, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    new_id = await create_administrator(admin)
    return {"id": new_id, "message": "Administrador creado correctamente"}

@router.put("/{admin_id}", summary="Actualizar un administrador")
async def update(admin_id: str, data: AdministratorUpdate, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    updated = await update_administrator(admin_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Administrador no encontrado o sin cambios")
    return {"message": "Administrador actualizado correctamente"}

@router.delete("/{admin_id}", summary="Eliminar (soft) un administrador")
async def delete(admin_id: str, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    deleted = await delete_administrator(admin_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return {"message": "Administrador eliminado correctamente (soft delete)"}
