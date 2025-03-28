from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.carmodels import router as carmodels_router
from app.database import async_engine
from app.models.base import Base
import asyncio
from app.models import base, company, models, spare

app = FastAPI()

# ✅ Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific frontend URLs for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# ✅ Include car models router
app.include_router(carmodels_router, prefix="/carmodels")

async def init_db():
    """Initialize the database asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    """Run database initialization on startup."""
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Car Spare API"}
