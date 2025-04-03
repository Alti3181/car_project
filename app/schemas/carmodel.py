# app/schemas/carmodel.py
from pydantic import BaseModel
from typing import Optional

class CarModelCreate(BaseModel):
    model_name : str
    mmode_image_url: Optional[str] = None

    class Config:
        orm_mode = True  # Ensure compatibility with SQLAlchemy models

class CarModelResponse(BaseModel):
    model_name : str
    company_brand : str
    brand_image_url: Optional[str] = None
    model_image_url : Optional[str] = None
    class Config:
        orm_mode = True
