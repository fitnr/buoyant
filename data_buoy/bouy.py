from lxml import etree
from datetime import datetime
from pytz import timezone
import requests
from io import BytesIO

# example
'''<?xml version="1.0" ?>
<observation id="ROBN4" lat="40.657" lon="-74.065" name="8530973 - Robbins Reef, NJ">
    <datetime>2014-11-01T01:30:00UTC</datetime>
    <winddir uom="degT">50</winddir>
    <windspeed uom="kt">17.1</windspeed>
    <windgust uom="kt">22.0</windgust>
    <pressure uom="in">29.83</pressure>
    <airtemp uom="F">53.6</airtemp>

    <waveht uom="ft">12.8</waveht>
    <domperiod uom="sec">10</domperiod>
    <avgperiod uom="sec">7.1</avgperiod>
    <meanwavedir uom="degT">353</meanwavedir>
</observation>
'''


# both take station as argument
OBS_ENDPOINT = "http://www.ndbc.noaa.gov/get_observation_as_xml.php"
CAM_ENDPOINT = 'http://www.ndbc.noaa.gov/buoycam.php'


def _get(endpoint, bouyid):
    return requests.get(endpoint, params={'station': bouyid}).text


def _parse(xmlstring):
    return etree.fromstring(bytes(xmlstring))


def _setup_ndbc_dt(dt_string):
    '''parse the kind of datetime we're likely to get'''
    d = datetime.strptime(dt_string[:-3], '%Y-%m-%dT%H:%M:%S')
    tz = timezone(dt_string[-3:])

    return tz.localize(d)


class Bouy(dict):

    '''Wrapper for the NDBC Buoy information mini-API'''

    def __init__(self, bouyid):
        super(Bouy, self).__init__()
        self._id = bouyid
        self.refresh()

    def _get_obs(self):
        xml = _get(OBS_ENDPOINT, self.id)
        return _parse(xml)

    def _set_obs(self, xml):
        # Add meta, ignoring id
        meta = dict(xml.items())
        del meta['id']
        self.update(**meta)

        # Add data
        self.update(**dict((y.tag, y.text) for y in xml.getchildren()))

        # Add units
        self['units'] = dict((y.tag, y.items().pop()[1]) for y in xml if len(y.items()))

    def refresh(self):
        xml = self._get_obs()
        self._set_obs(xml)

    @property
    def image_path(self):
        return '{0}?station={id}'.format(CAM_ENDPOINT, id=self._id)

    @property
    def image(self):
        i = requests.get(CAM_ENDPOINT, params={'station': self._id})
        output = BytesIO()

        for chunk in i.iter_content():
            output.write(chunk)

        output.seek(0)

        return output

    @property
    def datetime(self):
        if type(self.datetime) == str:
            self['datetime'] = _setup_ndbc_dt(self.datetime)

        return self.get('datetime')

    @property
    def id(self):
        return self.get('_id')

    @property
    def name(self):
        return self.get('name')

    @property
    def winddirection(self):
        return self.get('winddir')

    @property
    def windspeed(self):
        return self.get('windspeed')

    @property
    def wind_gust(self):
        return self.get('windgust')

    @property
    def pressure(self):
        return self.get('pressure')

    @property
    def airtemp(self):
        return self.get('airtemp')

    @property
    def coords(self):
        return (self.get('lat'), self.get('lon'))

    @property
    def lat(self):
        return self.get('lat')

    @property
    def lon(self):
        return self.get('lon')

    @property
    def waveheight(self):
        return self.get('waveht')

    @property
    def domperiod(self):
        return self.get('domperiod')

    @property
    def avgperiod(self):
        return self.get('avgperiod')

    @property
    def meanwavedir(self):
        return self.get('meanwavedir')
