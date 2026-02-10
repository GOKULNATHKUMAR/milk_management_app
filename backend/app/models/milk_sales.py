from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class MilkSale(Base):
    __tablename__ = "milk_sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    session = Column(String, nullable=False)  # morning / evening
    customer_name = Column(String, nullable=True)

    quantity_liters = Column(Float, nullable=False)
    sale_rate = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, server_default=func.current_date())
