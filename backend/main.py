# main.py
# The entry point of the FastAPI backend.
# This file:
# 1. Creates the FastAPI app
# 2. Configures CORS (allows frontend to talk to backend)
# 3. Registers all routers (design, status)
# 4. Adds health check endpoints
# 5. Starts the server
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from config import settings
from routers import design, status
from session.store import session_store

# ── Create the FastAPI app ────────────────────────────────────
app = FastAPI(
    title="AI Interior Designer API",
    description=(
        "Backend API for the AI Interior Designer application. "
        "Handles design plan generation, refinement, and "
        "image generation coordination."
    ),
    version="1.0.0",
    # Disable docs in production for security
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)

# ── CORS Configuration ────────────────────────────────────────
# CORS = Cross-Origin Resource Sharing
# This tells the backend which URLs are allowed to send requests.
# Without this, the browser blocks frontend → backend communication.
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add production frontend URL if set
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    allowed_origins.append(frontend_url)

# Allow all Vercel preview URLs
vercel_url = os.getenv("VERCEL_URL", "")
if vercel_url:
    allowed_origins.append(f"https://{vercel_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ──────────────────────────────────────────
# Each router handles a group of related endpoints
app.include_router(design.router)
app.include_router(status.router)

# ── Health Check Endpoints ────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint — confirms the server is running."""
    return {
        "message": "AI Interior Designer API is running",
        "version": "1.0.0",
        "environment": settings.environment,
        "docs": "/docs" if settings.environment == "development" else "disabled"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check.
    Frontend and deployment tools use this to verify the backend is alive.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "environment": settings.environment,
            "active_sessions": session_store.count(),
            "llm_provider": settings.llm_provider,
        }
    )


@app.on_event("startup")
async def startup_event():
    """Runs once when the server starts."""
    print("=" * 50)
    print("  AI Interior Designer Backend Starting")
    print("=" * 50)
    print(f"  Environment : {settings.environment}")
    print(f"  LLM Provider: {settings.llm_provider}")
    print(f"  Database    : {settings.database_url[:30]}...")
    print(f"  Docs        : http://localhost:{settings.backend_port}/docs")
    print("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """Runs once when the server shuts down."""
    print("AI Interior Designer Backend shutting down...")


# ── Run the server ────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,    # Auto-restart when code changes
        log_level="info"
    )