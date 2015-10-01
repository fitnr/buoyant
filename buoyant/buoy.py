# -*- coding: utf-8 -*-
# Copyright 2014 Neil Freeman
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from xml.dom.minidom import parseString
from datetime import datetime
from pytz import timezone
import requests
from io import BytesIO

# example xml response
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

# Both take station as a GET argument.
OBS_ENDPOINT = "http://www.ndbc.noaa.gov/get_observation_as_xml.php"
CAM_ENDPOINT = 'http://www.ndbc.noaa.gov/buoycam.php'


def _get(endpoint, bouyid):
    return requests.get(endpoint, params={'station': bouyid}).text


def get_text(node):
    while node.nodeType == node.ELEMENT_NODE:
        node = node.childNodes[0]

    if node.nodeType == node.TEXT_NODE:
        return node.data


def get_attrs(elem):
    return ((k, v) for k, v in elem.attributes.items())


def _parse(xmlstring):
    try:
        xml = parseString(bytes(xmlstring))
    except TypeError:
        xml = parseString(bytes(xmlstring, 'utf-8'))

    return xml.getElementsByTagName('observation').item(0)


def _setup_ndbc_dt(dt_string):
    '''parse the kind of datetime we're likely to get'''
    d = datetime.strptime(dt_string[:-3], '%Y-%m-%dT%H:%M:%S')
    tz = timezone(dt_string[-3:])

    return tz.localize(d)


# lat, lon and name are assigned separately.
NAMES = {
    'airtemp': 'air_temp',
    'avgperiod': 'average_period',
    'domperiod': 'dominant_period',
    'meanwavedir': 'mean_wave_direction',
    'msg': 'message',
    'watertemp': 'water_temp',
    'waveht': 'wave_height',
    'winddir': 'wind_direction',
    'windgust': 'wind_gust',
    'windspeed': 'wind_speed',

}

TYPES = {
    'airtemp': float,
    'avgperiod': float,
    'datetime': _setup_ndbc_dt,
    'dewpoint': float,
    'domperiod': float,
    'lat': float,
    'lon': float,
    'pressure': float,
    'watertemp': float,
    'waveht': float,
    'windgust': float,
    'windspeed': float,
}


def _set_obs(cls, xml):
    """Store observation data in the Buoy class."""
    # Add observation meta, ignoring id
    for key, value in get_attrs(xml):
        if key != 'id':
            typ = TYPES.get(key, str)
            classkey = NAMES.get(key, key)
            setattr(cls, classkey, typ(value))

    children = [node for node in xml.childNodes if node.nodeType == node.ELEMENT_NODE]

    # Add data
    for child in children:
        if child.nodeType == child.ELEMENT_NODE:
            classkey = NAMES.get(child.tagName, child.tagName)
            typ = TYPES.get(child.tagName, str)
            setattr(cls, classkey, typ(get_text(child)))

    # Read units from XML attributes and replace names with our kindler, gentler versions
    # And add any other metadata that might be in the attributes
    units, meta = {}, {}
    for node in children:
        attribs = dict(get_attrs(node))
        name = NAMES.get(node.tagName, node.tagName)

        if attribs.get('uom'):
            units[name] = attribs['uom']
            del attribs['uom']

        if len(attribs) > 0:
            meta[name] = attribs

    setattr(cls, 'units', units)
    setattr(cls, 'meta', meta)


class Buoy(object):

    '''Wrapper for the NDBC Buoy information mini-API'''

    _base_url = 'http://www.ndbc.noaa.gov/station_page.php?station={id}'

    lat, lon, xml = None, None, None

    def __init__(self, bouyid):
        self.id = bouyid
        self.refresh()

    def refresh(self):
        self.xml = _get(OBS_ENDPOINT, self.id)
        _set_obs(self, _parse(self.xml))

    @property
    def url(self):
        return self._base_url.format(id=self.id)

    @property
    def image_url(self):
        return '{0}?station={id}'.format(CAM_ENDPOINT, id=self.id)

    def _write_img(self, handle):
        i = requests.get(CAM_ENDPOINT, params={'station': self.id})
        for chunk in i.iter_content():
            handle.write(chunk)

    @property
    def image(self):
        output = BytesIO()
        self._write_img(output)
        output.seek(0)

        return output

    def save_image(self, filename):
        with open(filename, 'wb') as f:
            self._write_img(f)

    @property
    def coords(self):
        return (self.lat, self.lon)
