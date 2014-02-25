import csv

from command.base import BaseCommand
from module.station import Line, Station


LINE_CSV_FILE_PATH = './data/station/line20130617free.csv'
STATION_CSV_FILE_PATH = './data/station/station20130802free.csv'


class Command(BaseCommand):

    def run(self, *args, **options):
        self._import(Line, LINE_CSV_FILE_PATH)
        self._import(Station, STATION_CSV_FILE_PATH)
        self._add_index()

    def _import(self, model_cls, csv_file_path):
        session = self.get_session()
        session.query(model_cls).delete()
        headers = {}
        l_num = 0
        for row in csv.reader(open(csv_file_path)):
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

        session.commit()

    def _add_index(self):
        engine = self.get_session()
        engine.execute(
            "UPDATE station AS s SET s.latlon=GeomFromText( CONCAT('POINT(', s.lat, ' ', s.lon, ')' ))")
        engine.execute(
            "ALTER TABLE station MODIFY COLUMN latlon geometry NOT NULL")
        engine.execute(
            "CREATE SPATIAL INDEX sp_latlon_index ON station (latlon)")

        engine.execute(
            "UPDATE line AS s SET s.latlon=GeomFromText( CONCAT('POINT(', s.lat, ' ', s.lon, ')' ))")
        engine.execute(
            "ALTER TABLE line MODIFY COLUMN latlon geometry NOT NULL")
        engine.execute(
            "CREATE SPATIAL INDEX sp_latlon_index ON line (latlon)")


if __name__ == '__main__':
    Command().run()
