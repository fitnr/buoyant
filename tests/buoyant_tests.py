import buoyant
import unittest
import datetime
from io import BytesIO

class BuoyTestCase(unittest.TestCase):

    def setUp(self):
        self.b = buoyant.Buoy('ROBN4')

    def test_buoy_instant(self):
        assert self.b
        assert type(self.b) == buoyant.Buoy

    def test_data_exists(self):
        assert type(self.b.xml) == unicode
        assert type(self.b.datetime) == datetime.datetime
        assert type(self.b.image) == BytesIO

        assert type(self.b.lat) == float
        assert type(self.b.coords) == tuple
        assert (self.b.lat, self.b.lon) == self.b.coords

        assert type(self.b.meta) == dict

        assert hasattr(self.b.refresh, '__call__')

if __name__ == '__main__':
    unittest.main()
