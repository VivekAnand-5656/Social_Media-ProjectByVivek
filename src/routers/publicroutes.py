from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from src.utills.db import getDb
from src.controller import user_controller

router = APIRouter(prefix="/posts", tags=["Public"])

@router.get("/")
def getPosts(db:Session= Depends(getDb)):
    return user_controller.getPosts(db)

# ===== Get Posts Comments =====
@router.get("/postscomments/{postid}")
def commentByPosts(postid:int,db:Session = Depends(getDb)):
    return user_controller.getPostsComments(postid,db) 

# ==== Search Users ====
@router.get("/searchuser/{username}")
def searchuser(username:str,db:Session = Depends(getDb)):
    return user_controller.searchUser(username,db)