# app/routes/adminmodel.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import text
from app.database import get_async_db
from app.models.models import CarModel
from sqlalchemy.orm import joinedload
from app.schemas.adminmodel import (
    CarModelCreate,
    CarModelResponseAdmin,
    CarModelSearchResponse,
    CarModelUpdate
)
from Levenshtein import distance as levenshtein_distance

router = APIRouter()

# Admin Car Model Routes
model_router = APIRouter(prefix="/admin/model", tags=["Admin Model"])

@model_router.post("/", response_model=CarModelResponseAdmin)
async def create_model(model: CarModelCreate, db: AsyncSession = Depends(get_async_db)):
    """Create a new car model"""
    new_model = CarModel(
        name=model.name, 
        company_id=model.company_id, 
        image_url=str(model.image_url) if model.image_url else None  # Convert HttpUrl to str
    )
    db.add(new_model)
    await db.commit()
    await db.refresh(new_model)
    return new_model


@model_router.get("/search", response_model=list[CarModelSearchResponse])
async def search_cars(query: str, db: AsyncSession = Depends(get_async_db)):
    """Search for car models by exact match, company similarity, or fuzzy match."""
    query = query.strip().lower()

    # ✅ Step 1: Exact match search
    result = await db.execute(
        select(CarModel)
        .options(joinedload(CarModel.company))
        .filter(CarModel.name.ilike(query))  # Case-insensitive exact match
    )
    exact_match = result.scalars().all()

    if exact_match:
        return [
            CarModelSearchResponse(
                model_name=model.name,
                company_brand=model.company.name,
                brand_image_url=model.company.image_url,
                model_image_url=model.image_url
            ) for model in exact_match
        ]

    # ✅ Step 2: Try company similarity search
    sql = text("""
        SELECT id, name FROM car_companies 
        WHERE name % :query
        ORDER BY similarity(name, :query) DESC
        LIMIT 5;
    """)
    result = await db.execute(sql, {"query": query})
    best_match_company = result.fetchall()

    if best_match_company:
        company_id = best_match_company[0][0]
        result = await db.execute(
            select(CarModel)
            .options(joinedload(CarModel.company))
            .filter(CarModel.company_id == company_id)
        )
        models = result.scalars().all()
        return [
            CarModelSearchResponse(
                model_name=model.name,
                company_brand=model.company.name,
                brand_image_url=model.company.image_url,
                model_image_url=model.image_url
            ) for model in models
        ]

    # ✅ Step 3: Fallback to fuzzy search (if no exact match found)
    result = await db.execute(select(CarModel).options(joinedload(CarModel.company)))
    all_models = result.scalars().all()
    
    best_match_models = [
        model for model in all_models 
        if query in model.name.lower() or levenshtein_distance(query, model.name.lower()) <= 2
    ]

    if best_match_models:
        return [
            CarModelSearchResponse(
                model_name=model.name,
                company_brand=model.company.name,
                brand_image_url=model.company.image_url,
                model_image_url=model.image_url
            ) for model in best_match_models
        ]

    return []

@model_router.put("/{model_id}", response_model=CarModelResponseAdmin)
async def update_model(model_id: int, model: CarModelUpdate, db: AsyncSession = Depends(get_async_db)):
    """Update an existing car model"""
    result = await db.execute(select(CarModel).filter(CarModel.id == model_id))
    existing_model = result.scalars().first()
    if not existing_model:
        raise HTTPException(status_code=404, detail="Model not found")

    # Apply only provided updates
    if model.name is not None:
        existing_model.name = model.name
    if model.image_url is not None:
        existing_model.image_url = model.image_url

    await db.commit()
    await db.refresh(existing_model)
    return existing_model

@model_router.delete("/{model_id}")
async def delete_model(model_id: int, db: AsyncSession = Depends(get_async_db)):
    """Delete a car model"""
    result = await db.execute(select(CarModel).filter(CarModel.id == model_id))
    model = result.scalars().first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    await db.delete(model)
    await db.commit()
    return {"message": "Model deleted successfully"}
