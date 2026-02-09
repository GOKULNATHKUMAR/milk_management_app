from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.schemas.milk_sales import MilkSaleCreate, MilkSaleResponse
from app.models.milk_sales import MilkSale
from app.models.milk_intake import MilkIntake
from app.deps import milkman_only

router = APIRouter(prefix="/milk-sales", tags=["Milk Sales"])

@router.post("/", response_model=MilkSaleResponse)
def add_milk_sale(
    data: MilkSaleCreate,
    db: Session = Depends(get_db),
    user = Depends(milkman_only)
):
    # Get total intake for that date & session
    intake = db.query(MilkIntake).filter(
        MilkIntake.date == data.date,
        MilkIntake.session == data.session.lower(),
        MilkIntake.created_by == user.id
    ).first()
    print("Intake found:", intake)

    if not intake:
        raise HTTPException(status_code=400, detail="No milk intake found")

    # Calculate already sold milk
    sold_qty = db.query(MilkSale).filter(
        MilkSale.date == data.date,
        MilkSale.session == data.session.lower(),
        MilkIntake.created_by == user.id
    ).with_entities(
        func.coalesce(func.sum(MilkSale.quantity_liters), 0)
    ).scalar()

    if sold_qty + data.quantity_liters > intake.quantity_liters:
        raise HTTPException(
            status_code=400,
            detail="Not enough milk available"
        )

    total = data.quantity_liters * data.sale_rate

    sale = MilkSale(
        date=data.date,
        session=data.session.lower(),
        customer_name=data.customer_name,
        quantity_liters=data.quantity_liters,
        sale_rate=data.sale_rate,
        total_amount=total,
        created_by=user.id
    )

    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale
