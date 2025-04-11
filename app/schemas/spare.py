#app/schemas/spare.py
from decimal import Decimal  # ✅ Correct import
from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional

class SparePartBase(BaseModel):
    name: str
    category: str  # "interior", "exterior", "other"
    model_id: int
    quantity: int  # Ensure quantity is non-negative
    price: Decimal  # ✅ Use Python's decimal.Decimal
    img: Optional[HttpUrl] = None  # URL for image storage
 
    class Config:
        model_config = ConfigDict(from_attributes=True)  # ✅ Fix for Pydantic v2

class SparePartCreate(SparePartBase):
    pass  # Inherits all fields from SparePartBase

class SparePartUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[Decimal] = None
    img: Optional[HttpUrl] = None

    class Config:
            model_config = ConfigDict(from_attributes=True)  # ✅ Fix for Pydantic v2

class SparePartResponse(SparePartBase):
    id: int  # Include ID for response

    class Config:
        model_config = ConfigDict(from_attributes=True)  # ✅ Fix for Pydantic v2
