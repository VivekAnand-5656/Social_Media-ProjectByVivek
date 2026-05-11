from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from src.utills.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    fullname = Column(String)
    mobile = Column(String,unique=True)
    email = Column(String, unique=True, index=True)
    username = Column(String,unique=True)
    password = Column(String)
    posts = relationship("PostModel",back_populates="user")

class PostModel(Base):
    __tablename__ = "posts"
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    caption = Column(String)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    image = Column(String, nullable=True)
    user = relationship("UserModel",back_populates="posts")
