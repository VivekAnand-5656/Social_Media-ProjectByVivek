from fastapi import FastAPI
from src.routers.routers import user_routes

app = FastAPI(
    title="Social Media Project"
)

app.include_router(user_routes)

# @app.get("/")
# def home():
#     return {
#         "message":"Hello FastAPI"
#     }

# @app.get("/test")
# def test():
#     return {"status": "API is running successfully"}