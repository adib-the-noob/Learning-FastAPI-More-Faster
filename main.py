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
    id: int | None = None
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


@app.get("/all-todos", status_code=status.HTTP_200_OK)
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todos).all()
    return todos


@app.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoRequest, db: Session = Depends(get_db)):
    todo = Todos(**todo.model_dump())
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


@app.put('/update-todo/{todo_id}/')
async def update_todo_by_id(todo_id: int, todo_request: TodoRequest, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.completed = todo_request.completed
        db.commit()
        db.refresh(todo)
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete('/delete-todo/{todo_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        db.delete(todo)
        db.commit()
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
