import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ReUseMatch API",
    description="Autonomous multi-agent platform for circular economy and reuse routing.",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes (will import when router is defined)
from backend.routes.match import router as match_router
app.include_router(match_router, prefix="/api")

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
