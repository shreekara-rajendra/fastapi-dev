from typing import List, Optional
from fastapi import Depends, FastAPI,Request,Response,Header,HTTPException,status,APIRouter
from fastapi.params import Body
from fastapi.params import Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import schemas
from ..utils import hash
from ..utils import verify_password
from sqlalchemy import JSON, SQLColumnExpression
from .. import models
from ..database import SessionLocal, engine
from ..database import get_db
from .. import oauth2


router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login',response_model=schemas.Token)
async def login(credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    print(type(credentials))
    '''
    here credentials has username and password
    '''
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail ="invalid credentials")
    if not verify_password(credentials.password,user.password) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN   ,detail ="invalid credentials")
    #create token
    jwt_token = oauth2.create_jwt_token({'user_id':user.id})
    #return token
    return {"access_token":jwt_token,"token_type":"bearer"}
    
    
    
