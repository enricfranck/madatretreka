from typing import Generator

from backend.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



if settings.USE_SQLITE_DB:
	SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
	engine = create_engine(
		SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
	)
else:
	SQLALCHEMY_DATABASE_URL = "postgresql://qvksmvjzagqgxs:61344e8e24469c20c965090fdd18587227895b9791776fc06ee99d728be7712f@ec2-52-1-17-228.compute-1.amazonaws.com:5432/d9tv0fscv0ohbs"
	engine = create_engine(SQLALCHEMY_DATABASE_URL)



"""

SQLALCHEMY_DATABASE_URL = "postgresql://kgwwnfvmwdgoap:73d243a87b92266266ae49b13316c13e4161486f7398af5f6fdd350dff925b29@ec2-54-174-31-7.compute-1.amazonaws.com:5432/dcdr49146ik4vs"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


"""

# if you don't want to install postgres or any database, use sqlite, a file system based database,
# uncomment below lines if you would like to use sqlite and comment above 2 lines of SQLALCHEMY_DATABASE_URL AND engine

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
