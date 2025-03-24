from fastapi import FastAPI
from app.routes import cardata  # Importing routes
from app.database import engine, Base

# Initialize FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(cardata.router)

@app.get("/")
def root():
    return {"message": "Welcome to Car Spare API"}
