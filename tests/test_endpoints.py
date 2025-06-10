import sys
import os

from fastapi.testclient import TestClient

from src import app

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_predictions():
    payload = {
        "Pclass": 1,
        "Sex": "male",
        "Age": 10,
        "Siblings/Spouses_Aboard": 2,
        "Parents/Children_Aboard": 3,
        "Fare": 30.0,
    }

    response = client.post("/get-predictions", json=payload)
    assert response.status_code == 200
    assert "Survived" in response.json()


def test_invalid_payload():
    payload = {
        "Pclass": 12.0,
        "Sex": "unknown",
        "Age": -5,
    }

    response = client.post("/get-predictions", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()
