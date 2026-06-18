from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.core.security import (
    hash_password,
    encrypt_phone,
    verify_password,
    create_access_token,
)
from app.services.auth_service import get_current_user

router = APIRouter()


# route for user creation
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        encrypted_phone_number=encrypt_phone(user.phone_number),
    )

    db.add(new_user)
    db.commit()
    return {"massege": "user created"}


# user login route
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        return {"message": "user not found"}
    if not verify_password(user.password, db_user.hashed_password):
        return {"message": "invalid password"}

    token = create_access_token({"sub": db_user.username})
    return {
        "message": "login successful",
        "access_token": token,
        "token_type": "bearer",
    }


# ==================== get the current logged in user details ============
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username}
