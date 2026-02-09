from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.users import User
from app.core.security import SECRET_KEY, ALGORITHM
from app.core.logger import logger
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        role = payload.get("role")
        owner_id = payload.get("owner_id")

        if not user_id or not role or not owner_id:
            logger.warning("JWT payload missing sub or role or owner_id")
            raise HTTPException(status_code=401, detail="Invalid token payload")

        logger.info(f"JWT validated for user_id={user_id}, role={role}, owner_id={owner_id}")

    except JWTError as e:
        logger.error(f"JWT validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        logger.warning(f"User not found for user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    # Attach owner context dynamically
    user.owner_id = int(owner_id)
    
    return user, role


def milkman_only(user_role=Depends(get_current_user)):
    user, role = user_role

    if role not in ["milkman", "owner_milkman"]:
        logger.warning(
            f"Unauthorized role access attempt | user_id={user.id} | role={role}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Milkman access only"
        )

    logger.info(f"Milkman access granted | user_id={user.id} | owner_id={user.owner_id}")
    return user
