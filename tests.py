import pytest
from fastapi.testclient import TestClient

from main import app
from sea_routes.dependencies import get_sea_routes_repo
from sea_routes.exceptions import RouteNotFoundException
from sea_routes.models import RouteModel


class MockSeaRoutesRepository:
    async def get_all_routes(self):
        return [
            RouteModel(
                route_id=1, from_port="Port A", to_port="Port B", leg_duration=5
            ),
            RouteModel(
                route_id=2, from_port="Port C", to_port="Port D", leg_duration=3
            ),
        ]

    async def get_route(self, id):
        if id == 1:
            return {"features": [{"geometry": {"coordinates": [10.0, 20.0]}}]}
        raise RouteNotFoundException(id)


@pytest.fixture
def client():
    app.dependency_overrides[get_sea_routes_repo] = lambda: MockSeaRoutesRepository()
    with TestClient(app) as c:
        yield c


def test_get_all_routes(client):
    response = client.get("/routes")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["from_port"] == "Port A"


def test_get_route_found(client):
    response = client.get("/routes/1")
    assert response.status_code == 200
    assert "features" in response.json()
    assert response.json()["features"][0]["geometry"]["coordinates"] == [10.0, 20.0]


def test_get_route_not_found(client):
    response = client.get("/routes/999")
    assert response.status_code == 404
    assert (
        response.json()["message"]
        == "No route with id 999 has been found. Try accessing different id or view the list of ids by using /routes endpoint."
    )
