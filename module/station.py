from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, func
from sqlalchemy.types import UserDefinedType

from common.db_base import Base


class Geometry(UserDefinedType):

    def get_col_spec(self):
        return "GEOMETRY"

    def bind_expression(self, bindvalue):
        return func.GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)


class Line(Base):
    __tablename__ = 'line'
    __table_args__ = {"mysql_engine": "MyISAM"}

    line_cd = Column(Integer(), primary_key=True)
    company_cd = Column(Integer(), nullable=False)

    line_name = Column(String(80), nullable=False)
    line_name_k = Column(String(80), nullable=False)
    line_name_h = Column(String(80), nullable=False)

    line_color_c = Column(String(6))
    line_color_t = Column(String(10))
    line_type = Column(Integer())

    lon = Column(DECIMAL(20, 17), nullable=False)
    lat = Column(DECIMAL(20, 17), nullable=False)
    # 後でNOT NULLとインデックスを貼る
    latlon = Column(Geometry())

    zoom = Column(Integer(), nullable=False)

    e_status = Column(Integer(), nullable=False)
    e_sort = Column(Integer(), nullable=False)


class Station(Base):
    __tablename__ = 'station'
    __table_args__ = {"mysql_engine": "MyISAM"}

    station_cd = Column(Integer(), primary_key=True)
    station_g_cd = Column(Integer(), nullable=False)

    station_name = Column(String(80), nullable=False)
    station_name_k = Column(String(80))
    station_name_r = Column(String(200))

    line_cd = Column(Integer(), nullable=False)
    pref_cd = Column(Integer(), nullable=False)

    post = Column(String(10))
    add = Column(String(300))

    lon = Column(DECIMAL(20, 17), nullable=False)
    lat = Column(DECIMAL(20, 17), nullable=False)
    # 後でNOT NULLとインデックスを貼る
    latlon = Column(Geometry())

    open_ymd = Column(DateTime)
    close_ymd = Column(DateTime)

    e_status = Column(Integer(), nullable=False)
    e_sort = Column(Integer(), nullable=False)


class StationApi:

    @classmethod
    def get_nearest_stations(cls, lon, lat, range, limit, session):
        """
        指定座標の最寄り駅を取得
        """
        sql = """
SELECT station_cd, station_name FROM station
WHERE MBRContains(
  GeomFromText(
    Concat('LineString(',
      {lat} + {range} , ' ',
      {lon} + {range} , ',',
      {lat} - {range} , ' ',
      {lon} - {range} , ')'
    )
  ),
  latlon
)
ORDER BY GLength(
  GeomFromText(
    CONCAT(
       'LineString({lat} {lon},',
       X( `latlon` ) , ' ',
       Y( `latlon` ) , ')'
    )
  )
) LIMIT {limit};
""".format(lon=lon, lat=lat, range=range, limit=limit)
        return session.query(Station.station_cd, Station.station_name).from_statement(sql).all()

