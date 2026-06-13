from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    phone_number: str
    password: str