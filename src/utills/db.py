from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utills.setting import setting
from dotenv import load_dotenv

Base = declarative_base()

engine = create_engine(
    setting.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

# def create_tables():
#     Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

LocalSession = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

def getDb():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
