from fastapi import APIRouter, Depends

user_routes = APIRouter(prefix="/users")

@user_routes.get("/user")
def meuser():
    return {
        "msg":"I am user"
    }