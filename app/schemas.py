from datetime import datetime
from typing import Annotated, Optional, Union
from pydantic import BaseModel, EmailStr, Field, conint

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True
    rating:Optional[int] = 0

class PostCreate(PostBase):
    pass 

class PostUpdate(PostBase):
    pass 

class ResponseUser(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class config: 
        orm_mode = True
        
class ResponsePost(BaseModel):
    id : int
    title:str
    content:str
    published:bool 
    rating:int
    created_at : datetime
    owner_id : int
    owner : ResponseUser
    
    class config :
        orm_mode = True
    
class CreateUser(BaseModel):
    email : EmailStr
    password : str

class ResponseUser(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class config: 
        orm_mode = True

    
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
class Token (BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None
    
class VoteRequest(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, ge=0,le=1)]

class PostOut(BaseModel):
    Post: ResponsePost
    votes: int

    class Config:
        orm_mode = True
