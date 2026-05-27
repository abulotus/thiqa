from pydantic import BaseModel

# ---------------------------------------------------
# MERCHANT
# ---------------------------------------------------

class MerchantCreate(BaseModel):

    business_name: str
    owner_name: str
    mobile_number: str
    city: str

# ---------------------------------------------------
# USER
# ---------------------------------------------------

class UserCreate(BaseModel):

    merchant_id: int

    full_name: str
    mobile_number: str
    national_id: str

    city: str

    total_credit: float

# ---------------------------------------------------
# PAYMENT
# ---------------------------------------------------

class PaymentCreate(BaseModel):

    user_id: int

    amount_paid: float

    payment_method: str