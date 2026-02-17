from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.users import User
from app.schemas.user import OwnerRegister, MilkmanCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import Token
from app.core.hashing import hash_password, verify_password
from app.core.security import create_access_token
from app.deps import get_current_user
router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Owner Self Registration (Public)
@router.post("/register-owner")
def register_owner(user: OwnerRegister, db: Session = Depends(get_db)):

    if db.query(User).filter(User.mobile == user.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile already registered")

    new_owner = User(
        name=user.name,
        mobile=user.mobile,
        password=hash_password(user.password),
        role="owner",
        language=user.language
    )

    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)

    # If owner also acts as milkman → self mapping
    if user.is_milkman:
        new_owner.owner_id = new_owner.id
        db.commit()

    return {"message": "Owner registered successfully"}

# Owner Adds Milkman (Protected API)
@router.post("/add-milkman")
def add_milkman(
    milkman: MilkmanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can add milkman")

    if db.query(User).filter(User.mobile == milkman.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile already registered")

    new_milkman = User(
        name=milkman.name,
        mobile=milkman.mobile,
        password=hash_password(milkman.password),
        role="milkman",
        owner_id=current_user.id,
        language=milkman.language
    )

    db.add(new_milkman)
    db.commit()
    db.refresh(new_milkman)

    return {"message": "Milkman added successfully"}

@router.get("/milkmen")
def get_milkmen(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can view milkmen")

    milkmen = db.query(User).filter(
        User.owner_id == current_user.id,
        User.role == "milkman"
    ).all()

    return milkmen

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
    #print(f"Generated token for user {user.role} (ID: {user.id}): {token}")
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.id
    }
