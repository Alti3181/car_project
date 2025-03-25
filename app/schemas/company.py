from pydantic import BaseModel

class CarCompanyResponse(BaseModel):
    id: int
    name: str
    image_url: str | None

    class Config:
        from_attributes = True
