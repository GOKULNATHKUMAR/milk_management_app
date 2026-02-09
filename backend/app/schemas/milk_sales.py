from pydantic import BaseModel
from datetime import date

class MilkSaleCreate(BaseModel):
    date: date
    session: str
    customer_name: str | None = None
    quantity_liters: float
    sale_rate: float

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
