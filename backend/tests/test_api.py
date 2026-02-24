import pytest
from fastapi.testclient import TestClient

from app.models.home import HeatingType, InsulationLevel


def test_create_home(client: TestClient):
    response = client.post(
        "/api/homes",
        json={
            "size_sqm": 120,
            "year_built": 1995,
            "heating_type": HeatingType.GAS.value,
            "insulation": InsulationLevel.PARTIAL.value,
            "notes": "Single family",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["size_sqm"] == 120
    assert data["year_built"] == 1995
    assert data["heating_type"] == "GAS"
    assert data["insulation"] == "PARTIAL"
    assert "id" in data
    assert data["id"] >= 1


def test_get_home(client: TestClient):
    create_resp = client.post(
        "/api/homes",
        json={"size_sqm": 80, "heating_type": HeatingType.ELECTRIC.value},
    )
    assert create_resp.status_code == 200
    home_id = create_resp.json()["id"]

    response = client.get(f"/api/homes/{home_id}")
    assert response.status_code == 200
    assert response.json()["id"] == home_id
    assert response.json()["size_sqm"] == 80


def test_get_home_not_found(client: TestClient):
    response = client.get("/api/homes/99999")
    assert response.status_code == 404


def test_get_home_invalid_id(client: TestClient):
    response = client.get("/api/homes/0")
    assert response.status_code == 422


def test_advice_returns_recommendations(client: TestClient):
    create_resp = client.post(
        "/api/homes",
        json={"size_sqm": 100, "heating_type": HeatingType.OIL.value},
    )
    assert create_resp.status_code == 200
    home_id = create_resp.json()["id"]

    response = client.post(f"/api/homes/{home_id}/advice")
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) >= 1


def test_advice_home_not_found(client: TestClient):
    response = client.post("/api/homes/99999/advice")
    assert response.status_code == 404
