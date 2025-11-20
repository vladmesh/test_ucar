from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.models.incident import Incident, IncidentStatus
from app.schemas.incident import IncidentCreate, IncidentResponse, IncidentUpdate

router = APIRouter()


@router.post(
    "/incidents/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED
)
async def create_incident(
    incident: IncidentCreate, session: AsyncSession = Depends(get_async_session)
):
    new_incident = Incident(**incident.model_dump())
    session.add(new_incident)
    await session.commit()
    await session.refresh(new_incident)
    return new_incident


@router.get("/incidents/", response_model=List[IncidentResponse])
async def get_incidents(
    status: Optional[IncidentStatus] = Query(None, description="Фильтр по статусу"),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Incident)
    if status:
        query = query.where(Incident.status == status)

    result = await session.execute(query)
    return result.scalars().all()


@router.patch("/incidents/{incident_id}", response_model=IncidentResponse)
async def update_incident_status(
    incident_id: int,
    incident_update: IncidentUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Incident).where(Incident.id == incident_id)
    result = await session.execute(query)
    incident = result.scalars().first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident.status = incident_update.status
    await session.commit()
    await session.refresh(incident)
    return incident
