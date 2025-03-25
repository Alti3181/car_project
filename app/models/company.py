from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import text
from Levenshtein import distance as levenshtein_distance

async def get_company_with_models(company_name: str, db: AsyncSession):
    result = await db.execute(
        select(CarCompany)
        .options(joinedload(CarCompany.models))
        .filter(CarCompany.name.ilike(f"%{company_name}%"))
    )
    return result.scalars().first()

class CarCompany(Base):
    __tablename__ = "car_companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    models = relationship("CarModel", back_populates="company")
    image_url = Column(String, nullable=True)
