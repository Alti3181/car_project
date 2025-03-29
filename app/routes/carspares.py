from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.database import get_async_db
from app.models.models import CarModel
from app.models.spare import SparePart
from app.schemas.spare import SparePartResponse

router = APIRouter(prefix="/spare-parts", tags=["SpareParts"])

@router.get("/", response_model=list[SparePartResponse])
async def search_spare_parts(model_name: str, db: AsyncSession = Depends(get_async_db)):
    """Async search for spare parts by car model name."""
    model_name = model_name.strip().lower()

    result = await db.execute(
        select(SparePart)
        .join(CarModel)
        .options(joinedload(SparePart.model).joinedload(CarModel.company))
        .filter(CarModel.name.ilike(f"%{model_name}%"))
    )
    
    parts = result.scalars().all()

    return [
        SparePartResponse(  # ✅ Ensure this matches the schema
            id=part.id,  
            name=part.name,
            category=part.category,  # ✅ Added missing category
            model_id=part.model_id,  # ✅ Added missing model_id
            quantity=part.quantity,
            price=part.price,
            img=part.image_url  
        )
        for part in parts
    ]
