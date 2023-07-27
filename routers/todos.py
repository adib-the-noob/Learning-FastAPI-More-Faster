from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from database import get_db
from models import Todos
from pydantic import BaseModel
from .jwt_generator import get_current_user

from typing import Annotated

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    id: int | None = None
    user : int | None = None
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


@router.get("/all-todos", status_code=status.HTTP_200_OK, response_model=list[TodoRequest])
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todos).all()
    return todos


@router.post("/create-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoRequest, user : user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})

    todo = Todos(**todo.model_dump(), user=user.get('id'))
    if todo is not None:
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.get('/get-todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@router.put('/update-todo/{todo_id}/')
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


@router.delete('/delete-todo/{todo_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is not None:
        db.delete(todo)
        db.commit()
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
