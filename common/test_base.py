import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.db_base import Base
from settings import CREATE_ENGINE_URL, CREATE_ENGINE_CONF


class TestBase(unittest.TestCase):

    def setUp(self):
        self.create_engine()
        self.create_test_db()

    def create_engine(self):
        self.engine = create_engine(CREATE_ENGINE_URL, **CREATE_ENGINE_CONF)

    def create_test_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()
