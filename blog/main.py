
from fastapi import Depends, FastAPI, status, Response, HTTPException
from . import schemas, models
from typing import List
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .hashing import Hash


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


app = FastAPI()


@app.get("/blog-list", response_model=List[schemas.BlogDetail], tags=['blogs'])
async def get_blog_list(db: Session = Depends(get_db)):

    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{blog_id}', status_code=200, response_model=schemas.BlogDetail,tags=['blogs'])
async def blog_detail(blog_id, response:  Response, db: Session = Depends(get_db),):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='EL blog no existe')
    return blog


@app.post("/blog_create", status_code=status.HTTP_201_CREATED, tags=['blogs'])
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put('/blog/{blog_id}', tags=['blogs'])
async def blog_update(blog_id, request: schemas.Blog, db: Session = Depends(get_db),):
    db.query(models.Blog).filter(models.Blog.id==blog_id,).update({'title': request.title, 'body': request.body})
    db.commit()
    return 'blog Update'


@app.delete('/blog/{blog_id}', tags=['blogs'])
async def blog_delete(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f'EL blog con id: {blog_id} no existe'))

    blog.delete(synchronize_session=False)
    db.commit()

    return 'Done'


@app.post('user/user_create', tags=['users'])
async def Create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{user_id}', status_code=200, response_model=schemas.ShowUser, tags=['users'])
async def show_user(user_id, db: Session = Depends(get_db),):
    user = db.query(models.User).filter(models.User.id ==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='EL Usuario no existe')
    return user