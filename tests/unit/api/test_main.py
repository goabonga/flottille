from fastapi import FastAPI
from fastapi.testclient import TestClient

from flottille.api.main import app


def test_app_creation():
    """Test that the FastAPI app is created and has the correct configuration."""
    assert isinstance(app, FastAPI)
    assert app.title == "My FastAPI Application"  # Update based on actual `AppSettings`
    assert app.version == "0.1.0"  # Update based on actual `AppSettings`
    assert app.debug is False  # Update based on actual `AppSettings`

def test_root_endpoint():
    """Test the root endpoint response."""
    client = TestClient(app)
    response = client.get("/heartbeat")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}
