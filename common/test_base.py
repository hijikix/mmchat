import unittest

from common.db_base import Session

#from command.recreate_db import Command as RecreateDbCommand
#from command.load_station_master import Command as LoadStationMasterCommand


class TestBase(unittest.TestCase):

    def setUp(self):
        #RecreateDbCommand().run()
        #LoadStationMasterCommand().run()
        pass

    def tearDown(self):
        # ローカルセションを閉じる
        self.remove_session()

    def remove_session(self):
        Session.commit()
        Session.remove()
