from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import AppSettings


class FastAPIBuilder:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    def build(self) -> FastAPI:
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

        if self.settings.middleware:
            for mw in self.settings.middleware:
                app.add_middleware(mw['middleware_class'], **mw['options'])

        if self.settings.cors_origins:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.settings.cors_origins],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        return app
