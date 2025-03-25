from pydantic import BaseModel

class CarModelResponse(BaseModel):
    id: int
    name: str
    company_name: str
    image_url: str | None

    class Config:
        from_attributes = True

