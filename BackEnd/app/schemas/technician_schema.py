from pydantic import BaseModel, EmailStr
from datetime import datetime

class TechnicianCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    phone: str
    password: str
    status: str = "active"

class TechnicianUpdate(BaseModel):
    name: str | None = None
    lastname: str | None = None
    phone: str | None = None
    status: str | None = None

class TechnicianOut(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    phone: str
    role: str
    createdAt: datetime
    status: str
