from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.message import Message
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter()
# ================== route to fetch message =================
@router.get("/messages/{user_id}")
def get_messages(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    messages = (
        db.query(Message)
        .filter(
            (
                (Message.sender_id == current_user.id) & 
                (Message.receiver_id == user_id))
            | (
                (Message.sender_id == user_id) & 
                (Message.receiver_id == current_user.id)
            )
        )
        .all()
    )

    return messages
