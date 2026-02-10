from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.deps import milkman_only
from app.services.daily_summary import get_owner_daily_summary
from app.utils.whatsapp import build_whatsapp_message, generate_whatsapp_link

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/daily-summary")
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
