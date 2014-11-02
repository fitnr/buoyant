## Buoyant

Python wrapper for grabbing buoy data from the [National Buoy Sata Center](http://www.ndbc.noaa.gov).

Example:
````python

from buoyant import Buoy

# construct the Buoy object with the station ID
station = Buoy(13002)

station.windspeed
# 15.9

station.units['windspeed']
# 'kt'

station.lon
# -23.14

station.coords
# (20.43, -23.14)

station.waveheight
# None
# Not all station report all data

# some buoys have cameras
station = Buoy(41009)

station.image_url
# http://www.ndbc.noaa.gov/images/buoycam/Z14C_2014_11_01_2200.jpg

station.image
# <_io.BytesIO object>
# a [BytesIO object](https://docs.python.org/2/library/io.html)

station.url
# http://www.ndbc.noaa.gov/station_page.php?station=13002
````
