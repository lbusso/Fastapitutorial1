
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blogs, users, authentication

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(authentication.router)
app.include_router(blogs.router)
app.include_router(users.router)

