from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserModel(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    company: str
    salt: str
    passwordHash: str
    role: str = "user"
    createdAt: datetime
    status: str
