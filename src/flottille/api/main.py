from fastapi import FastAPI

from .builder import FastAPIBuilder
from .config import AppSettings

settings = AppSettings()
builder = FastAPIBuilder(settings)
app: FastAPI = builder.build()


# Define a heartbeat route to check service health
@app.get("/heartbeat", include_in_schema=False)
def heartbeat() -> dict[str, str]:
    """
    Health check endpoint. Returns the status of the application.

    Returns:
    -------
    dict[str, str]
        A JSON response indicating the service status as "up".
    """
    return {"status": "up"}
