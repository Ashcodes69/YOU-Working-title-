from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_token, oauth2_scheme
from app.models.user import User
from app.db.session import get_db


# ==================== get the current logged in user details ============
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="invalid token")

    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")

    return db_user
