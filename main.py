from turtle import home
from typing import Optional
from fastapi import FastAPI
from enum import Enum
import uvicorn
from models import Blog


app = FastAPI()

@app.get("/blog")
async def index(limit=10,  published: bool=True, sort: Optional[str] = None):
    if published:
        return {'data' : f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from db'}
    

@app.get('/blog/unpublished')
async def unpublished():
    return {'devolver blogs no publicados'}


@app.get("/blog/{blog_id}")
async def show_blog(blog_id: int):
   # mostrar blog con blog id
  return {
      'data': blog_id 
  }


@app.get('/blog/{blog_id}/comments')
async def blog_coments(blog_id: int, limit=10):
    return {'data':{'1': 'primer comentario', '2': 'Segundo comentario'}}


@app.post('/blog')
async def create_blog(blog: Blog):
    return {'Data': f'Blog is created: {blog.title}',}


