import unittest

from common.test_base import TestBase
from module.station import StationApi


class TestStationApi(TestBase):

    def setUp(self):
        super().setUp()

    def test_get_nearest_stations(self):
        session = self.get_session()
        lon = 139.728001
        lat = 35.628832
        nearest_stations = StationApi.get_nearest_stations(lon, lat, 5, 1, session)
        print(nearest_stations)


if __name__ == '__main__':
    unittest.main()
