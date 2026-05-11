from fastapi import FastAPI
from src.utills.db import Base, engine
from src.routers.routers import user_routes
from src.routers.publicroutes import router
import src.config.clodinary
app = FastAPI(
    title="Social Media Project"
)
Base.metadata.create_all(bind=engine)
app.include_router(user_routes)
app.include_router(router)