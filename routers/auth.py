from fastapi import APIRouter, Depends

from models import User
from database import db_dependency
from pydantic import BaseModel

# for password hash
from passlib.context import CryptContext

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


class UserRequest(BaseModel):
    email: str
    full_name: str
    username: str
    password: str


@router.post("/create-user")
async def register_user(user_request: UserRequest, db: db_dependency):
    user = User(
        email=user_request.email,
        full_name=user_request.full_name,
        username=user_request.username,
        hashed_password=bcrypt.hash(user_request.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user