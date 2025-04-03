from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Optional

class SparePartCreate(BaseModel):
    name: str
    category: str
    model_id: int
    quantity: int
    price: float
    image_url: Optional[str] = None

    @field_validator("image_url", mode="before")
    @classmethod
    def validate_url(cls, v):
        return str(v) if v else None

class SparePartAdminResponse(BaseModel):
    id: int
    name: str
    category: str
    model_id: int
    quantity: int
    price: Decimal
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ Updated for Pydantic v2

class SparePartUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    model_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    image_url: Optional[str] = None  # ✅ Changed from HttpUrl to str for consistency

    def to_dict(self):
        return {k: v for k, v in self.model_dump() if v is not None}  # ✅ Use `model_dump()` instead of `dict()`
