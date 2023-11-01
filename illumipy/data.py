#!/usr/bin/env python3

"""
General-purpose solar irradiance and brightness calculator.
"""
import logging
import defaults
from classes import Illumination
import math

dfval() 

def light_data(time=None, date=None, city=None, country=None, api_key=None, cloud_coverage=None):
    """ Main function:
    Creates Illuminance object to calculate Relevant data and
    returns a dictionary object with the following information:
        ['illuminance']: Outside Brightness in Lux
        ['time']: Time used as %-H (e.g. 4 or 12)
        ['date']: Date used as YYYY-MM-DD
        ['city']: City Used
        ['country']: Country Used
        ['cloud_coverage']: Cloud coverage in %
        ['et_illuminance']: Extraterrestrial Illuminance in Lux
        ['direct_illuminance']: Direct Illuminance in Lux
        ['horizontal_illuminance']: Horizontal Illuminance in Lux
        ['horizontal_sky_illuminance']: Horizontal Sky Illuminance in Lux
        ['sunrise']: Time of Sunrise as hh:mm
        ['sunset']: Time of sunset as hh:mm
        ['sun_altitude']: Sund altitude at [Time] in degrees.
        ['day']: True if there is daylight at [Time].
        ['clear_sky_index'] = Aproximation of Clear Sky Index based on cloud coverage
        ['cs_irradiance'] = Estimated Clear Sky Irradiance in W/m^2 based on solar altitude.
        ['irradiance'] = Estimated current Irradiance in W/m^2 based on solar altitude and cloud coverage.
    Takes the following arguments:
        time: str=[0-24], date: str=[YYYY-MM-DD], city: str=['City'],
        country: str=['Country'], api_key: str=['api key']
    If no arguments are provided, defaults to values defined in main.py.
    """
    _time = time
    logging.debug('time is %s', _time)
    _date = date
    logging.debug('date is %s', _date)
    _city = city if city is not None else CITY_DEFAULT
    logging.debug('city is %s', _city)
    _country = country if country is not None else COUNTRY_DEFAULT
    logging.debug('country is %s', _country)
    _api_key = api_key if api_key is not None else API_KEY_DEFAULT
    logging.debug('api_key is %s', _api_key)
    _cloud_coverage = cloud_coverage if cloud_coverage is not None else None
    # illumination = initialiser(requested_hour=12)
    logging.debug('initialising illumination object')
    illumination = Illumination(
        requested_hour=_time,
        requested_day=_date,
        city=_city,
        country=_country,
        api_key=_api_key,
        cloud_coverage=_cloud_coverage)

    illumination_data = {
        'illuminance': illumination.daylight_illuminance,
        'time': illumination.current_time,
        'date': illumination.current_date,
        'city': illumination.city,
        'country': illumination.country,
        'cloud_coverage': illumination.cloud_coverage,
        'et_illuminance': illumination.et_illuminance,
        'direct_illuminance': illumination.direct_illuminance,
        'horizontal_illuminance': illumination.horizontal_illuminance,
        'horizontal_sky_illuminance': illumination.horizontal_sky_illuminance,
        'sunrise': illumination.sunrise,
        'sunset': illumination.sunset,
        'sun_altitude': illumination.altitude,
        'day': illumination.day,
        'clear_sky_index': illumination.clear_sky,
        'cs_irradiance': illumination.irradiance_clear,
        'irradiance': illumination.irradiance_cloud,
        'air_mass': illumination.air_mass,
        'azimuth': illumination.solar_azimuth,
        'declination': math.degrees(illumination.declination_angle_rad),
    }
    illumination_data['LSTM'] = math.degrees(illumination.local_standard_time_meridian_rad)
    illumination_data['EOT'] = illumination.equation_of_time_rad
    return illumination_data
#    return vars(illumination) 

if __name__ == "__main__":
    