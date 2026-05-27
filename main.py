from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from db import SessionLocal, engine, Base
from models import User
from schemas import UserCreate

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# ADD USER (CUSTOMER)
# ---------------------------

@app.post("/users")
def add_user(user: UserCreate, db: Session = Depends(get_db)):

    # check mobile exists
    existing = db.query(User).filter(
        User.mobile_number == user.mobile_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        id=str(uuid.uuid4()),
        full_name_ar=user.full_name_ar,
        full_name_en=user.full_name_en,
        mobile_number=user.mobile_number,
        national_id=user.national_id,
        address=user.address,
        city=user.city,
        total_credit=user.total_credit,
        balance_remaining=user.total_credit
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }