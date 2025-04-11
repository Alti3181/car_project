#app/routes/carmodel.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import text
from sqlalchemy.orm import joinedload
from app.database import get_async_db
from app.schemas.carmodel import CarModelResponse
from app.models.models import CarModel
from Levenshtein import distance as levenshtein_distance

router = APIRouter(prefix="/carmodels", tags=["Carmodels"])

@router.get("/search/", response_model=list[CarModelResponse])
async def search_cars(query: str, db: AsyncSession = Depends(get_async_db)):
    """Async search for car models by exact match first, then fuzzy search."""
    query = query.strip().lower()

    # ✅ Step 1: Try to get an exact match
    result = await db.execute(
        select(CarModel)
        .options(joinedload(CarModel.company))
        .filter(CarModel.name.ilike(query))  # Case-insensitive exact match
    )
    exact_match = result.scalars().all()

    if exact_match:
        return [
            {
                "model_name": model.name,
                "company_brand": model.company.name,
                "brand_image_url": model.company.image_url,  # ✅ Added
                "model_image_url": model.image_url  # ✅ Added
            }
            for model in exact_match
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
            {
                "model_name": model.name,
                "company_brand": model.company.name,
                "brand_image_url": model.company.image_url,  # ✅ Added
                "model_image_url": model.image_url  # ✅ Added
            }
            for model in models
        ]

    # ✅ Step 3: Fallback to fuzzy search (only if no exact match found)
    result = await db.execute(select(CarModel).options(joinedload(CarModel.company)))
    all_models = result.scalars().all()
    
    best_match_models = [
        model for model in all_models 
        if query in model.name.lower() or levenshtein_distance(query, model.name.lower()) <= 2
    ]

    if best_match_models:
        return [
            {
                "model_name": model.name,
                "company_brand": model.company.name,
                "brand_image_url": model.company.image_url,  # ✅ Added
                "model_image_url": model.image_url  # ✅ Added
            }
            for model in best_match_models
        ]

    return []
