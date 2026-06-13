# uvicorn app.main:app --reload
from fastapi import FastAPI

from app.db.database import Base, engine
from app.api.users import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)

@app.get('/')
def root():
    return {'message': 'hello YOU!'}