from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_db
from app.models.spare import SparePart
from app.schemas.adminspare import SparePartCreate, SparePartUpdate ,SparePartAdminResponse
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator

router = APIRouter()
spare_router = APIRouter(prefix="/admin/spare", tags=["Admin Spare"])

@spare_router.post("/", response_model=SparePartAdminResponse)
async def create_spare(spare: SparePartCreate, db: AsyncSession = Depends(get_async_db)):
    new_spare = SparePart(
        name=spare.name,
        category=spare.category,
        model_id=spare.model_id,
        quantity=spare.quantity,
        price=Decimal(spare.price),
        image_url=str(spare.image_url) if spare.image_url else None
    )
    db.add(new_spare)
    await db.commit()
    await db.refresh(new_spare)
    return new_spare

@spare_router.get("/{spare_id}", response_model=SparePartAdminResponse)
async def get_spare(spare_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SparePart).filter(SparePart.id == spare_id))
    spare = result.scalars().first()
    if not spare:
        raise HTTPException(status_code=404, detail="Spare part not found")
    return spare

@spare_router.put("/{spare_id}", response_model=SparePartAdminResponse)
async def update_spare(spare_id: int, spare_update: SparePartUpdate, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SparePart).filter(SparePart.id == spare_id))
    spare = result.scalars().first()
    if not spare:
        raise HTTPException(status_code=404, detail="Spare part not found")
    
    update_data = spare_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(spare, key, value if value is not None else getattr(spare, key))
    
    await db.commit()
    await db.refresh(spare)
    return spare

@spare_router.delete("/{spare_id}")
async def delete_spare(spare_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(SparePart).filter(SparePart.id == spare_id))
    spare = result.scalars().first()
    if not spare:
        raise HTTPException(status_code=404, detail="Spare part not found")
    await db.delete(spare)
    await db.commit()
    return {"message": "Spare part deleted successfully"}