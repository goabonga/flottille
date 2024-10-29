import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from flottille.api.builder import FastAPIBuilder
from flottille.api.config import AppSettings


@pytest.fixture
def app_settings():
    """Provides default settings for FastAPIBuilder tests."""
    return AppSettings()

def test_fastapi_builder_basic_setup(app_settings):
    """Test that FastAPIBuilder builds an app with correct settings."""
    builder = FastAPIBuilder(settings=app_settings)
    app = builder.build()
    
    assert isinstance(app, FastAPI)
    assert app.title == app_settings.title
    assert app.version == app_settings.version
    assert app.debug == app_settings.debug
    assert app.openapi_url == app_settings.openapi_url
    assert app.docs_url == app_settings.docs_url
    assert app.redoc_url == app_settings.redoc_url

def test_fastapi_builder_cors_middleware(app_settings, monkeypatch):
    """Test that CORS middleware is added when cors_origins is specified in settings."""
    cors_origins = ["http://example.com", "http://localhost"]
    monkeypatch.setattr(app_settings, "cors_origins", cors_origins)
    
    builder = FastAPIBuilder(settings=app_settings)
    app = builder.build()

    # Debugging: Print all middleware classes in the app
    print("Middleware stack:", [middleware.cls for middleware in app.user_middleware])

    # Check if CORS middleware is present in the middleware stack
    cors_middleware_present = any(middleware.cls == CORSMiddleware for middleware in app.user_middleware)
    assert cors_middleware_present, "CORS middleware should be present"

def test_fastapi_builder_custom_middleware(app_settings):
    """Test that custom middleware is added to the app."""
    custom_middleware_class = CORSMiddleware
    app_settings.middleware = [{"middleware_class": custom_middleware_class, "options": {"allow_origins": ["*"]}}]
    
    builder = FastAPIBuilder(settings=app_settings)
    app = builder.build()

    # Verify that custom middleware is added by checking the class
    custom_middleware_present = any(middleware.cls == custom_middleware_class for middleware in app.user_middleware)
    assert custom_middleware_present, "Custom middleware should be present"

def test_fastapi_builder_with_optional_settings(app_settings, monkeypatch):
    """Test that optional settings are correctly applied in the FastAPI app."""
    monkeypatch.setattr(app_settings, "terms_of_service", "https://example.com/terms/")
    monkeypatch.setattr(app_settings, "contact", {"name": "Support", "email": "support@example.com"})
    monkeypatch.setattr(app_settings, "license_info", {"name": "MIT", "url": "https://opensource.org/licenses/MIT"})

    builder = FastAPIBuilder(settings=app_settings)
    app = builder.build()
    app.openapi()  # Generate OpenAPI schema explicitly

    assert app.openapi_schema['info']['termsOfService'] == app_settings.terms_of_service
    assert app.openapi_schema['info']['contact'] == app_settings.contact
    assert app.openapi_schema['info']['license'] == app_settings.license_info

def test_fastapi_builder_no_middleware(app_settings):
    """Test that no middleware is added if middleware settings are empty."""
    app_settings.middleware = []
    
    builder = FastAPIBuilder(settings=app_settings)
    app = builder.build()
    
    assert len(app.user_middleware) == 0, "No middleware should be present if not specified in settings"
