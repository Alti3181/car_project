# app/models/error_log.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.models.base import Base

class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    error = Column(String(255), nullable=False)          # Short error type
    reason = Column(Text, nullable=False)                # Full stack trace
    pc_name = Column(String(100), nullable=True)         # System that triggered it
    timestamp = Column(DateTime, default=datetime.utcnow) # When it occurred
    path = Column(String(255), nullable=True)            # Which endpoint
    method = Column(String(10), nullable=True)           # GET/POST etc.
