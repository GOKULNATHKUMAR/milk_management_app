from pydantic import BaseModel

class SessionSummary(BaseModel):
    quantity: float
    amount: float

class DailySummaryResponse(BaseModel):
    date: str

    intake_morning: SessionSummary
    intake_evening: SessionSummary
    intake_total: SessionSummary

    sold_morning: SessionSummary
    sold_evening: SessionSummary
    sold_total: SessionSummary

    remaining_milk: float
