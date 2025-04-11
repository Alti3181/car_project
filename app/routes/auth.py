from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
import jwt
import random
import string
from fastapi.security import HTTPBearer
from ..database import get_async_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse, OTPVerify, Token
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

# Constants
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
EMAIL_SENDER = "headway366@gmail.com"
EMAIL_PASSWORD = "vdgl hjrk yrvw xkkf"

bearer_scheme = HTTPBearer()

# def send_otp_email(email: str, otp: str):
    
#     message = MIMEMultipart()
#     message["From"] = EMAIL_SENDER
#     message["To"] = email
#     message["Subject"] = "Your OTP for Authentication"
    
#     body = f"Your OTP is: {otp}. It will expire in 10 minutes."
#     message.attach(MIMEText(body, "plain"))
    
#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         server.send_message(message)
def send_otp_email(email: str, otp: str):
    try:
        print(f"Sending OTP to: {email}, OTP: {otp}")  # For debugging

        message = MIMEMultipart()
        message["From"] = EMAIL_SENDER
        message["To"] = email
        message["Subject"] = "Your OTP for Authentication"
        
        body = f"Your OTP is: {otp}. It will expire in 10 minutes."
        message.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(message)

        print("Email sent successfully!")

    except Exception as e:
        print("Failed to send OTP email:", e)

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token = Depends(bearer_scheme), db: AsyncSession = Depends(get_async_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        # Convert string user_id to integer
        try:
            user_id = int(user_id)
        except ValueError:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user

# @router.post("/register", response_model=dict)
# async def register_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    # Create new user (allows duplicates)
    # new_user = User(
    #     username=user.username,
    #     phone_number=user.phone_number,
    #     email=user.email
    # )
    
    # # Generate and save OTP
    # otp = generate_otp()
    # new_user.otp = otp
    # new_user.otp_created_at = datetime.utcnow()
    
    # db.add(new_user)
    # await db.commit()
    # await db.refresh(new_user)
    # # Log before sending email
    # print(f"User {new_user.email} registered with OTP: {otp}")
    # # Send OTP via email
    # send_otp_email(user.email, otp)
    
    # return {"message": "OTP sent to your email"}

@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    new_user = User(
        username=user.username,
        phone_number=user.phone_number,
        email=user.email
    )
    
    otp = generate_otp()
    new_user.otp = otp
    new_user.otp_created_at = datetime.utcnow()
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    send_otp_email(user.email, otp)
    
    return {"success": True, "message": "OTP sent to your email"}


@router.post("/verify-otp", response_model=Token)
async def verify_otp(otp_data: OTPVerify, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        select(User).where(User.otp == otp_data.otp)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Check OTP expiration (10 minutes)
    if datetime.utcnow() - user.otp_created_at > timedelta(minutes=10):
        raise HTTPException(status_code=400, detail="OTP expired")
    
    # Mark user as verified and clear OTP
    user.is_verified = True
    user.otp = None
    user.otp_created_at = None
    await db.commit()
    await db.refresh(user)
    
    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user