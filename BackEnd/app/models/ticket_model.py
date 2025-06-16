# app/models/ticket_model.py

from datetime import datetime

def ticket_document(data: dict) -> dict:
    return {
        "requesterId": data["requesterId"],
        "assignedTechId": data.get("assignedTechId"),  # puede ser None al crear
        "alertId": data.get("alertId"),  # opcional
        "subject": data["subject"],
        "description": data["description"],
        "priority": data["priority"],
        "status": data.get("status", "open"),  # por defecto abierto
        "history": data.get("history", []),  # lista de cambios
        "meeting": data.get("meeting"),  # opcional: {date, link}
        "createdAt": datetime.utcnow()
    }
