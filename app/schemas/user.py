from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    phone_number: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class OTPVerify(BaseModel):
    otp: str

class UserResponse(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str