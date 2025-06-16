from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId

class Thresholds(BaseModel):
    min: float
    max: float

class SensorBase(BaseModel):
    serial: str
    type: str
    location: str
    thresholds: Thresholds

class SensorCreate(SensorBase):
    ownerUserId: str  # validaremos que exista
    installedAt: Optional[datetime] = None  # por defecto hoy
    status: Optional[Literal["online", "offline", "maintenance"]] = "online"

class SensorUpdate(BaseModel):
    serial: Optional[str]
    type: Optional[str]
    location: Optional[str]
    status: Optional[Literal["online", "offline", "maintenance"]]
    thresholds: Optional[Thresholds]

class SensorOut(SensorBase):
    id: str = Field(..., alias="_id")
    ownerUserId: str
    installedAt: datetime
    status: str

    class Config:
        allow_population_by_field_name = True
