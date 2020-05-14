import datetime
import unittest
from io import BytesIO
import buoyant
from buoyant import buoy

sampledata = [{
    'latitude (degree)': '39.235',
    'sea_surface_wave_peak_period (s)': '13.79',
    'polar_coordinate_r1 (1)': ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;',
    'station_id': 'urn:ioos:station:wmo:46014',
    'sea_surface_wind_wave_period (s)': '3.80',
    'spectral_energy (m**2/Hz)': '0;0;0;0;0.117495;0.347233;0.340078;1.07545;1.31407;0.644604;0.319928;0.20951;0.203445;0.407703;0.501098;1.05528;0.552653;0.982512;0.40238;0.259344;0.176087;0.156276;0.10127;0.0713481;0.1257;0.0469963;0.0294347;0.0344079;0.0196117;0.0208386;0.0207157;0.0185725;0.0112313;0.0140935;0.00829521;0.0135329;0.0103501;0.00823833;0.00611987;0.00516951;0.00295949;0.00274196;0.00162249;0.00153895;0.000701703;0.000452887',
    'sea_surface_wave_mean_period (s)': '7.61',
    'sea_water_temperature (c)': '',
    'bandwidths (Hz)': '0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0050;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0100;0.0200;0.0200;0.0200;0.0200;0.0200;0.0200;0.0200',
    'sea_surface_wind_wave_to_direction (degree)': '',
    'polar_coordinate_r2 (1)': ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;',
    'sampling_rate (Hz)': '',
    'sea_surface_wave_to_direction (degree)': '',
    'sea_surface_swell_wave_significant_height (m)': '1.07',
    'number_of_frequencies (count)': '46',
    'center_frequencies (Hz)': '0.0325;0.0375;0.0425;0.0475;0.0525;0.0575;0.0625;0.0675;0.0725;0.0775;0.0825;0.0875;0.0925;0.1000;0.1100;0.1200;0.1300;0.1400;0.1500;0.1600;0.1700;0.1800;0.1900;0.2000;0.2100;0.2200;0.2300;0.2400;0.2500;0.2600;0.2700;0.2800;0.2900;0.3000;0.3100;0.3200;0.3300;0.3400;0.3500;0.3650;0.3850;0.4050;0.4250;0.4450;0.4650;0.4850',
    'date_time': '2015-07-31T19:50:00Z',
    'sea_surface_wind_wave_significant_height (m)': '0.17',
    'sea_surface_wave_significant_height (m)': '1.09',
    'sea_surface_swell_wave_to_direction (degree)': '',
    'sea_surface_swell_wave_period (s)': '',
    'calculation_method': 'UNKNOWN',
    'mean_wave_direction (degree)': ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;',
    'longitude (degree)': '-123.974',
    'principal_wave_direction (degree)': ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;',
    'sensor_id': 'urn:ioos:sensor:wmo:46014::wpm1'
}]


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
        assert isinstance(x.datetime, datetime.datetime)
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
        dictionary = {'magic (pixie dust)': '42'}
        x = buoy.parse_unit('magic', dictionary)
        assert isinstance(x, buoyant.Observation)

        nope = buoy.parse_unit('widget', dictionary)
        self.assertIsNone(nope)

        spectral_energy = buoy.parse_unit('spectral_energy', sampledata[0])
        self.assertEqual(spectral_energy[4], buoy.Observation(0.117495, 'm**2/Hz'))

    def test_error(self):
        with self.assertRaises(AttributeError):
            self.b._get('foo bar')

        self.assertIsNone(self.b.depth)

    def test_image(self):
        station = buoyant.Buoy(51001)
        assert buoy.CAM_ENDPOINT in station.image_url
        self.assertIsNotNone(station.image)

    def test_degroup(self):
        waves = buoyant.buoy._degroup(sampledata, buoyant.properties.waves)
        self.assertEqual(waves[0]['sea_surface_wind_wave_significant_height'], buoy.Observation(0.17, 'm'))


if __name__ == '__main__':
    unittest.main()
