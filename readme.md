## Buoyant

Python wrapper for grabbing buoy data from the [National Buoy Data Center](http://www.ndbc.noaa.gov).

This package works by parsing XML from a NBDC endpoint. This isn't fully documented, so there's no guarantee of its stability.

The NBDC provides a [list](http://www.ndbc.noaa.gov/to_station.shtml) and a [map](http://www.ndbc.noaa.gov/obs.shtml) of active buoys.

Hello buoy example:

````python
from buoyant import Buoy

# construct the Buoy object with the station ID
# It's an alphanumeric code. If its numeric, an integer works fine.
station = Buoy(13002)

station.name
# 'Soul'
# Yes, that buoy is really named Soul.
````

More examples:

````python
from buoyant import Buoy

station = Buoy('lndc1')

station.wind_speed
# 9.9

station.units['wind_speed']
# 'kt'

station.lon
# -23.14

station.coords
# (20.43, -23.14)

# Get the time the measurements were made.
station.datetime
# datetime.datetime(2014, 12, 15, 20, 50, tzinfo=<UTC>)

# Not all stations report all data.
station.wave_height
# raises AttributeError

# Fetches new data. This isn't very useful, since the buoys update only every hour or so
station.refresh()

````

### Images

Some buoys have cameras! If the buoy doesn't have an active camera, a placeholder image provided by the NBDC will be returned.

````python
station = Buoy(41009)

station.image_url
# 'http://www.ndbc.noaa.gov/images/buoycam/Z14C_2014_11_01_2200.jpg'

# Save image as a file 'out.jpg'
station.write_image('out.jpg')

# Get raw image as a BytesIO object (see https://docs.python.org/2/library/io.html)
station.image
# <_io.BytesIO object>

station.url
# 'http://www.ndbc.noaa.gov/station_page.php?station=41009'
````

### Measurement metadata

The occassional buoy reports metadata about its measurements. The `Buoy` object has a meta attribute with this data, if any.

````python
# Buoy in the Frying Pan Shoals, NC
frying_pan = Buoy(41013)

frying_pan.pressure
# 30.1

frying_pan.meta['pressure']
# {'tendency': 'steady'}
````

### No data

Sometimes buoys don't have recent data. You'll be able to tell two ways. First, the `Buoy` object won't have many attributes. Second, there will be a message. It will say 'No data'.

````python
station = Buoy('ANRN6')
station.message
# 'No data'
````

### Measurements included

Any measurements reported in the NBDC's XML api are included in a `Buoy` object. [Read about the meaning of the different measurements](http://www.ndbc.noaa.gov/measdes.shtml).

Measurements often included (the text in parentheses is the one used on the NBDC's [measurement descriptions page](http://www.ndbc.noaa.gov/measdes.shtml)):

* air_temp (ATMP)
* average_period (APD)
* dominant_period (DPD)
* mean_wave_direction (Spectral wave direction)
* water_temp (WTMP)
* wave_height (WVHT)
* wind_direction (WDIR)
* wind_gust (GST)
* wind_speed (WSPD)
* datetime
* dewpoint (DEWP)
* lat (latitude)
* lon (longitude)
* pressure (PRES)

Water quality data isn't included in the XML data source. Neither is the elevation of the station or the location of the instruments relative to the station.

### XML

Get the raw XML, if you like XML for some reason. Maybe the package is missing something? If so, submit an issue or pull request!

````python
soul = Buoy('13010')
soul.xml
u'<?xml version="1.0" encoding="UTF-8"?>\n<observation id="13010" name="Soul" lat="-0.01" lon="0.00">\n  <datetime>2014-12-16T02:00:00UTC</datetime>\n  <winddir uom="degT">190</winddir>\n  <windspeed uom="kt">9.9</windspeed>\n  <airtemp uom="F">78.8</airtemp>\n</observation>\n'
````

### Compatibility

Buoyant is compatible with Python 2 and 3.

