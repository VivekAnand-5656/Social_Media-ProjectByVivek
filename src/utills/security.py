from fastapi import HTTPException, Depends
from src.utills.setting import setting
from sqlalchemy.orm import Session
from jose import jwt 
from jose.exceptions import ExpiredSignatureError, JWTError
from src.models.users import UserModel
from src.utills.db import getDb
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def isLogin(
        credentials: HTTPAuthorizationCredentials=Depends(security),
        db:Session =Depends(getDb)):
    try:
        token = credentials.credentials
        data = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM,)
        user_id = data.get("_id")
        if user_id is None:
            raise HTTPException(401, detail="Please Login")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not user:
            raise HTTPException(401, detail="Please Login")
        print(data)
        return user
    except ExpiredSignatureError:
        raise HTTPException(401, detail="Token Expired")
    except JWTError:
        raise HTTPException(401,detail="Invalid Token")