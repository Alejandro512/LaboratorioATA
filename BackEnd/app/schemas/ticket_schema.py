from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TicketBase(BaseModel):
    requesterId: str
    assignedTechId: Optional[str] = None
    alertId: Optional[str] = None
    subject: str
    description: str
    priority: str  # low, medium, high, critical
    meeting: Optional[Dict[str, Any]] = None  # {date, link}

class TicketCreate(TicketBase):
    pass  # mismo que base

class TicketUpdate(BaseModel):
    assignedTechId: Optional[str] = None
    status: Optional[str] = None  # open, in_progress, resolved, closed
    history: Optional[List[Dict[str, Any]]] = None
    meeting: Optional[Dict[str, Any]] = None

class TicketOut(TicketBase):
    id: str = Field(..., alias="_id")
    status: str
    history: List[Dict[str, Any]]
    createdAt: datetime

    class Config:
        allow_population_by_field_name = True
