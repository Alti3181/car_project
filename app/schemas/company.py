#app/schema/company.py
from pydantic import BaseModel

class CarCompanyResponse(BaseModel):
    company_brand: str  # Changed from `name`
    image_url: str | None

    class Config:
        from_attributes = True