from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password, encrypt_phone

router = APIRouter()

@router.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username= user.username,
        hashed_password = hash_password(user.password),
        encrypted_phone_number = encrypt_phone(user.phone_number)
    )

    db.add(new_user)
    db.commit()
    return {"massege": "user created"}