from typing import List, Dict, Any, Optional, Union, Callable, Type, Sequence
from fastapi import Response, Depends
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, ConfigDict
from fastapi.routing import APIRoute


def default_generate_unique_id(route: APIRoute) -> str:
    return f"{route.name}_{route.path.replace('/', '_')}"


class AppSettings(BaseSettings):
    """
    Pydantic settings for configuring FastAPI application, loading from environment variables where available.
    """

    title: str = "My FastAPI Application"
    """Title of the API, displayed in documentation and OpenAPI schema."""

    version: str = "0.1.0"
    """Version of the application, not the OpenAPI or FastAPI version."""

    debug: bool = False
    """Indicates if debug tracebacks should be shown on server errors."""

    description: str = "This is a sample FastAPI application."
    """Markdown-supported description of the API, visible in documentation."""

    openapi_url: Optional[str] = "/openapi.json"
    """URL for serving the OpenAPI schema. Set to `None` to disable."""

    docs_url: Optional[str] = "/docs"
    """Path to the Swagger UI docs. Set to `None` to disable."""

    redoc_url: Optional[str] = "/redoc"
    """Path to the ReDoc docs. Set to `None` to disable."""

    host: str = "0.0.0.0"
    """Host IP address on which to run the application."""

    port: int = 8000
    """Port number to run the application."""

    allowed_hosts: List[str] = ["*"]
    """List of allowed hosts for CORS."""

    middleware: Optional[List[Dict[str, Any]]] = None
    """List of middleware configurations as dictionaries."""

    openapi_tags: Optional[List[Dict[str, Any]]] = None
    """Tags for organizing OpenAPI endpoints."""

    servers: Optional[List[Dict[str, Union[str, Any]]]] = None
    """List of server details for OpenAPI specification."""

    dependencies: Optional[List[Depends]] = None
    """Global dependencies applied to each path operation."""

    default_response_class: Type[Response] = JSONResponse
    """Default response class for the application."""

    root_path: str = ""
    """Prefix path for the application when behind a proxy."""

    root_path_in_servers: bool = True
    """Determines if root_path is included in OpenAPI servers."""

    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    """Custom responses to be added in OpenAPI schema."""

    callbacks: Optional[List[APIRoute]] = None
    """Global OpenAPI callbacks."""

    swagger_ui_parameters: Optional[Dict[str, Any]] = None
    """Configuration parameters for Swagger UI."""

    swagger_ui_init_oauth: Optional[Dict[str, Any]] = None
    """OAuth2 configuration for Swagger UI."""

    generate_unique_id_function: Callable[[APIRoute], str] = default_generate_unique_id
    """Custom function for generating unique IDs for routes in OpenAPI."""

    terms_of_service: Optional[str] = None
    """URL to the Terms of Service for the API."""

    contact: Optional[Dict[str, str]] = None
    """Contact information for the API."""

    license_info: Optional[Dict[str, str]] = None
    """License information for the API."""

    cors_origins: Optional[List[AnyHttpUrl]] = None
    """List of allowed origins for CORS."""

    swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect"
    """OAuth2 redirect URL for Swagger UI."""

    include_in_schema: bool = True
    """Determines if paths are included in the OpenAPI schema."""

    redirect_slashes: bool = True
    """Enables automatic redirection for trailing slash in paths."""

    deprecated: Optional[bool] = None
    """Marks all paths as deprecated in the OpenAPI schema."""

    webhooks: Optional[Dict[str, Any]] = None
    """Global OpenAPI webhooks."""

    # Extra fields for server behavior
    separate_input_output_schemas: bool = True
    """Generate separate schemas for request and response bodies in OpenAPI."""

    on_startup: Optional[Sequence[Callable[[], Any]]] = None
    """List of startup event handlers."""

    on_shutdown: Optional[Sequence[Callable[[], Any]]] = None
    """List of shutdown event handlers."""

    lifespan: Optional[Callable] = None
    """Context manager for application lifespan, replaces on_startup/on_shutdown."""

    model_config = ConfigDict(env_prefix="APP_", env_file=".env")
