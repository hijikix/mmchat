import unittest

from common.db_base import Session


class TestBase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        # ローカルセションを閉じる
        self.remove_session()

    def remove_session(self):
        Session.commit()
        Session.remove()
