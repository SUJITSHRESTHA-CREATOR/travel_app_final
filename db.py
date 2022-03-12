import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings



SQLALCHEMY_DATABASE_URL = f'mysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



async def add_models_to_database() -> None:
    from models import User, TrekDestination, Itenary, Comment, Vote

    User.Base.metadata.create_all(bind=engine)
    TrekDestination.Base.metadata.create_all(bind=engine)
    Itenary.Base.metadata.create_all(bind=engine)
    Comment.Base.metadata.create_all(bind=engine)
    Vote.Base.metadata.create_all(bind=engine)



def get_db():
    dbase = SessionLocal()
    try:
        yield dbase
    finally:
        dbase.close()
