from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session 
from src.controller import user_controller
from src.dtos.userSchemas import LoginSchema, CreateAccountSchema
from src.utills.db import getDb
from src.utills.security import isLogin
from src.config.service import upload_image
from src.models.users import UserModel
user_routes = APIRouter(prefix="/users")
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
