#app/models/models.py
from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.spare import SparePart  # ✅ Import SparePart to avoid errors

class CarModel(Base):
    __tablename__ = "car_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("car_companies.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String, nullable=True)

    company = relationship("CarCompany", back_populates="models", foreign_keys=[company_id])
    spare_parts = relationship("SparePart", back_populates="model", cascade="all, delete-orphan")
