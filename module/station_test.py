import unittest

from common.test_base import TestBase
from module.station import StationApi


class TestStationApi(TestBase):

    def setUp(self):
        super().setUp()

    def test_get_nearest_stations(self):
        lon = 139.728001
        lat = 35.628832
        distance = 5
        nearest_stations = StationApi.get_nearest_stations(lon, lat, 3, distance)
        self.assertEqual(distance, len(nearest_stations))


if __name__ == '__main__':
    unittest.main()
