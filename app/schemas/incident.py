from datetime import datetime
from pydantic import BaseModel, Field
from app.models.incident import IncidentStatus, IncidentSource

class IncidentBase(BaseModel):
    description: str = Field(..., min_length=1, description="Описание инцидента")
    source: IncidentSource
    status: IncidentStatus = IncidentStatus.OPEN

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: IncidentStatus

class IncidentResponse(IncidentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

