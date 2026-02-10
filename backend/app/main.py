"""
Main FastAPI application.
"""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import lottery, subscriptions
from app.schemas.lottery import HealthCheckResponse


# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📊 Environment: {settings.environment}")
    print(f"🗄️  Database: Connected")
    
    # Check and update lottery data
    print("🔍 Checking lottery data...")
    from app.core.database import SessionLocal
    from app.services.data.lotofacil_fetcher import get_fetcher
    
    db = SessionLocal()
    try:
        fetcher = get_fetcher()
        result = await fetcher.update_database(db)
        if result.get("success"):
            print(f"✅ {result.get('message')} (Latest: {result.get('latest_contest')})")
        else:
            print(f"⚠️  Data update warning: {result.get('error')}")
    except Exception as e:
        print(f"⚠️  Could not update lottery data: {e}")
    finally:
        db.close()
    
    # Start scheduler if enabled
    if settings.scheduler_enabled:
        from app.services.scheduler import start_scheduler
        start_scheduler()
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")
    if settings.scheduler_enabled:
        from app.services.scheduler import shutdown_scheduler
        shutdown_scheduler()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for lottery number analysis and suggestions",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(lottery.router, prefix="/api/v1")
app.include_router(subscriptions.router, prefix="/api/v1")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "Documentation disabled in production",
    }


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        Health status
    """
    try:
        # Test database connection
        from sqlalchemy import text
        from app.core.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return HealthCheckResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        version=settings.app_version,
        database=db_status,
        timestamp=datetime.utcnow()
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.debug else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
