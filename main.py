from fastapi import FastAPI, Depends, HTTPException, Path
import models
from database import engine, SessionLocal

from sqlalchemy.orm import Session
from models import Todos

from pydantic import BaseModel

from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


@app.get("/all-todos", status_code=status.HTTP_200_OK)
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todos).all()
    return todos


@app.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoRequest, db: Session = Depends(get_db)):
    todo = Todos(title=todo.title, description=todo.description, completed=todo.completed)
    if todo is not None:
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.get('/get-todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")
