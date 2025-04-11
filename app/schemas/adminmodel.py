from pydantic import BaseModel, HttpUrl
from typing import Optional

class CarModelCreate(BaseModel):
    name: str
    company_id: int
    image_url: Optional[str] = None  # Change from HttpUrl to str

class CarModelUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None  # Change from HttpUrl to str

class CarModelResponseAdmin(CarModelCreate):
    id: int

class CarModelSearchResponse(BaseModel):
    model_name: str
    company_brand: str
    brand_image_url: Optional[str] = None  # Change from HttpUrl to str
    model_image_url: Optional[str] = None  # Change from HttpUrl to str
