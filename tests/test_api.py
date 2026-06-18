from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_positive():
    response = client.post("/predict", json={"text": "Ce produit est excellent !"})
    assert response.status_code == 200
    assert response.json() == {"label": "POSITIVE", "score": 0.6, "text": "Ce produit est excellent !"}


def test_predict_negative():
    response = client.post("/predict", json={"text": "Ce service est horrible"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "NEGATIVE"
    assert 0.5 <= data["score"] <= 1.0
    assert data["text"] == "Ce service est horrible"


def test_predict_neutral():
    response = client.post("/predict", json={"text": "Le colis est arrivé aujourd'hui."})
    assert response.status_code == 200
    assert response.json()["label"] == "NEUTRAL"


def test_predict_empty_fails():
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
