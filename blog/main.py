from fastapi import FastAPI
from .schemas import Blog

app = FastAPI()


@app.post("/blog")
async def create(blog: Blog):
    return {'title': blog.title, 'body': blog.body}