
from module.station import *
from module.security import *
from command.base import BaseCommand
from common.db_base import Base, engine, session_factory


class Command(BaseCommand):

    def run(self, *args, **options):

        # DB名取得
        session = session_factory()
        database = session.bind.url.database
        session.close()

        # DB再作成
        connection = engine.connect()
        connection.execute(
            "drop database {database}".format(database=database))
        connection.execute(
            "create database {database}".format(database=database))

        # テーブル作成
        Base.metadata.create_all(engine)
        connection.close()


if __name__ == '__main__':
    Command().run()
