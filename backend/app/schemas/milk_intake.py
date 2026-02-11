from pydantic import BaseModel, field_validator
from datetime import date

class MilkIntakeCreate(BaseModel):
    date: date
    session: str   # morning / evening
    customer_name: str
    quantity_liters: float
    rate_per_liter: float

    @field_validator("session")
    @classmethod
    def validate_session(cls, v: str):
        if v.lower() not in {"morning", "evening"}:
            raise ValueError("session must be 'morning' or 'evening'")
        return v.lower()
class MilkIntakeResponse(BaseModel):
    id: int
    date: date
    session: str
    customer_name: str
    quantity_liters: float
    rate_per_liter: float
    total_amount: float
    owner_id: int          # optional
    created_by: int        # optional

    class Config:
        from_attributes = True
