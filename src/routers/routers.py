from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session 
from src.controller import user_controller
from src.dtos.userSchemas import LoginSchema, CreateAccountSchema, CommentSchema
from src.utills.db import getDb
from src.utills.security import isLogin
from src.config.service import upload_image
from src.models.users import UserModel
user_routes = APIRouter(prefix="/users",tags=["User"])
@user_routes.get("/")
def meuser():
    return {
        "msg":"I am user"
    }
# ===== Create Account ====
@user_routes.post("/createaccount")
def accountCreate(body:CreateAccountSchema,db:Session = Depends(getDb)):
    return user_controller.createAccount(body,db)

@user_routes.post("/login")
def loginuser(body:LoginSchema,db:Session=Depends(getDb)):
    return user_controller.login(body,db)

# ==== Create Post ====
@user_routes.post("/createpost")
def createPost(
    caption: str = Form(...),
    file: UploadFile = File(...),
    db:Session = Depends(getDb),
    user:UserModel = Depends(isLogin)
):
    # imagePath = upload_image(file)

    return user_controller.createPost(
        caption,file,db,user
    )

# ==== Delete Posts ====
@user_routes.delete("/deletepost/{postid}")
def removePost(postid:int,db:Session = Depends(getDb),user:UserModel=Depends(isLogin)):
    return user_controller.deletePost(postid,db,user)
# ===== Get Posts ====
@user_routes.get("/myposts")
def myPosts(db:Session=Depends(getDb),user:UserModel=Depends(isLogin)):
    return user_controller.getMyPost(db,user)

# === Like Post ====
@user_routes.post("/likepost/{postid}")
def likePost(postid:int,db:Session = Depends(getDb),user:UserModel=Depends(isLogin)):
    return user_controller.likePosts(postid,db,user)

# === Comment on Post ====
@user_routes.post("/comment/{postid}")
def commentPost(postid:int,body:CommentSchema,db:Session = Depends(getDb),user:UserModel = Depends(isLogin)):
    return user_controller.comment(postid,body,db,user)

# ===== Get Posts Comments =====
@user_routes.get("/postscomments/{postid}")
def commentByPosts(postid:int,db:Session = Depends(getDb)):
    return user_controller.getPostsComments(postid,db) 

# ==== Search Users ====
@user_routes.get("/searchuser/{username}")
def searchuser(username:str,db:Session = Depends(getDb)):
    return user_controller.searchUser(username,db)

# ===== Follow Sections ======
@user_routes.post("/follow/{userid}")
def userFollow(userid:int,db:Session=Depends(getDb),user:UserModel=Depends(isLogin)):
    return user_controller.followUser(userid,db,user)

# ====== Unfollow ======
@user_routes.post("/unfollow/{userid}")
def userUnFollow(userid:int,db:Session=Depends(getDb),user:UserModel=Depends(isLogin)):
    return user_controller.unFollow(userid,db,user)
# ============= Follow Section Reh gya hai bhai =======
