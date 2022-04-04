from fastapi import APIRouter, Depends, HTTPException
from .blogs import models, schemas
from sqlalchemy.orm import Session
from blog.database import get_db
from .. repository import user

router = APIRouter(
    prefix= '/users',
    tags=['users']
)


@router.post('/user_create',)
async def Create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(db, request)


@router.get('/detail/{user_id}', status_code=200, response_model=schemas.ShowUser,)
async def show_user(user_id, db: Session = Depends(get_db),):
    return user.show(user_id, db)