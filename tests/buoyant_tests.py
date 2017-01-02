import datetime
import unittest
from io import BytesIO
import buoyant
from buoyant import buoy


class BuoyTestCase(unittest.TestCase):

    def setUp(self):
        self.b = buoyant.Buoy('41012')

    def test_observation(self):
        self.assertTrue(issubclass(buoyant.Observation, float))
        subint = float.__new__(buoyant.Observation, 11)
        assert subint == 11
        assert isinstance(subint, buoyant.Observation)
        obs = buoyant.Observation(1, 'm')
        assert isinstance(obs, buoyant.Observation)
        assert obs.unit == 'm'
        self.assertEqual(str(obs), '1.0 m')
        assert repr(obs) == "Observation(1.0, 'm')"
        assert obs + 2 == 3

    def test_buoy_instant(self):
        assert self.b
        assert isinstance(self.b, buoyant.Buoy)

    def test_data_exists(self):
        x = self.b.sea_water_electrical_conductivity
        assert x.unit == 'mS/cm'
        currents = self.b.currents
        self.assertIsInstance(currents, list)
        assert isinstance(self.b.datetime, datetime.datetime)
        assert isinstance(self.b.image, BytesIO)
        assert isinstance(self.b.__dict__['lat'], float)
        assert isinstance(self.b.coords, tuple)
        assert (self.b.__dict__['lat'], self.b.__dict__['lon']) == self.b.coords

    def test_keys(self):
        self.assertIsNotNone(self.b.sea_water_salinity)
        self.assertIsNotNone(self.b.air_pressure_at_sea_level)
        self.assertIsNotNone(self.b.air_temperature)
        self.assertIsNotNone(self.b.currents)
        self.assertIsNotNone(self.b.sea_water_electrical_conductivity)
        self.assertIsNotNone(self.b.sea_water_salinity)
        self.assertIsNotNone(self.b.sea_water_temperature)

    def test_parse_unit(self):
        dictionary = {'magic (pixie dust)': 42}
        x = buoy.parse_unit('magic', dictionary)
        assert isinstance(x, buoyant.Observation)

        nope = buoy.parse_unit('widget', dictionary)
        self.assertIsNone(nope)

    def test_error(self):
        with self.assertRaises(AttributeError):
            self.b._get('foo bar')

        self.assertIsNone(self.b.depth)

    def test_image(self):
        station = buoyant.Buoy(51001)
        assert buoy.CAM_ENDPOINT in station.image_url
        self.assertIsNotNone(station.image)

if __name__ == '__main__':
    unittest.main()
