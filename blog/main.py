from fileinput import close
from gc import get_debug
from pyexpat import model
from turtle import title
from urllib import request
from fastapi import Depends, FastAPI
from .schemas import Blog
from . import schemas, models

from sqlalchemy.orm import Session

from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


app = FastAPI()


@app.get("/blog-list")
async def get_blog_list():
    return {'Lista de blogs'}
    
@app.post("/blog")
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog