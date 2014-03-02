import csv

from command.base import BaseCommand
from common.db_base import engine, session_factory
from module.station import Line, Station


#LINE_CSV_FILE_PATH = './data/station/line20130617free.csv'
#STATION_CSV_FILE_PATH = './data/station/station20130802free.csv'
LINE_CSV_FILE_PATH = './data/station/line20130617free_test.csv'
STATION_CSV_FILE_PATH = './data/station/station20130802free_test.csv'


class Command(BaseCommand):

    def run(self, *args, **options):
        self._import(Line, LINE_CSV_FILE_PATH)
        self._import(Station, STATION_CSV_FILE_PATH)
        self._add_index()

    def _import(self, model_cls, csv_file_path):
        session = session_factory()

        session.query(model_cls).delete()
        headers = {}
        l_num = 0
        csvfile = open(csv_file_path)
        for row in csv.reader(csvfile):
            print(row)
            # 1行目のヘッダを展開
            if l_num == 0:
                for h_i, h_elem in enumerate(row):
                    headers[h_i] = h_elem
            # データ部
            else:
                data = {}
                for i, elem in enumerate(row):
                    if elem:
                        data[headers[i]] = elem

                instance = model_cls(**data)
                session.add(instance)

            l_num += 1
        csvfile.close()

        session.commit()
        session.close()

    def _add_index(self):
        connection = engine.connect()
        connection.execute(
            "UPDATE station AS s SET s.latlon=GeomFromText( CONCAT('POINT(', s.lat, ' ', s.lon, ')' ))")
        connection.execute(
            "ALTER TABLE station MODIFY COLUMN latlon geometry NOT NULL")
        connection.execute(
            "CREATE SPATIAL INDEX sp_latlon_index ON station (latlon)")

        connection.execute(
            "UPDATE line AS s SET s.latlon=GeomFromText( CONCAT('POINT(', s.lat, ' ', s.lon, ')' ))")
        connection.execute(
            "ALTER TABLE line MODIFY COLUMN latlon geometry NOT NULL")
        connection.execute(
            "CREATE SPATIAL INDEX sp_latlon_index ON line (latlon)")
        connection.close()


if __name__ == '__main__':
    Command().run()
