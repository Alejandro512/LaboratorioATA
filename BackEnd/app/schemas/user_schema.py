from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str
    company: str
    status: str = "active"

class UserUpdate(BaseModel):
    name: str | None = None
    lastname: str | None = None
    company: str | None = None
    status: str | None = None

class UserOut(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    company: str
    role: str
    createdAt: datetime
    status: str
