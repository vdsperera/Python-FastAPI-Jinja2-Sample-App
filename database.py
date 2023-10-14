from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

""" 
url format: dialect+driver://username:password@host:port/database
more info: https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
"""
SQLALCHMY_DATABASE_URL = "sqlite:///:db.sqlite"

engine = create_engine(SQLALCHMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()