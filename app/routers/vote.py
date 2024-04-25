from multiprocessing.sharedctypes import Synchronized, synchronized
from fastapi import APIRouter, Depends, HTTPException,status
from httpx import delete
from sqlalchemy.orm import Session
from .. import models
from app.oauth2 import get_current_user
from .. import schemas,database
router =  APIRouter(
    prefix = '/votes',
    tags = ['vote_model']
)
 
@router.post('/',status_code = status.HTTP_201_CREATED)
async def create_vote(vote: schemas.VoteRequest,db : Session = Depends(database.get_db), user_id : schemas.TokenData = Depends(get_current_user)):
    like_exit = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()
    if not like_exit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"the post id {vote.post_id} doesnt exist")
    found_row = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == user_id.id)
    if(vote.dir == 1):
        if found_row.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = f"user {user_id.id} has already voted post {vote.post_id}")
        else :
            new_like = models.Vote(user_id = user_id.id,post_id = vote.post_id)
            db.add(new_like)
            db.commit()
            return {"message":"successfully added vote"}
    else:
        if found_row.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"the given post has not been liked")
        else :
            found_row.delete(synchronize_session = False)
            db.commit()
            return  {"message":"successfully deleted vote"}
        
    
        
