from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.milk_intake import MilkIntake
from app.models.milk_sales import MilkSale

def get_owner_daily_summary(
    db: Session,
    owner_id: int,
    summary_date: date
):
    # Total intake
    intake = db.query(
        func.coalesce(func.sum(MilkIntake.quantity_liters), 0),
        func.coalesce(func.sum(MilkIntake.total_amount), 0)
    ).filter(
        MilkIntake.date == summary_date,
        MilkIntake.owner_id == owner_id
    ).first()

    total_intake_qty, total_intake_amount = intake

    # Total sales
    sales = db.query(
        func.coalesce(func.sum(MilkSale.quantity_liters), 0),
        func.coalesce(func.sum(MilkSale.total_amount), 0)
    ).filter(
        MilkSale.date == summary_date,
        MilkSale.owner_id == owner_id
    ).first()

    total_sold_qty, total_sales_amount = sales

    balance_qty = total_intake_qty - total_sold_qty
    profit = total_sales_amount - total_intake_amount

    return {
        "date": summary_date,
        "total_intake_qty": total_intake_qty,
        "total_sold_qty": total_sold_qty,
        "balance_qty": balance_qty,
        "total_intake_amount": total_intake_amount,
        "total_sales_amount": total_sales_amount,
        "profit": profit
    }
