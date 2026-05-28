from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from app.databas import Base

# ---------------------------------------------------
# MERCHANTS
# ---------------------------------------------------

class Merchant(Base):

    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True)

    business_name = Column(String)

    owner_name = Column(String)

    mobile_number = Column(String)

    city = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# ---------------------------------------------------
# USERS / CUSTOMERS
# ---------------------------------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    merchant_id = Column(
        Integer,
        ForeignKey("merchants.id")
    )

    full_name = Column(String)

    mobile_number = Column(
        String,
        unique=True
    )

    national_id = Column(
        String,
        unique=True
    )

    city = Column(String)

    total_credit = Column(Float)

    balance_remaining = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    payments = relationship(
        "Payment",
        back_populates="user"
    )

# ---------------------------------------------------
# PAYMENTS
# ---------------------------------------------------

class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    amount_paid = Column(Float)

    payment_method = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="payments"
    )
