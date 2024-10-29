# Import FastAPI framework
from fastapi import FastAPI

# Import custom builder and configuration settings
from .builder import FastAPIBuilder
from .config import AppSettings

# Initialize application settings from AppSettings
settings = AppSettings()

# Instantiate FastAPIBuilder with provided settings
builder = FastAPIBuilder(settings)

# Build the FastAPI application using the builder's configuration
app: FastAPI = builder.build()

# Define a heartbeat route for checking service health
@app.get("/heartbeat", include_in_schema=False)  # Exclude from OpenAPI schema
def heartbeat() -> dict[str, str]:
    """
    Health check endpoint to verify service availability.

    Returns
    -------
    dict[str, str]
        A JSON response with the application status set to "up".
    """
    # Return JSON response indicating that the service is operational
    return {"status": "up"}
