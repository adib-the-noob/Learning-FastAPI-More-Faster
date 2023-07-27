from typing import Annotated
from fastapi import APIRouter, Depends

from models import User
from database import db_dependency, get_db
from pydantic import BaseModel

# for password hash
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from .jwt_generator import generate_access_token
from datetime import timedelta

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


def authenticate_user(username :str, password : str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt.verify(password, user.hashed_password):
        return False
    return user


@router.post("/login-token")
async def login_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is not None:
        token = generate_access_token(user.username, user.id, timedelta(minutes=30))
        return {
            "access_token": token,
            "token_type": "bearer",
        }
    return {"error": "invalid credentials"}