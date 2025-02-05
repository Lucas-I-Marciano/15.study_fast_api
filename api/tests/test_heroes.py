from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_reading_heroes():
    response = client.get("/heroes")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_reading_specific_hero():
    response = client.get("/heroes/1")
    assert response.status_code == 200

