from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

# ================ passward hashing ====================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


# =============== Encrypting Phone numbe r=================

load_dotenv()

cipher = Fernet(os.getenv("ENCRYPTION_KEY"))


def encrypt_phone(phone: str):
    return cipher.encrypt(phone.encode()).decode()


def decrypt_phone(encrypted_phone: str):
    return cipher.decrypt(encrypted_phone.encode()).decode()


# ===== compairing users given password to its hashed password =====


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ================== create access token ==========================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            return None
        return username

    except JWTError:
        return None
    
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='login'
)
