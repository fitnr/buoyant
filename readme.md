## Buoyant

Python wrapper for grabbing buoy data from the [National Buoy Data Center](http://www.ndbc.noaa.gov).

Example:
````python
from buoyant import Buoy

# construct the Buoy object with the station ID
station = Buoy(13002)

station.wind_speed
# 15.9

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
````

### Images

Some buoys have cameras!

````python
station = Buoy(41009)
station.image_url
# http://www.ndbc.noaa.gov/images/buoycam/Z14C_2014_11_01_2200.jpg

station.image
# <_io.BytesIO object>
# a BytesIO object (see https://docs.python.org/2/library/io.html)
with open('station.jpg', 'wb') as f:
    f.write(station.image.read())

station.url
# http://www.ndbc.noaa.gov/station_page.php?station=13002
````

### Measurement metadata

The occassional buoy reports metadata about its measurements. The `Buoy` object has a meta attribute with this data, if any.
````python
# Buoy in the Frying Pan Shoals, NC
frying_pan = Buoy(41013)

frying_pan.pressure
30.1

frying_pan.meta['pressure']
{'tendency': 'steady'}
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

### Compatibility

Buoyant is compatible with Python 2 and 3.

