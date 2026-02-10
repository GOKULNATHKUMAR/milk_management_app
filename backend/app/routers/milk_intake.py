from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.milk_intake import MilkIntakeCreate, MilkIntakeResponse
from app.models.milk_intake import MilkIntake
from app.models.users import User
from app.deps import milkman_only
from datetime import date

router = APIRouter(prefix="/milk-intake", tags=["Milk Intake"])

@router.post("/", response_model=MilkIntakeResponse)
def add_milk_intake(
    data: MilkIntakeCreate,
    db: Session = Depends(get_db),
    user: User = Depends(milkman_only)
):
    total = data.quantity_liters * data.rate_per_liter

    intake = MilkIntake(
        date=data.date,
        session=data.session.lower(),
        quantity_liters=data.quantity_liters,
        rate_per_liter=data.rate_per_liter,
        total_amount=total,
        owner_id=user.owner_id,
        created_by=user.id
    )

    db.add(intake)
    db.commit()
    db.refresh(intake)
    return intake


@router.get("/", response_model=list[MilkIntakeResponse])
def get_milk_intake(
    date: date,
    session: str,
    db: Session = Depends(get_db),
    user: User = Depends(milkman_only)
):
    return db.query(MilkIntake).filter(
        MilkIntake.date == date,
        MilkIntake.session == session.lower(),
        MilkIntake.owner_id == user.owner_id
    ).all()
