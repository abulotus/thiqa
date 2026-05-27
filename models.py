from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)

    full_name_ar = Column(String, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    national_id = Column(String, unique=True, nullable=False)

    address = Column(String)
    city = Column(String)

    total_credit = Column(Float, default=0)
    balance_remaining = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)