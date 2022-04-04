from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail='EL blog no existe')
    return blog

def create(db: Session, request):
    new_blog = models.Blog(title=request.title, body=request.body, creator_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=(f'EL blog con id: {id} no existe'))

    blog.delete(synchronize_session=False)
    db.commit()
    return 'Done'

def update(db: Session, id, request):
    db.query(models.Blog).filter(models.Blog.id == id, ).update({'title': request.title, 'body': request.body})
    db.commit()
    return 'blog Update'