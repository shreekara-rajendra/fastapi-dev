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
from .. import oauth2
from sqlalchemy import JSON, SQLColumnExpression
from .. import models
from ..database import SessionLocal, engine
from ..database import get_db
from sqlalchemy import func
router = APIRouter(
    prefix='/posts',
    tags = ['posts']
)




@router.get("/",response_model= List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db) ,limit : int = 5,skip : int = 0,search : Optional[str] = ""):
    ## without using orm
    '''
    cursor.execute("""SELECT * FROM posts""")
    posts =  cursor.fetchall()
    print(posts)
    return {'data' : posts}
    print("yes")
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    print(posts)
    #cursor.execute(f""" SELECT * FROM posts where title ilike '%{search}%' """,)
    return posts
    #return cursor.fetchall()
    '''
    rows = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    return rows
    

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_post(post : schemas.PostCreate,db: Session = Depends(get_db), user_id : schemas.TokenData  = Depends(oauth2.get_current_user)):
    '''
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published))
    post = cursor.fetchone()
    conn.commit()
    print(type(post))
    return {'data':post}
    '''
    ## **post is used to unpack a dictionary
    post = dict(post)
    post.update({"owner_id":user_id.id})
    new_post = models.Post(**post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id : int,db: Session = Depends(get_db)):
    ##the type hint should be int so that some nonsense string cant be set as id
    '''
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with id {id} not found")
    return {"data" : post}
    '''
    ##join is by default left inner join , so we need to pass outer parameter
    rows = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with id {id} not found")
    return rows

    
    
    
#generally we dont send anything with delete operation
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db: Session = Depends(get_db),user_id:schemas.TokenData = Depends(oauth2.get_current_user)):
    '''
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    deletedpost = cursor.fetchone()
    conn.commit()
    if not deletedpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    '''
    posts = db.query(models.Post).filter(models.Post.id == id)
    if posts.first() is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"the id {id} was not found")
    if posts.first().owner_id != user_id.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail =f"you arent allowed" )
    posts.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    
    
@router.put("/{id}",response_model = schemas.ResponsePost)
async def update_post(id:int,post:schemas.PostUpdate,db : Session = Depends(get_db),user_id:schemas.TokenData = Depends(oauth2.get_current_user)):
    '''
    cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s returning * """,(str(post.title),str(post.content),str(post.published),str(id)))
    updated_post = cursor.fetchall()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "not found")
    return {"data":updated_post}
    '''
    posts = db.query(models.Post).filter(models.Post.id == id)
    if posts.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"id {id} doesnt exist")
    if posts.first().owner_id != user_id.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail =f"you arent allowed" )
    posts.update(dict(post),synchronize_session=False)
    db.commit()
    return posts.first()
    ## we need to send a dictionary in update, we can convert pydantic to dict

