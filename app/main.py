from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import admincompany, adminmodel, adminspare, carmodels, carspares, auth
from .database import async_engine
from .database import engine
from .models import models
from .models.user import User
from .models.base import Base
import logging

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Synchronous table creation for backward compatibility
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin routes
app.include_router(admincompany.company_router, prefix="/api/v1/admin/company", tags=["Admin Company"])
app.include_router(adminmodel.model_router, prefix="/api/v1/admin/model", tags=["Admin Model"])
app.include_router(adminspare.spare_router, prefix="/api/v1/admin/spare", tags=["Admin Spare"])

# Car routes
app.include_router(carmodels.router, prefix="/api/v1/car/model", tags=["Carmodels"])
app.include_router(carspares.router, prefix="/api/v1/car/spare", tags=["SpareParts"])

# Auth routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

async def init_db():
    """Initialize the database asynchronously."""
    try:
        async with async_engine.begin() as conn:
            logger.info("Initializing database...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

@app.on_event("startup")
async def startup():
    """Run database initialization on startup."""
    logger.info("🚀 Starting FastAPI application...")
    await init_db()

@app.get("/")
async def root():
    """Root endpoint to check API status."""
    return {"message": "Welcome to Car Spare API 🚗💨"}
