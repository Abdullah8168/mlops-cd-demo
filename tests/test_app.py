from app import app


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["application_version"]
    assert data["git_commit"]


def test_prediction():
    response = app.test_client().post("/predict", json={"value": 5})
    assert response.status_code == 200
    assert response.get_json()["prediction"] == 10
