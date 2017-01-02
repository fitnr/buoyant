## Buoyant

Buoyant is a Python wrapper for grabbing buoy data from the [National Buoy Data Center](http://www.ndbc.noaa.gov). It parses CSV from the [SDF](http://sdf.ndbc.noaa.gov) endpoint and images from the [BuoyCam](http://www.ndbc.noaa.gov/buoycams.shtml) service.

The NBDC provides a [list](http://sdf.ndbc.noaa.gov/stations.shtml) and a [map](http://sdf.ndbc.noaa.gov) of active buoys.

Hello buoy example:

````python
from buoyant import Buoy

# construct the Buoy object with the station ID
# It's an alphanumeric code. If its numeric, an integer works fine.
buoy = Buoy(13010)
````

More examples:

````python
from buoyant import Buoy

sturgeon_buoy = Buoy('0Y2W3')

sturgeon_buoy.air_pressure_at_sea_level
# Observation(18.9, 'C')
```

The `Observation` object is numeric value (a `float`) with an additional attribute, `unit`. Generally this is an abbreviation for a metric unit or composition of units.

```
sturgeon_buoy.coords
# (44.794, -87.313)

# Get the time the measurements were made. This can be some time ago!
sturgeon_buoy.datetime
# datetime.datetime(2015, 8, 18, 11, 40, tzinfo=<UTC>)

# Not all stations report all data.
sturgeon_buoy.wave_height
# raises AttributeError

# Clears the buoy object's data dictionary. This isn't very useful, since the buoys update only every hour or so
sturgeon_buoy.refresh()
````

### Images

Some buoys have cameras! If the buoy doesn't have an active camera, a placeholder image provided by the NBDC will be returned.

````python
station = Buoy(41009)

station.image_url
# 'http://www.ndbc.noaa.gov/images/buoycam/Z14C_2014_11_01_2200.jpg'

# Save image as a file 'out.jpg'
station.write_image('out.jpg')

# Get raw image as a `BytesIO` object
station.image
# <_io.BytesIO object>

station.url
# 'http://www.ndbc.noaa.gov/station_page.php?station=41009'
````

### No data

There are two ways to a buoy can be missing a certain data field. Either there's no recent observation, or that buoy doesn't observe that datum.

````python
sturgeon = Buoy('0Y2W3')

sturgeon.winds
# None, because while this is usually recorded, it hasn't been.

sturgeon.waves
# raises AttributeError
````

### Measurements included

* air_pressure_at_sea_level
* air_temperature
* currents
* sea_floor_depth_below_sea_surface
* sea_water_electrical_conductivity
* sea_water_salinity
* sea_water_temperature
* waves
* winds

### Currents

Currents data is a `list` of `dict`s with current information at different depths. It's not well-documented on the NBDC site, so good luck!

### Compatibility

Buoyant is compatible with Python 2 and 3.

### License

Buoyant is licensed under the [GPL](http://www.gnu.org/licenses/#GPL).
