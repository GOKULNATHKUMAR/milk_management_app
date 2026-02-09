from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class MilkIntake(Base):
    __tablename__ = "milk_intake"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    session = Column(String, nullable=False)  # morning / evening

    quantity_liters = Column(Float, nullable=False)
    rate_per_liter = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    # NEW: Business owner
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
