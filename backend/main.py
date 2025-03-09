import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title="DevMarketer API",
    description="個人開発者向けSNSマーケティング自動化WebアプリのAPI",
    version="0.1.0",
    openapi_url="/api/openapi.json",
)

# CORS middleware setup
origins = [
    "http://localhost:3000",
    # Add production URLs as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to DevMarketer API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
