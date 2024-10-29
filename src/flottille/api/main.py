from fastapi import FastAPI
from .config import AppSettings
from .builder import FastAPIBuilder

settings = AppSettings()
builder = FastAPIBuilder(settings)
app: FastAPI = builder.build()

@app.get("/")
async def root():
    return {"message": "Hello World"}
