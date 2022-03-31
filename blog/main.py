
from fastapi import Depends, FastAPI, status, Response, HTTPException
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
async def get_blog_list(db: Session = Depends(get_db)):

    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{blog_id}')
async def blog_detail(blog_id, response:  Response, db: Session = Depends(get_db),):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='EL blog no existe')
    return blog

@app.put('/blog/{blog_id}')
async def blog_update(blog_id, request: schemas.Blog, db: Session = Depends(get_db),):
    db.query(models.Blog).filter(models.Blog.id==blog_id,).update({'title': request.title, 'body': request.body})
    db.commit()
    return 'blog Update'


    
@app.post("/blog_create", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{blog_id}')
async def blog_delete(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).delete(synchronize_session=False)
    db.commit()

    return 'Done'