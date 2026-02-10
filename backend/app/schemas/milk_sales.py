from pydantic import BaseModel, field_validator
from datetime import date

class MilkSaleCreate(BaseModel):
    date: date
    session: str
    customer_name: str | None = None
    quantity_liters: float
    sale_rate: float
    
    @field_validator("session")
    @classmethod
    def validate_session(cls, v: str):
        if v.lower() not in {"morning", "evening"}:
            raise ValueError("session must be morning or evening")
        return v.lower()

class MilkSaleResponse(BaseModel):
    id: int
    date: date
    session: str
    customer_name: str | None
    quantity_liters: float
    sale_rate: float
    total_amount: float

    class Config:
        from_attributes = True
