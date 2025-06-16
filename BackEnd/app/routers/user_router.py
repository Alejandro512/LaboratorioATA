from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserCreate, UserUpdate
from app.crud.user_crud import create_user, update_user, delete_user
from app.utils.dependencies import get_current_user
from app.database import db

router = APIRouter()

# 🚀 Registro público de usuarios
@router.post("/register", summary="Registro público de usuario")
async def public_register(user: UserCreate):
    new_id = await create_user(user)
    return {"id": new_id, "message": "Usuario registrado correctamente"}

# 🛡️ Creación interna (solo administrador)
@router.post("/", summary="Crear usuario (solo administrador)")
async def create(user: UserCreate, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    new_id = await create_user(user)
    return {"id": new_id, "message": "Usuario creado correctamente"}

# 🛡️ Actualizar usuario (solo administrador)
@router.put("/{user_id}", summary="Actualizar usuario")
async def update(user_id: str, data: UserUpdate, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    updated = await update_user(user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o sin cambios")
    return {"message": "Usuario actualizado correctamente"}

# 🛡️ Eliminar usuario (soft delete)
@router.delete("/{user_id}", summary="Eliminar (soft) usuario")
async def delete(user_id: str, current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente (soft delete)"}

# 🛠️ Obtener todos los usuarios (solo administrador)
@router.get("/", summary="Listar usuarios (solo administrador)")
async def list_users(current_user=Depends(get_current_user)):
    if current_user["role"] != "administrator":
        raise HTTPException(status_code=403, detail="Acceso denegado")

    users = await db["users"].find({"status": {"$ne": "deleted"}}).to_list(100)
    
    # Convertir _id a string en cada documento
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
    
    return users