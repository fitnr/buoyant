# -*- coding: utf-8 -*-
# Copyright 2014-17 Neil Freeman
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
import csv
import re
from io import BytesIO, StringIO
import requests
from pytz import utc
from . import properties, timezone

# Both take station as a GET argument.
OBS_ENDPOINT = "https://sdf.ndbc.noaa.gov/sos/server.php"
CAM_ENDPOINT = 'https://www.ndbc.noaa.gov/buoycam.php'

'''
request=GetObservation
service=SOS
version=1.0.0
offering=urn:ioos:station:wmo:41012
observedproperty=air_pressure_at_sea_level
responseformat=text/csv
eventtime=latest
'''


def parse_unit(prop, dictionary, dt=None):
    '''Do a fuzzy match for `prop` in the dictionary, taking into account unit suffix.'''
    # add the observation's time
    try:
        dt = timezone.parse_datetime(dictionary.get('date_time'))
    except TypeError:
        dt = None

    # 'prop' is a stub of the property's attribute key, so search for matches
    matches = [k for k in dictionary.keys() if prop in k]

    try:
        value = dictionary[matches[0]]
        unit = re.search(r' \(([^)]+)\)', matches[0])

    except IndexError:
        # No matches: fail out
        return None

    # Sometimes we get a list of values (e.g. waves)
    if ';' in value:
        # Ignore empty values
        values = [val for val in value.split(';') if val != '']

        if unit:
            return [Observation(v, unit.group(1), dt) for v in values]
        else:
            return values

    # Sometimes there's no value! Sometimes there's no unit!
    if not value or not unit:
        return value or None

    return Observation(value, unit.group(1), dt)


def _degroup(iterable, propertylist):
    return [{prop: parse_unit(prop, row) for prop in propertylist} for row in iterable]


'''
Response looks like:
station_id,sensor_id,"latitude (degree)","longitude (degree)",date_time,"depth (m)","air_pressure_at_sea_level (hPa)"
urn:ioos:station:wmo:41012,urn:ioos:sensor:wmo:41012::baro1,30.04,-80.55,2014-02-19T12:50:00Z,0.00,1022.1
'''


class Buoy(object):

    '''Wrapper for the NDBC Buoy information mini-API'''

    __dict__ = {}
    params = {
        'request': 'GetObservation',
        'service': 'SOS',
        'version': '1.0.0',
        'responseformat': 'text/csv',
    }

    def __init__(self, bouyid, eventtime=None):
        self.id = bouyid
        self.refresh()

        if eventtime:
            if eventtime.tzinfo:
                eventtime = eventtime.astimezone(utc)
            eventtime = timezone.iso_format(eventtime)
        self.eventtime = eventtime or 'latest'

    def refresh(self):
        self.__dict__ = {
            'lat': None,
            'lon': None,
            'datetime': None,
        }

    def _get(self, observation, as_group=None):
        return self.__dict__.setdefault(observation, self.fetch(observation, as_group))

    def fetch(self, observation, as_group=None):
        params = {
            'offering': 'urn:ioos:station:wmo:{}'.format(self.id),
            'observedproperty': observation,
            'eventtime': self.eventtime
        }
        params.update(self.params)
        request = requests.get(OBS_ENDPOINT, params=params)

        try:
            reader = csv.DictReader(StringIO(request.text))

            if as_group:
                return _degroup(reader, getattr(properties, observation))

            else:
                result = next(reader)

            if 'ows:ExceptionReport' in str(result):
                raise AttributeError(observation)

        except StopIteration:
            raise AttributeError(observation)

        self.__dict__['station_id'] = result.get('station_id')
        self.__dict__['sensor_id'] = result.get('sensor_id')

        try:
            self.__dict__['lon'] = float(result.get('longitude (degree)'))
            self.__dict__['lat'] = float(result.get('latitude (degree)'))

        except TypeError:
            self.__dict__['lon'], self.__dict__['lat'] = None, None

        self.__dict__['depth'] = parse_unit('depth', result)

        return parse_unit(observation, result)

    @property
    def air_pressure_at_sea_level(self):
        return self._get('air_pressure_at_sea_level')

    @property
    def air_temperature(self):
        return self._get('air_temperature')

    @property
    def currents(self):
        try:
            return self._get('currents', as_group=True)
        except IndexError:
            pass

    @property
    def sea_floor_depth_below_sea_surface(self):
        return self._get('sea_floor_depth_below_sea_surface')

    @property
    def sea_water_electrical_conductivity(self):
        return self._get('sea_water_electrical_conductivity')

    @property
    def sea_water_salinity(self):
        return self._get('sea_water_salinity')

    @property
    def sea_water_temperature(self):
        return self._get('sea_water_temperature')

    @property
    def waves(self):
        try:
            return self._get('waves', as_group=True)[0]
        except IndexError:
            pass

    @property
    def winds(self):
        try:
            return self._get('winds', as_group=True)[0]
        except IndexError:
            pass

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
        return self.__dict__.get('lat'), self.__dict__.get('lon')

    @property
    def depth(self):
        return self.__dict__.get('depth')


class Observation(float):

    def __init__(self, value, unit, datetime=None):
        self.value = value
        self._unit = unit
        self._datetime = datetime

    def __new__(cls, value, *args):
        return float.__new__(cls, value)

    @property
    def unit(self):
        return self._unit

    @property
    def datetime(self):
        return self._datetime

    def __repr__(self):
        return "Observation({}, '{}')".format(self.__float__(), self.unit)

    def __str__(self):
        return "{} {}".format(self.__float__(), self.unit)
