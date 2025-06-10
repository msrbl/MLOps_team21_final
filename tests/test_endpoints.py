from fastapi.testclient import TestClient
from src import app

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
        "Siblings_Spouses_Aboard": 2,
        "Parents_Children_Aboard": 3,
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
