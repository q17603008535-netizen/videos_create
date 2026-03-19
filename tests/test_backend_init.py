def test_backend_imports():
    from backend.main import app
    from backend.config import settings
    assert app is not None
    assert settings is not None


def test_health_endpoint():
    from fastapi.testclient import TestClient
    from backend.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
