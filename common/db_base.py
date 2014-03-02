from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from settings import CREATE_ENGINE_URL, CREATE_ENGINE_CONF


Base = declarative_base()

engine = create_engine(CREATE_ENGINE_URL, **CREATE_ENGINE_CONF)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
