from pydantic import BaseModel, EmailStr
from datetime import datetime

class TechnicianModel(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    phone: str
    salt: str
    passwordHash: str
    role: str = "technician"
    createdAt: datetime
    status: str
