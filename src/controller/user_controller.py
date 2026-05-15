from jose import jwt
from datetime import datetime, timedelta
from src.utills.setting import setting
from pwdlib import PasswordHash
from src.dtos.userSchemas import LoginSchema, CreateAccountSchema, PostSchema, CommentSchema
from src.models.users import UserModel, PostModel, LikeModel, CommentModel, FollowModel
from src.config.service import upload_image
from sqlalchemy.orm import Session
from fastapi import HTTPException 
from sqlalchemy import or_
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
 
# ==== User Get My Posts ====
def getMyPost(db:Session,user):
    posts = db.query(PostModel).filter(PostModel.user_id == user.id).all()
    return posts

# === Delete Post ====
def deletePost(postid:int,db:Session,user):
    post = db.query(PostModel).filter(PostModel.id == postid).first()

    if not post:
        raise HTTPException(404, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(403, detail="You are not allowed to delete this post")
    
    db.delete(post)
    db.commit() 

    return {
        "msg":"Post Deleted Successfully"
    }

# ==== Like Posts =====
def likePosts(postid:int,db:Session,user):
    post = db.query(PostModel).filter(PostModel.id == postid).first()
    if not post:
        raise HTTPException(404, detail="Post not found")

    alreadyLike = db.query(LikeModel).filter(
        LikeModel.user_id == user.id,
        LikeModel.post_id == post.id
    ).first()
    if alreadyLike:
        db.delete(alreadyLike)
        post.likeCount -= 1
        db.commit()
        return {
            "msg":"Unliked this post"
        }
    else:
        newlike = LikeModel(
            user_id = user.id,
            post_id = post.id
            ) 
        db.add(newlike)
        post.likeCount += 1
        db.commit()
    
     
    return {
        "msg" : "Liked this post"
    }

# ==== Comment ====
def comment(postid:int,body:CommentSchema,db:Session,user):
    post = db.query(PostModel).filter(PostModel.id == postid).first()

    if not post:
        raise HTTPException(404, detail="Post not found")
    
    newComment = CommentModel(
        user_id = user.id,
        post_id = post.id,
        commentStr = body.commentstr
    )

    db.add(newComment)
    post.commentcount += 1
    post.comment = newComment.commentStr
    db.commit()
    db.refresh(newComment)

    return {
        "msg":"Commented on this post",
        "comment": newComment
    }
# ===== Get Posts Comments ====
def getPostsComments(postid:int,db:Session):
    allComments = db.query(CommentModel).filter(CommentModel.post_id == postid).all()
    if not allComments:
        raise HTTPException(404, detail="No Comments")
    return allComments 

# ================ Search User ==============
def searchUser(username:str,db:Session):
    users = db.query(UserModel).filter(or_(UserModel.username.ilike(f"%{username}%"), UserModel.fullname.ilike(f"%{username}%"))).all()
    if not users:
        raise HTTPException(404,detail="Users not found")
    return users

# ===== Follow =====
def followUser(userid:int ,db:Session,user):
    follower = db.query(FollowModel).filter(FollowModel.followerId == user.id,FollowModel.followingId == userid).first()

    if follower:
        raise HTTPException(409,detail="You already followed")
    
    if userid == user.id:
        raise HTTPException(400, detail="You cannot follow yourself")
    
    
    newFollower = FollowModel(
        followerId = user.id, 
        followingId = userid
    )
    db.add(newFollower)
    tarUser = db.query(UserModel).filter(UserModel.id == userid).first()
    curentUser = db.query(UserModel).filter(UserModel.id == user.id).first()

    tarUser.followercount += 1
    curentUser.followingcount += 1
    db.commit() 

    return {
        "msg":"Follow Successfully"
    }

# ===== UnFollow user =====
def unFollow(userid: int, db: Session, user):

    follow = db.query(FollowModel).filter(
        FollowModel.followerId == user.id,
        FollowModel.followingId == userid
    ).first()

    if not follow:
        raise HTTPException(404, "You are not following this user")

    db.delete(follow)

    
    targetUser = db.query(UserModel).filter(UserModel.id == userid).first()
    currentUser = db.query(UserModel).filter(UserModel.id == user.id).first()

    if targetUser.followercount > 0:
        targetUser.followercount -= 1
    if currentUser.followingcount > 0: 
        currentUser.followingcount -= 1
     

    db.commit()

    return {"msg": "Unfollow Successfully"}