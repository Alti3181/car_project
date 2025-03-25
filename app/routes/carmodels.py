
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.schemas.carmodel import CarModelResponse
from app.models.company import CarCompany
from app.models.models import CarModel
from sqlalchemy.sql import text

router = APIRouter(prefix="/carmodels", tags=["Carmodels"])

@router.get("/search/", response_model=list[CarModelResponse])
async def search_cars(query: str, db: AsyncSession = Depends(get_async_db)):
    """Async search for car models by company name or model name, with fuzzy & prefix search."""
    query = query.strip().lower()

    # Use PostgreSQL trigram similarity search for companies
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
        result = await db.execute(select(CarModel).filter(CarModel.company_id == company_id))
        models = result.scalars().all()
        return [{"name": model.name, "company_name": best_match_company[0][1], "image_url": model.image_url} for model in models]

    # Fallback: Fuzzy search for models
    result = await db.execute(select(CarModel))
    all_models = result.scalars().all()
    best_match_models = [model for model in all_models if query in model.name.lower() or levenshtein_distance(query, model.name.lower()) <= 2]

    if best_match_models:
        return [{"name": model.name, "company_name": model.company.name, "image_url": model.image_url} for model in best_match_models]

    return []