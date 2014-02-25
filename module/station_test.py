import unittest

from common.test_base import TestBase
from module.station import StationApi


class TestStationApi(TestBase):

    def setUp(self):
        super().setUp()

    def test_get_nearest_stations(self):
        lon = None
        lat = None
        nearest_stations = StationApi.get_nearest_stations(lon, lat)


if __name__ == '__main__':
    unittest.main()
