from datetime import datetime
from pytz import timezone

ISOFORMAT = '%Y-%m-%dT%H:%M:%S'


def parse_datetime(dt):
    '''Parse an ISO datetime, which Python does buggily.'''
    d = datetime.strptime(dt[:-1], ISOFORMAT)

    if dt[-1:] == 'Z':
        return timezone('utc').localize(d)
    else:
        return d


def iso_format(dt):
    return dt.strftime(ISOFORMAT + 'Z')
