from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import engine
from app.database import Base
from app.database import get_db

import app.models as models
import app.schemas as schemas
import app.crud as crud

# ---------------------------------------------------
# CREATE TABLES
# ---------------------------------------------------

models.Base.metadata.create_all(
    bind=engine
)

# ---------------------------------------------------
# FASTAPI
# ---------------------------------------------------

app = FastAPI()

# ---------------------------------------------------
# ROOT
# ---------------------------------------------------

@app.get("/")

def root():

    return {
        "message": "Thiqa API Running"
    }

# ---------------------------------------------------
# ADD MERCHANT
# ---------------------------------------------------

@app.post("/merchants")

def create_merchant(

    merchant: schemas.MerchantCreate,

    db: Session = Depends(get_db)
):

    return crud.create_merchant(
        db,
        merchant
    )

# ---------------------------------------------------
# ADD USER
# ---------------------------------------------------

@app.post("/users")

def create_user(

    user: schemas.UserCreate,

    db: Session = Depends(get_db)
):

    return crud.create_user(
        db,
        user
    )

# ---------------------------------------------------
# ADD PAYMENT
# ---------------------------------------------------

@app.post("/payments")

def add_payment(

    payment: schemas.PaymentCreate,

    db: Session = Depends(get_db)
):

    result = crud.add_payment(
        db,
        payment
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return result
