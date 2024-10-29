import pytest
from pydantic import ValidationError
from fastapi import Response
from fastapi.responses import JSONResponse
from flottille.api.config import AppSettings

# Sample test case to validate AppSettings defaults and environment-based overrides

def test_app_settings_defaults():
    """Test default values in AppSettings."""
    settings = AppSettings()
    
    assert settings.title == "My FastAPI Application"
    assert settings.version == "0.1.0"
    assert settings.debug is False
    assert settings.openapi_url == "/openapi.json"
    assert settings.docs_url == "/docs"
    assert settings.redoc_url == "/redoc"
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000
    assert settings.allowed_hosts == ["*"]
    assert settings.default_response_class == JSONResponse
    assert settings.root_path == ""
    assert settings.root_path_in_servers is True
    assert settings.generate_unique_id_function.__name__ == "default_generate_unique_id"

def test_app_settings_env_override(monkeypatch):
    """Test environment variable overrides for AppSettings."""
    monkeypatch.setenv("APP_TITLE", "Custom FastAPI App")
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("APP_PORT", "8080")
    monkeypatch.setenv("APP_HOST", "127.0.0.1")

    settings = AppSettings()

    assert settings.title == "Custom FastAPI App"
    assert settings.debug is True
    assert settings.port == 8080
    assert settings.host == "127.0.0.1"

def test_app_settings_invalid_port(monkeypatch):
    """Test invalid environment variable type for port, expecting ValidationError."""
    monkeypatch.setenv("APP_PORT", "not_a_number")

    with pytest.raises(ValidationError):
        AppSettings()

def test_app_settings_custom_response_class():
    """Test setting a custom response class."""
    class CustomResponse(Response):
        pass

    settings = AppSettings(default_response_class=CustomResponse)
    assert settings.default_response_class == CustomResponse
