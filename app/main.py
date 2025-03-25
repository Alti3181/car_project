from fastapi import FastAPI
from app.routes.carmodels import router as company_router
from app.database import async_engine
from app.models.base import Base
import asyncio
from app.models import (
    base,company,models,spare)

app = FastAPI()
app.include_router(company_router, prefix="/carmodels")


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
