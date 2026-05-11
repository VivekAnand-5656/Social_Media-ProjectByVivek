from jose import jwt
from datetime import datetime, timedelta
from src.utills.setting import setting
from pwdlib import PasswordHash
from src.dtos.userSchemas import LoginSchema, CreateAccountSchema, PostSchema
from src.models.users import UserModel, PostModel
from src.config.service import upload_image
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.utills.security import isLogin
password_hash = PasswordHash.recommended()

# ==== Password Hashing =====
def getPasswordHash(password):
    return password_hash.hash(password)

def verifyPassword(plain_password,hash_password):
    return password_hash.verify(plain_password,hash_password)

# ==== Create Account =====
def createAccount(body:CreateAccountSchema,db:Session):
    userEmail = db.query(UserModel).filter(UserModel.email == body.email).first()
    userMobile = db.query(UserModel).filter(UserModel.mobile == body.mobile).first()
    userUsername = db.query(UserModel).filter(UserModel.username == body.username).first()
    userPassword = db.query(UserModel).filter(UserModel.password == body.password).first()
    if userEmail:
        raise HTTPException(400,detail="Email already exists")
    if userMobile:
        raise HTTPException(400,detail="Mobile already exists")
    if userUsername:
        raise HTTPException(400,detail="Username already exists")
    if userPassword:
        raise HTTPException(400,detail="Password already exists")
    hashed_pwd = getPasswordHash(body.password)
    newUser = UserModel(
        fullname = body.fullname,
        mobile = body.mobile,
        email = body.email,
        username = body.username,
        password =  hashed_pwd
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

# ===== Login User =====
def login(body:LoginSchema,db:Session): 
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if not user:
        raise HTTPException(401,detail="Unauthorized User")
    
    if not verifyPassword(body.password,user.password):
        raise HTTPException(401,detail="Unauthorized User")

    exp_time = datetime.utcnow() + timedelta(minutes=setting.EXP_TIME)
    payload = {
        "_id":user.id,
        "exp": exp_time
    }

    token = jwt.encode(
        payload,
        setting.SECRET_KEY,
        setting.ALGORITHM
    )

    return {
        "id":user.id,
        "token":token
    }

# ===== Create Post =====
def createPost(
    caption,
    file,
    db:Session,
    user
    ):
    imageUrl = upload_image(file) 
    newPost = PostModel(
        user_id = user.id,
        caption = caption, 
        image = imageUrl 
    )
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return {
        "msg":"Post Uploaded",
        "post":newPost
    }

# === Get Posts ====
def getPosts(db:Session):
    posts = db.query(PostModel).all()
    return posts