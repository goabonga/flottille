from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.routing import BaseRoute


def default_generate_unique_id(route: APIRoute) -> str:
    """
    Generates a unique identifier for a given API route.

    Parameters
    ----------
    route : APIRoute
        The route for which a unique ID is generated.

    Returns
    -------
    str
        A unique identifier string based on route name and path.
    """
    return f"{route.name}_{route.path.replace('/', '_')}"


class AppSettings(BaseSettings):
    """
    Pydantic settings for configuring a FastAPI application, with support for environment variable overrides.

    Attributes
    ----------
    title : str
        Title of the API, displayed in documentation and OpenAPI schema.
    version : str
        Version of the application, not the OpenAPI or FastAPI version.
    debug : bool
        Indicates if debug tracebacks should be shown on server errors.
    description : str
        Markdown-supported description of the API, visible in documentation.
    openapi_url : Optional[str]
        URL for serving the OpenAPI schema. Set to `None` to disable.
    docs_url : Optional[str]
        Path to the Swagger UI docs. Set to `None` to disable.
    redoc_url : Optional[str]
        Path to the ReDoc docs. Set to `None` to disable.
    allowed_hosts : List[str]
        List of allowed hosts for CORS.
    middleware : Optional[List[Dict[str, Any]]]
        List of middleware configurations as dictionaries.
    openapi_tags : Optional[List[Dict[str, Any]]]
        Tags for organizing OpenAPI endpoints.
    servers : Optional[List[Dict[str, Union[str, Any]]]]
        List of server details for OpenAPI specification.
    dependencies : Optional[Sequence[Depends]]
        Global dependencies applied to each path operation.
    default_response_class : Type[Response]
        Default response class for the application.
    root_path : str
        Prefix path for the application when behind a proxy.
    root_path_in_servers : bool
        Determines if root_path is included in OpenAPI servers.
    responses : Optional[Dict[Union[int, str], Dict[str, Any]]]
        Custom responses to be added in OpenAPI schema.
    callbacks : Optional[List[BaseRoute]]
        Global OpenAPI callbacks.
    swagger_ui_parameters : Optional[Dict[str, Any]]
        Configuration parameters for Swagger UI.
    swagger_ui_init_oauth : Optional[Dict[str, Any]]
        OAuth2 configuration for Swagger UI.
    generate_unique_id_function : Callable[[APIRoute], str]
        Custom function for generating unique IDs for routes in OpenAPI.
    terms_of_service : Optional[str]
        URL to the Terms of Service for the API.
    contact : Optional[Dict[str, str]]
        Contact information for the API.
    license_info : Optional[Dict[str, str]]
        License information for the API.
    cors_origins : Optional[List[AnyHttpUrl]]
        List of allowed origins for CORS.
    swagger_ui_oauth2_redirect_url : Optional[str]
        OAuth2 redirect URL for Swagger UI.
    include_in_schema : bool
        Determines if paths are included in the OpenAPI schema.
    redirect_slashes : bool
        Enables automatic redirection for trailing slashes in paths.
    deprecated : Optional[bool]
        Marks all paths as deprecated in the OpenAPI schema.
    webhooks : Optional[APIRouter]
        Global OpenAPI webhooks.
    separate_input_output_schemas : bool
        Generate separate schemas for request and response bodies in OpenAPI.
    on_startup : Optional[Sequence[Callable[[], Any]]]
        List of startup event handlers.
    on_shutdown : Optional[Sequence[Callable[[], Any]]]
        List of shutdown event handlers.
    lifespan : Optional[Callable]
        Context manager for application lifespan, replaces on_startup/on_shutdown.
    
    Configurations
    --------------
    model_config : SettingsConfigDict
        Configuration dict for setting environment variable prefix and env file location.
    """

    title: str = "My FastAPI Application"
    version: str = "0.1.0"
    debug: bool = False
    description: str = "This is a sample FastAPI application."
    openapi_url: Optional[str] = "/openapi.json"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_hosts: List[str] = ["*"]
    middleware: Optional[List[Dict[str, Any]]] = None
    openapi_tags: Optional[List[Dict[str, Any]]] = None
    servers: Optional[List[Dict[str, Union[str, Any]]]] = None
    dependencies: Optional[Sequence[Depends]] = None  # type: ignore[valid-type]
    default_response_class: Type[Response] = JSONResponse
    root_path: str = ""
    root_path_in_servers: bool = True
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    callbacks: Optional[List[BaseRoute]] = None
    swagger_ui_parameters: Optional[Dict[str, Any]] = None
    swagger_ui_init_oauth: Optional[Dict[str, Any]] = None
    generate_unique_id_function: Callable[[APIRoute], str] = default_generate_unique_id
    terms_of_service: Optional[str] = None
    contact: Optional[Dict[str, str]] = None
    license_info: Optional[Dict[str, str]] = None
    cors_origins: Optional[List[AnyHttpUrl]] = None
    swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect"
    include_in_schema: bool = True
    redirect_slashes: bool = True
    deprecated: Optional[bool] = None
    webhooks: Optional[APIRouter] = None
    separate_input_output_schemas: bool = True
    on_startup: Optional[Sequence[Callable[[], Any]]] = None
    on_shutdown: Optional[Sequence[Callable[[], Any]]] = None
    lifespan: Optional[Callable] = None

    # Configuration for loading environment variables with a specific prefix and env file
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")
