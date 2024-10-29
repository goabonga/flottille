from fastapi import FastAPI

from .builder import FastAPIBuilder
from .config import AppSettings

settings = AppSettings()
builder = FastAPIBuilder(settings)
app: FastAPI = builder.build()

@app.get("/")
async def root():
    return {"message": "Hello World"}
