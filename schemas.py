from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name_ar: str
    full_name_en: str
    mobile_number: str
    national_id: str
    address: str
    city: str
    total_credit: float