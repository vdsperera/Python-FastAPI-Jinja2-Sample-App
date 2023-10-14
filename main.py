# https://tutorial101.blogspot.com/2023/01/python-fastapi-to-do-with-jinja2.html

from typing import Union
from fastapi import FastAPI, Request, Depends, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine



models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="./templates")

app = FastAPI()

def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        

@app.post("/add")
def add(request: Request, title: str = Form(...), db_session: Session = Depends(get_db)):
    todo = models.Todo(title=title)
    db_session.add(todo)
    db_session.commit()

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/", name="root") 
def home(request: Request, db_session: Session = Depends(get_db)):
    todos = db_session.query(models.Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


@app.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db_session.commit()

    root_url = app.url_path_for("root")
    return RedirectResponse(url=root_url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db_session.delete(todo)
    db_session.commit()

    root_url = app.url_path_for("root")
    return RedirectResponse(url=root_url, status_code=status.HTTP_302_FOUND)
