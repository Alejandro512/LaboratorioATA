# app/crud/ticket_crud.py

from bson import ObjectId
from app.database import db
from app.models.ticket_model import ticket_document

async def create_ticket(data: dict):
    ticket = ticket_document(data)
    result = await db["tickets"].insert_one(ticket)
    return str(result.inserted_id)

async def update_ticket(ticket_id: str, updates: dict):
    result = await db["tickets"].update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": updates}
    )
    return result.modified_count > 0

async def get_ticket(ticket_id: str):
    return await db["tickets"].find_one({"_id": ObjectId(ticket_id)})

async def list_user_tickets(user_id: str):
    return await db["tickets"].find({"requesterId": ObjectId(user_id)}).to_list(100)

async def list_tech_tickets(tech_id: str):
    return await db["tickets"].find({"assignedTechId": ObjectId(tech_id)}).to_list(100)

async def list_all_tickets():
    return await db["tickets"].find().to_list(100)

# Busca un técnico disponible
async def get_available_technician():
    return await db["technicians"].find_one({"status": "active"})