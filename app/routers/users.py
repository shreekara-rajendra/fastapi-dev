from typing import List, Optional
from fastapi import Depends, FastAPI,Request,Response,Header,HTTPException,status,APIRouter
from fastapi.params import Body
from fastapi.params import Header
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import schemas
from ..utils import hash

from sqlalchemy import JSON, SQLColumnExpression
from .. import models
from ..database import SessionLocal, engine
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags = ['users']
)
@router.post('/',response_model=schemas.ResponseUser)
async def createuser(user : schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**dict(user))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model= schemas.ResponseUser)
async def getuser(id : int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "user with id {id} not found")
    return user