from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import CREATE_ENGINE_URL, CREATE_ENGINE_CONF


class BaseCommand:

    def create_engine(self):
        engine = create_engine(CREATE_ENGINE_URL, **CREATE_ENGINE_CONF)
        return engine

    def get_session(self):
        engine = create_engine(CREATE_ENGINE_URL, **CREATE_ENGINE_CONF)
        Session = sessionmaker(bind=engine)
        return Session()
