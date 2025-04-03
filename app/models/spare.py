#app/models/spare.py
from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from app.models.base import Base

class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(Enum("interior", "exterior", "other", name="part_category"), nullable=False)
    model_id = Column(Integer, ForeignKey("car_models.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(DECIMAL(10, 2), nullable=False)  # ✅ Correct: Keep using SQLAlchemy's DECIMAL
    image_url = Column(String, nullable=True)

    model = relationship("CarModel", back_populates="spare_parts")
