from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
