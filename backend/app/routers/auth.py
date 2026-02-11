from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.users import User
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.core.hashing import hash_password, verify_password
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.mobile == user.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile already registered")
    # Role validation
    if user.role in ["milkman", "owner_milkman"] and not user.owner_id:
        raise HTTPException(
            status_code=400,
            detail=f"{user.role} must be linked to an owner"
        )
    new_user = User(
        name=user.name,
        mobile=user.mobile,
        password=hash_password(user.password),
        role=user.role,
        owner_id=user.owner_id,
        language=user.language
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Swagger uses "username" → we map it to mobile
    user = db.query(User).filter(User.mobile == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "mobile": user.mobile,
        "role": user.role,
        "owner_id": user.owner_id or user.id  # KEY LINE
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
