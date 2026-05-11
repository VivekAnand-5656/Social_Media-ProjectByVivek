from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from src.utills.db import getDb
from src.controller import user_controller

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/")
def getPosts(db:Session= Depends(getDb)):
    return user_controller.getPosts(db)