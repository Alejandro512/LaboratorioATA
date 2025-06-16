# app/routers/ticket_router.py

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ticket_schema import TicketCreate, TicketUpdate, TicketOut
from app.crud import ticket_crud
from app.utils.dependencies import get_current_user
from app.utils.roles import is_user, is_technician, is_admin

from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=dict)
async def create_ticket(data: TicketCreate, current_user=Depends(get_current_user)):
    if not is_user(current_user) and not is_admin(current_user):
        raise HTTPException(403, "Solo usuario o admin pueden crear tickets")
    # Validar que requester sea el mismo user (si no es admin)
    if is_user(current_user) and data.requesterId != current_user["id"]:
        raise HTTPException(403, "No puedes crear tickets para otro usuario")
    new_id = await ticket_crud.create_ticket(data.dict())
    return {"id": new_id, "message": "Ticket creado correctamente"}

@router.put("/{ticket_id}", response_model=dict)
async def update_ticket(ticket_id: str, updates: TicketUpdate, current_user=Depends(get_current_user)):
    ticket = await ticket_crud.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket no encontrado")
    if is_technician(current_user):
        if str(ticket["assignedTechId"]) != current_user["id"]:
            raise HTTPException(403, "No autorizado para este ticket")
    updated = await ticket_crud.update_ticket(ticket_id, updates.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(400, "No se realizaron cambios")
    return {"message": "Ticket actualizado"}

@router.get("/", response_model=list[TicketOut])
async def list_tickets(current_user=Depends(get_current_user)):
    if is_admin(current_user):
        return await ticket_crud.list_all_tickets()
    elif is_user(current_user):
        return await ticket_crud.list_user_tickets(current_user["id"])
    elif is_technician(current_user):
        return await ticket_crud.list_tech_tickets(current_user["id"])
    else:
        raise HTTPException(403, "Acceso denegado")
