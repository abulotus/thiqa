from sqlalchemy.orm import Session

from models import Merchant
from models import User
from models import Payment

# ---------------------------------------------------
# CREATE MERCHANT
# ---------------------------------------------------

def create_merchant(
    db: Session,
    merchant_data
):

    merchant = Merchant(

        business_name=
            merchant_data.business_name,

        owner_name=
            merchant_data.owner_name,

        mobile_number=
            merchant_data.mobile_number,

        city=
            merchant_data.city
    )

    db.add(merchant)

    db.commit()

    db.refresh(merchant)

    return merchant

# ---------------------------------------------------
# CREATE USER
# ---------------------------------------------------

def create_user(
    db: Session,
    user_data
):

    user = User(

        merchant_id=
            user_data.merchant_id,

        full_name=
            user_data.full_name,

        mobile_number=
            user_data.mobile_number,

        national_id=
            user_data.national_id,

        city=
            user_data.city,

        total_credit=
            user_data.total_credit,

        balance_remaining=
            user_data.total_credit
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user

# ---------------------------------------------------
# ADD PAYMENT
# ---------------------------------------------------

def add_payment(
    db: Session,
    payment_data
):

    user = db.query(User).filter(
        User.id == payment_data.user_id
    ).first()

    if not user:
        return None

    payment = Payment(

        user_id=
            payment_data.user_id,

        amount_paid=
            payment_data.amount_paid,

        payment_method=
            payment_data.payment_method
    )

    user.balance_remaining -= (
        payment_data.amount_paid
    )

    if user.balance_remaining < 0:
        user.balance_remaining = 0

    db.add(payment)

    db.commit()

    db.refresh(payment)

    return payment