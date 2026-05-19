from sqlalchemy import Column, Integer,Boolean, String, ForeignKey, DateTime
from datetime import datetime
from src.utills.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# ===== UserModel ====
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    fullname = Column(String)
    mobile = Column(String,unique=True)
    email = Column(String, unique=True, index=True)
    username = Column(String,unique=True)
    password = Column(String)
    followercount = Column(Integer,default=0)
    followingcount = Column(Integer,default=0)

    posts = relationship("PostModel",back_populates="user")
    likes = relationship("LikeModel",back_populates="user")
    comments = relationship("CommentModel",back_populates="user") 
    
    follows = relationship(
        "FollowModel",
        foreign_keys="FollowModel.followerId",  
        back_populates="user"
    )

# ==== PostModel ====
class PostModel(Base):
    __tablename__ = "posts"
    
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    caption = Column(String)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    image = Column(String, nullable=True)
    likeCount = Column(Integer,default=0)
    commentcount = Column(Integer,default=0) 

    user = relationship("UserModel",back_populates="posts") 
    likes = relationship("LikeModel",back_populates="post",cascade="all, delete")
    comments = relationship("CommentModel",back_populates="post", cascade="all, delete")

# ===== Like Model ====
class LikeModel(Base):
    __tablename__ = "likes"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    post_id = Column(Integer,ForeignKey("posts.id"))

    user = relationship("UserModel",back_populates="likes")
    post = relationship("PostModel",back_populates="likes")    

# # ==== comments =====
class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    post_id = Column(Integer,ForeignKey("posts.id"))
    commentStr = Column(String)

    user = relationship("UserModel",back_populates="comments")
    post = relationship("PostModel",back_populates="comments")

#  ==== Follow Model =====
class FollowModel(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    followerId = Column(Integer, ForeignKey("users.id"))
    followingId = Column(Integer, ForeignKey("users.id"))

    user = relationship(
        "UserModel",
        foreign_keys=[followerId],
        back_populates="follows"
    )