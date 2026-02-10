from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.deps import milkman_only
from app.services.daily_summary import get_owner_daily_summary
from app.utils.whatsapp import build_whatsapp_message, generate_whatsapp_link
from app.deps import cron_only
from app.models.users import User
from app.models.milk_intake import MilkIntake
from app.models.milk_sales import MilkSale
from sqlalchemy import func

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/daily/manual")
def daily_summary(
    summary_date: date = date.today(),
    db: Session = Depends(get_db),
    user = Depends(milkman_only)
):
    summary = get_owner_daily_summary(
        db=db,
        owner_id=user.owner_id,
        summary_date=summary_date
    )

    message = build_whatsapp_message(summary)
    link = generate_whatsapp_link(user.mobile, message)

    return {
        "whatsapp_link": link
    }

@router.post("/daily")
def daily_summary(
    db: Session = Depends(get_db),
    _ = Depends(cron_only)
):
    today = date.today()

    owners = db.query(User).filter(User.role == "owner").all()

    results = []

    for owner in owners:
        intake_total = db.query(
            func.coalesce(func.sum(MilkIntake.total_amount), 0)
        ).filter(
            MilkIntake.date == today,
            MilkIntake.owner_id == owner.id
        ).scalar()

        sales_total = db.query(
            func.coalesce(func.sum(MilkSale.total_amount), 0)
        ).filter(
            MilkSale.date == today,
            MilkSale.owner_id == owner.id
        ).scalar()

        profit = sales_total - intake_total

        # WhatsApp trigger (FREE method)
        whatsapp_url = (
            f"https://wa.me/{owner.mobile}"
            f"?text=🧾 Daily Milk Summary ({today})%0A"
            f"🥛 Intake: ₹{intake_total}%0A"
            f"💰 Sales: ₹{sales_total}%0A"
            f"📈 Profit: ₹{profit}"
        )

        results.append({
            "owner": owner.name,
            "mobile": owner.mobile,
            "whatsapp_url": whatsapp_url
        })

    return {
        "date": today,
        "owners": results
    }
