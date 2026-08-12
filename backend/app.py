import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from contextlib import asynccontextmanager
from database.connection import engine, Base
import backend.models  # Ensures Device and Recipient models are registered with Base.metadata

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables safely on application startup
    Base.metadata.create_all(bind=engine)
    yield

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ReUseMatch API",
    description="Autonomous multi-agent platform for circular economy and reuse routing.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
from backend.routes.match import router as match_router
from backend.routes.devices import router as devices_router
from backend.routes.recipients import router as recipients_router

app.include_router(match_router, prefix="/api")
app.include_router(devices_router, prefix="/api")
app.include_router(recipients_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the ReUseMatch API",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": os.getenv("ENV", "development")}
