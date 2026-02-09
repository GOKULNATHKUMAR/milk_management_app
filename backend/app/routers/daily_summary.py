from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.milk_intake import MilkIntake
from app.models.milk_sales import MilkSale
from app.schemas.daily_summary import DailySummaryResponse, SessionSummary
from app.deps import milkman_only

router = APIRouter(prefix="/daily-summary", tags=["Daily Summary"])

@router.get("/", response_model=DailySummaryResponse)
def get_daily_summary(
    date: str,
    db: Session = Depends(get_db),
    user = Depends(milkman_only)
):
    def intake(session):
        qty, amt = db.query(
            func.coalesce(func.sum(MilkIntake.quantity_liters), 0),
            func.coalesce(func.sum(MilkIntake.total_amount), 0)
        ).filter(
            MilkIntake.date == date,
            MilkIntake.session == session,
            MilkIntake.created_by == user.id
        ).one()
        return qty, amt

    def sales(session):
        qty, amt = db.query(
            func.coalesce(func.sum(MilkSale.quantity_liters), 0),
            func.coalesce(func.sum(MilkSale.total_amount), 0)
        ).filter(
            MilkSale.date == date,
            MilkSale.session == session,
            MilkSale.created_by == user.id
        ).one()
        return qty, amt

    im_q, im_a = intake("morning")
    ie_q, ie_a = intake("evening")

    sm_q, sm_a = sales("morning")
    se_q, se_a = sales("evening")

    return {
        "date": date,

        "intake_morning": {"quantity": im_q, "amount": im_a},
        "intake_evening": {"quantity": ie_q, "amount": ie_a},
        "intake_total": {
            "quantity": im_q + ie_q,
            "amount": im_a + ie_a
        },

        "sold_morning": {"quantity": sm_q, "amount": sm_a},
        "sold_evening": {"quantity": se_q, "amount": se_a},
        "sold_total": {
            "quantity": sm_q + se_q,
            "amount": sm_a + se_a
        },

        "remaining_milk": (im_q + ie_q) - (sm_q + se_q)
    }
