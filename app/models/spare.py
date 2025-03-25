
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, LargeBinary
from sqlalchemy.orm import relationship
from app.models.base import Base

class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(Enum("interior", "exterior", "other", name="part_category"))
    model_id = Column(Integer, ForeignKey("car_models.id"))

    model = relationship("CarModel", back_populates="spare_parts")
    img = Column(LargeBinary)