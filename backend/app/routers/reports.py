from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import date
import calendar
from app.database import get_db
from app.deps import milkman_only, owner_only
from app.services.daily_summary import get_owner_daily_summary
from app.utils.whatsapp import build_whatsapp_message, generate_whatsapp_link
from app.deps import cron_only, get_current_user
from app.models.users import User
from app.models.milk_intake import MilkIntake
from app.models.milk_sales import MilkSale
from sqlalchemy import func

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/daily/manual")
def daily_summary(
    summary_date: date = date.today(),
    db: Session = Depends(get_db),
    user: User = Depends(owner_only)
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


@router.get("/monthly")
def monthly_report(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(owner_only)
):
    if current_user.role not in ["owner", "owner_milkman"]:
        raise HTTPException(status_code=403, detail="Only owner can download report")

    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])

    intake_records = db.query(MilkIntake).filter(
        MilkIntake.owner_id == current_user.id,
        MilkIntake.date.between(start_date, end_date)
    ).order_by(MilkIntake.date).all()
    print(f"Intake records found: {len(intake_records)} for owner_id={current_user.id} between {start_date} and {end_date}")
    sale_records = db.query(MilkSale).filter(
        MilkSale.owner_id == current_user.id,
        MilkSale.date.between(start_date, end_date)
    ).order_by(MilkSale.date).all()
    print(f"Sale records found: {len(sale_records)} for owner_id={current_user.id} between {start_date} and {end_date}")
    total_intake = sum(r.total_amount for r in intake_records)
    total_sales = sum(r.total_amount for r in sale_records)

    profit = total_sales - total_intake
    loss = 0
    if profit < 0:
        loss = abs(profit)
        profit = 0

    file_path = f"monthly_report_{year}_{month}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=pagesizes.A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Monthly Milk Report - {month}/{year}", styles["Heading1"]))
    elements.append(Spacer(1, 12))

    # Intake Table
    intake_data = [["Date", "Customer", "Session", "Qty", "Rate", "Total"]]
    for r in intake_records:
        intake_data.append([
            str(r.date),
            r.customer_name,
            r.session,
            r.quantity_liters,
            r.rate_per_liter,
            r.total_amount
        ])

    intake_table = Table(intake_data)
    intake_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))

    elements.append(Paragraph("Milk Intake Details", styles["Heading2"]))
    elements.append(intake_table)
    elements.append(Spacer(1, 20))

    # Sales Table
    sale_data = [["Date", "Customer", "Session", "Qty", "Rate", "Total"]]
    for r in sale_records:
        sale_data.append([
            str(r.date),
            r.customer_name,
            r.session,
            r.quantity_liters,
            r.sale_rate,
            r.total_amount
        ])

    sale_table = Table(sale_data)
    sale_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))

    elements.append(Paragraph("Milk Sales Details", styles["Heading2"]))
    elements.append(sale_table)
    elements.append(Spacer(1, 20))

    # Summary
    summary_data = [
        ["Total Intake", total_intake],
        ["Total Sales", total_sales],
        ["Profit", profit],
        ["Loss", loss],
    ]

    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))

    elements.append(Paragraph("Summary", styles["Heading2"]))
    elements.append(summary_table)

    doc.build(elements)

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=file_path
    )