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

# lat, lon, datetime are assigned separately.
general = [
    'air_pressure_at_sea_level',
    'air_temperature',
    'currents',
    'sea_floor_depth_below_sea_surface',
    'sea_water_electrical_conductivity',
    'sea_water_salinity',
    'sea_water_temperature',
    'waves',
    'winds',
]

currents = [
    'bin',  # (count)
    'depth',  # (m)
    'direction_of_sea_water_velocity',  # (degree)
    'sea_water_speed',  # (c/s)
    'upward_sea_water_velocity',  # (c/s)
    'error_velocity',  # (c/s)
    'platform_orientation',  # (degree)
    'platform_pitch_angle',  # (degree)
    'platform_roll_angle',  # (degree)
    'sea_water_temperature',  # (C)
    'pct_good_3_beam',  # (%)
    'pct_good_4_beam',  # (%)
    'pct_rejected',  # (%)
    'pct_bad',  # (%)
    'echo_intensity_beam1',  # (count)
    'echo_intensity_beam2',  # (count)
    'echo_intensity_beam3',  # (count)
    'echo_intensity_beam4',  # (count)
    'correlation_magnitude_beam1',  # (count)
    'correlation_magnitude_beam2',  # (count)
    'correlation_magnitude_beam3',  # (count)
    'correlation_magnitude_beam4',  # (count)
    'quality_flags',
]

waves = [
    "sea_surface_wave_significant_height",  # (m)
    "sea_surface_wave_peak_period",  # (s)
    "sea_surface_wave_mean_period",  # (s)
    "sea_surface_swell_wave_significant_height",  # (m)
    "sea_surface_swell_wave_period",  # (s)
    "sea_surface_wind_wave_significant_height",  # (m)
    "sea_surface_wind_wave_period",  # (s)
    "sea_water_temperature",  # (c)
    "sea_surface_wave_to_direction",  # (degree)
    "sea_surface_swell_wave_to_direction",  # (degree)
    "sea_surface_wind_wave_to_direction",  # (degree)
    "number_of_frequencies",  # (count)
    "center_frequencies",  # (Hz)
    "bandwidths",  # (Hz)
    "spectral_energy",  # (m**2/Hz)
    "mean_wave_direction",  # (degree)
    "principal_wave_direction",  # (degree)
    "polar_coordinate_r1",  # (1)
    "polar_coordinate_r2",  # (1)
    "calculation_method",
    "sampling_rate",  # (Hz)
]

winds = [
    "wind_from_direction",  # (degree)
    "wind_speed",  # (m/s)
    "wind_speed_of_gust",  # (m/s)
    "upward_air_velocity",  # (m/s)
]
