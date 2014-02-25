from command.base import BaseCommand
from module.station import *
from module.security import *


class Command(BaseCommand):
    def run(self, *args, **options):
        engine = self.create_engine()
        session = self.get_session()
        database = session.bind.url.database

        engine.execute("drop database {database}".format(database=database))
        engine.execute("create database {database}".format(database=database))

        # 再取得
        engine = self.create_engine()
        Base.metadata.create_all(engine)


if __name__ == '__main__':
    Command().run()
