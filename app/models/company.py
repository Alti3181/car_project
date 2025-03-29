from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.base import Base
from app.models.models import CarModel  # ✅ Import CarModel to avoid errors

class CarCompany(Base):
    __tablename__ = "car_companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    image_url = Column(String, nullable=True)

    models = relationship("CarModel", back_populates="company", cascade="all, delete-orphan")

    @staticmethod
    async def get_company_with_models(company_name: str, db: AsyncSession):
        """Fetch a car company along with its associated models using case-insensitive search."""
        result = await db.execute(
            select(CarCompany)
            .options(joinedload(CarCompany.models))
            .filter(CarCompany.name.ilike(f"%{company_name}%"))
        )
        return result.scalars().first()
