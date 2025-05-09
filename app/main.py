from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.carmodels import router as carmodels_router
from app.routes.carspares import router as spare_parts_router
from app.database import async_engine
from app.models import Base
import logging

# ✅ Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers WITHOUT prefix to avoid duplication
app.include_router(carmodels_router)  
app.include_router(spare_parts_router)

async def init_db():
    """Initialize the database asynchronously."""
    async with async_engine.begin() as conn:
        logger.info("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully!")

@app.on_event("startup")
async def startup():
    """Run database initialization on startup."""
    logger.info("🚀 Starting FastAPI application...")
    await init_db()

@app.get("/")
async def root():
    """Root endpoint to check API status."""
    return {"message": "Welcome to Car Spare API 🚗💨"}
