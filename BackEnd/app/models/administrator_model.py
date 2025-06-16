from bson import ObjectId
from pydantic import BaseModel

class AdministratorModel(BaseModel):
    name: str
    lastname: str
    email: str
    salt: str
    passwordHash: str
    role: str = "administrator"
    createdAt: str
    status: str
