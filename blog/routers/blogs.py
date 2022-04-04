from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from blog import schemas, models
from typing import List
from blog.database import SessionLocal, get_db
from ..repository import blog



router =  APIRouter(
    prefix="/blogs",
    tags=['blogs']
    )

@router.get("/blog-list", response_model=List[schemas.BlogDetail],)
async def get_blog_list(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.get('/detail/{blog_id}', status_code=200, response_model=schemas.BlogDetail,)
async def blog_detail(blog_id, db: Session = Depends(get_db),):
    return blog.show(blog_id, db)


@router.post("/blog_create", status_code=status.HTTP_201_CREATED, )
async def create(request: schemas.Blog, db: Session = Depends(get_db), ):
    return blog.create(db, request)


@router.put('/update/{blog_id}',)
async def blog_update(blog_id, request: schemas.Blog, db: Session = Depends(get_db),):
    return blog.update(db,blog_id, request, )


@router.delete('/delete/{blog_id}',)
async def blog_delete(blog_id, db: Session = Depends(get_db)):
    return blog.delete(db, blog_id,)