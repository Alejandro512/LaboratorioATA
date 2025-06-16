from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdministratorCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str  # Este es el campo plano que se convertirá en hash
    status: str = "active"


class AdministratorOut(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    role: str
    createdAt: datetime
    status: str

class AdministratorUpdate(BaseModel):
    name: str | None = None
    lastname: str | None = None
    status: str | None = None
