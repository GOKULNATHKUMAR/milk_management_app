import sys
import os
from datetime import date

# Make app importable
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.users import User
from app.services.daily_summary import get_owner_daily_summary
from app.utils.whatsapp import build_whatsapp_message, generate_whatsapp_link

db = SessionLocal()

owners = db.query(User).filter(User.role == "owner").all()

for owner in owners:
    summary = get_owner_daily_summary(
        db=db,
        owner_id=owner.id,
        summary_date=date.today()
    )

    message = build_whatsapp_message(summary)
    link = generate_whatsapp_link(owner.mobile, message)

    print(f"[AUTO 9PM] {owner.name} → {link}")

db.close()
