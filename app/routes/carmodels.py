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
    """Async search for car models by company name or model name, with fuzzy & prefix search."""
    query = query.strip().lower()

    # ✅ Use PostgreSQL trigram similarity search for company names
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
            .options(joinedload(CarModel.company))  # ✅ Eagerly load `company`
            .filter(CarModel.company_id == company_id)
        )
        models = result.scalars().all()
        return [
            {"name": model.name, "company_name": model.company.name, "image_url": model.image_url}
            for model in models
        ]

    # ✅ Fallback: Fuzzy search for car models using Levenshtein distance
    result = await db.execute(select(CarModel).options(joinedload(CarModel.company)))  # ✅ Load `company`
    all_models = result.scalars().all()
    
    best_match_models = [
        model for model in all_models 
        if query in model.name.lower() or levenshtein_distance(query, model.name.lower()) <= 2
    ]

    if best_match_models:
        return [
            {"name": model.name, "company_name": model.company.name, "image_url": model.image_url}
            for model in best_match_models
        ]

    return []
