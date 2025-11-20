from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="Incident Management API")

app.include_router(endpoints.router, tags=["incidents"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

