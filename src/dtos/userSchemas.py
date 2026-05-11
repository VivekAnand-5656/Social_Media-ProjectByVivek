from pydantic import BaseModel, EmailStr
from datetime import datetime
class CreateAccountSchema(BaseModel): 
    fullname : str
    mobile : str
    email : str
    username : str
    password : str

class LoginSchema(BaseModel):
    email: str
    password: str

class PostSchema(BaseModel): 
    caption : str 
    image : str

    class Config:
        from_attributes = True
