from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_db
from app.models.company import CarCompany
from app.schemas.admincompany import CarCompanyCreate, CarCompanyResponse  ,CarCompanyUpdate# Correct import path
from app.schemas.carmodel import CarModelCreate, CarModelResponse
from app.schemas.spare import SparePartCreate, SparePartResponse
from typing import List  # Import List from typing module

router = APIRouter()

# Admin Company Routes
company_router = APIRouter(prefix="/admin/company", tags=["Admin Company"])

@company_router.post("/", response_model=CarCompanyResponse)
async def create_company(company: CarCompanyCreate, db: AsyncSession = Depends(get_async_db)):
    new_company = CarCompany(id=company.id, name=company.name, image_url=company.image_url)  # Fixed attributes
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return CarCompanyResponse(
        id = new_company.id,
        brand_name = new_company.name,
        brand_image_url= new_company.image_url
    )

@company_router.get("/search", response_model=List[CarCompanyResponse])
async def search_companies(query: str, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        select(CarCompany).filter(CarCompany.name.ilike(f"%{query}%"))
    )
    companies = result.scalars().all()

    if not companies:
        raise HTTPException(status_code=404, detail="No companies found matching the search query")

    # Transform response to match new field names
    transformed_companies = [
        CarCompanyResponse(
            id=company.id,
            brand_name=company.name,  # Renaming field
            brand_image_url=company.image_url  # Renaming field
        )
        for company in companies
    ]

    return transformed_companies

@company_router.get("/{company_id}", response_model=CarCompanyResponse)
async def get_company(company_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(CarCompany).filter(CarCompany.id == company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Manually transform the response to match the new schema
    return {
        "id": company.id,
        "brand_name": company.name,  # Mapping name → brand_name
        "brand_image_url": company.image_url,  # Mapping image_url → brand_image_url
    }

@company_router.put("/{company_id}", response_model=CarCompanyResponse)
async def update_company(company_id: int, company_data: CarCompanyUpdate, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(CarCompany).filter(CarCompany.id == company_id))
    company = result.scalars().first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Update only provided fields
    if company_data.name is not None:
        company.name = company_data.name
    if company_data.image_url is not None:
        company.image_url = company_data.image_url

    await db.commit()
    await db.refresh(company)

    return {
        "id": company.id,
        "brand_name": company.name,
        "brand_image_url": company.image_url
    }


@company_router.delete("/{company_id}")
async def delete_company(company_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(CarCompany).filter(CarCompany.id == company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    await db.delete(company)
    await db.commit()
    return {"message": "Company deleted successfully"}