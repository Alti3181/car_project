from pydantic import BaseModel

class CarModelResponse(BaseModel):
    model_name: str  
    company_brand: str  
    brand_image_url: str | None  # ✅ New field
    model_image_url: str | None  # ✅ New field

    class Config:
        from_attributes = True
