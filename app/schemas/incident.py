from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
