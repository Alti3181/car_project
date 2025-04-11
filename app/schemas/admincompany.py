from pydantic import BaseModel
from typing import Optional

class CarCompanyCreate(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2

class CarCompanyUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2

class CarCompanyResponse(BaseModel):
    id: int
    brand_name: str
    brand_image_url: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2
