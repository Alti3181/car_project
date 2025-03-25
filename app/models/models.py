from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class CarModel(Base):
    __tablename__ = "car_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company_id = Column(Integer, ForeignKey("car_companies.id"))

    company = relationship("CarCompany", back_populates="models")
    spare_parts = relationship("SparePart", back_populates="model")
    image_url = Column(String, nullable=True)
