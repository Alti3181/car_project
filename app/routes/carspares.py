# app/routes/carspare.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.database import get_async_db
from app.models.models import CarModel
from app.models.spare import SparePart
from app.schemas.spare import SparePartResponse
from app.utils.errorlog import log_error_to_db  # ✅ Import log_error_to_db

router = APIRouter(prefix="/spare-parts", tags=["SpareParts"])

@router.get("/", response_model=list[SparePartResponse])
async def search_spare_parts(request: Request, model_name: str, db: AsyncSession = Depends(get_async_db)):
    """Async search for spare parts by car model name."""
    try:
        model_name = model_name.strip().lower()

        result = await db.execute(
            select(SparePart)
            .join(CarModel)
            .options(joinedload(SparePart.model).joinedload(CarModel.company))
            .filter(CarModel.name.ilike(f"%{model_name}%"))
        )
        
        parts = result.scalars().all()

        return [
            SparePartResponse(
                id=part.id,
                name=part.name,
                category=part.category,
                model_id=part.model_id,
                quantity=part.quantity,
                price=part.price,
                img=part.image_url
            )
            for part in parts
        ]
    except Exception as e:
        await log_error_to_db(request, e, db)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{spare_id}", response_model=SparePartResponse)
async def get_spare(request: Request, spare_id: int, db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(select(SparePart).filter(SparePart.id == spare_id))
        spare = result.scalar_one_or_none()

        if not spare:
            raise HTTPException(status_code=404, detail="Spare part not found")

        return SparePartResponse(
            id=spare.id,
            name=spare.name,
            category=spare.category,
            model_id=spare.model_id,
            quantity=spare.quantity,
            price=spare.price,
            img=spare.image_url
        )
    except Exception as e:
        await log_error_to_db(request, e, db)
        raise HTTPException(status_code=500, detail="Internal server error")
