from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import engine
from database import Base
from database import get_db

import models as models
import schemas as schemas
import crud as crud

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
