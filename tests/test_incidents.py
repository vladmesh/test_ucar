from httpx import AsyncClient
from app.models.incident import IncidentStatus, IncidentSource


async def test_create_incident(ac: AsyncClient):
    response = await ac.post(
        "/incidents/",
        json={
            "description": "Test Incident",
            "source": IncidentSource.MONITORING,
            "status": IncidentStatus.OPEN,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Test Incident"
    assert data["source"] == IncidentSource.MONITORING
    assert "id" in data
    assert "created_at" in data


async def test_get_incidents(ac: AsyncClient):
    # Create a few incidents
    await ac.post(
        "/incidents/",
        json={
            "description": "Incident 1",
            "source": IncidentSource.OPERATOR,
            "status": IncidentStatus.OPEN,
        },
    )
    await ac.post(
        "/incidents/",
        json={
            "description": "Incident 2",
            "source": IncidentSource.PARTNER,
            "status": IncidentStatus.RESOLVED,
        },
    )

    # Get all incidents
    response = await ac.get("/incidents/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

    # Filter by status
    response = await ac.get("/incidents/?status=resolved")
    assert response.status_code == 200
    data = response.json()
    assert all(item["status"] == IncidentStatus.RESOLVED for item in data)


async def test_update_incident(ac: AsyncClient):
    # Create incident
    create_response = await ac.post(
        "/incidents/",
        json={
            "description": "To be updated",
            "source": IncidentSource.MONITORING,
            "status": IncidentStatus.OPEN,
        },
    )
    incident_id = create_response.json()["id"]

    # Update status
    response = await ac.patch(
        f"/incidents/{incident_id}", json={"status": IncidentStatus.CLOSED}
    )
    assert response.status_code == 200
    assert response.json()["status"] == IncidentStatus.CLOSED

    # Check persistence
    get_response = await ac.get("/incidents/")
    updated_incident = next(i for i in get_response.json() if i["id"] == incident_id)
    assert updated_incident["status"] == IncidentStatus.CLOSED


async def test_update_nonexistent_incident(ac: AsyncClient):
    response = await ac.patch(
        "/incidents/999999", json={"status": IncidentStatus.CLOSED}
    )
    assert response.status_code == 404
