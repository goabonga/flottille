from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import AppSettings


class FastAPIBuilder:
    """
    A builder class to configure and create an instance of FastAPI with custom settings.

    Parameters
    ----------
    settings : AppSettings
        An instance of AppSettings that holds configuration details for the FastAPI app.

    Methods
    -------
    build() -> FastAPI:
        Configures and returns a FastAPI application instance based on the provided settings.
    """

    def __init__(self, settings: AppSettings):
        """
        Initializes the FastAPIBuilder with the provided settings.

        Parameters
        ----------
        settings : AppSettings
            An instance containing configuration settings for the FastAPI application.
        """
        self.settings = settings

    def build(self) -> FastAPI:
        """
        Builds and configures the FastAPI application based on the settings provided.

        Returns
        -------
        FastAPI
            A configured FastAPI instance ready for use with the specified settings.
        """
        # Initialize the FastAPI app with settings attributes
        app = FastAPI(
            title=self.settings.title,
            version=self.settings.version,
            debug=self.settings.debug,
            description=self.settings.description,
            openapi_url=self.settings.openapi_url,
            docs_url=self.settings.docs_url,
            redoc_url=self.settings.redoc_url,
            openapi_tags=self.settings.openapi_tags,
            servers=self.settings.servers,
            dependencies=self.settings.dependencies,
            default_response_class=self.settings.default_response_class,
            root_path=self.settings.root_path,
            root_path_in_servers=self.settings.root_path_in_servers,
            responses=self.settings.responses,
            callbacks=self.settings.callbacks,
            swagger_ui_parameters=self.settings.swagger_ui_parameters,
            swagger_ui_init_oauth=self.settings.swagger_ui_init_oauth,
            generate_unique_id_function=self.settings.generate_unique_id_function,
            terms_of_service=self.settings.terms_of_service,
            contact=self.settings.contact,
            license_info=self.settings.license_info,
            swagger_ui_oauth2_redirect_url=self.settings.swagger_ui_oauth2_redirect_url,
            include_in_schema=self.settings.include_in_schema,
            redirect_slashes=self.settings.redirect_slashes,
            deprecated=self.settings.deprecated,
            webhooks=self.settings.webhooks,
        )

        # Add custom middleware from settings if defined
        if self.settings.middleware:
            for mw in self.settings.middleware:
                # Each middleware requires its class and additional options passed as kwargs
                app.add_middleware(mw['middleware_class'], **mw['options'])

        # Add CORS middleware if origins are specified in settings
        if self.settings.cors_origins:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.settings.cors_origins],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # Return the fully configured FastAPI instance
        return app
