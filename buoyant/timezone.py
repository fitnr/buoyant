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
from datetime import datetime

from pytz import timezone

ISOFORMAT = '%Y-%m-%dT%H:%M:%S'


def parse_datetime(timestamp):
    '''Parse an ISO datetime, which Python does buggily.'''
    d = datetime.strptime(timestamp[:-1], ISOFORMAT)

    if timestamp[-1:] == 'Z':
        return timezone('utc').localize(d)

    return d


def iso_format(timestamp):
    return timestamp.strftime(ISOFORMAT + 'Z')
