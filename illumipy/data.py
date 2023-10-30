#!/usr/bin/env python3

"""
General-purpose solar irradiance and brightness calculator.
"""
import logging
from illumipy.classes.illumination import Illumination
from illumipy.defaults import API_KEY_DEFAULT, CITY_DEFAULT, COUNTRY_DEFAULT


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
    if city is not None:
        _city = city
    else:
        _city = CITY_DEFAULT
    logging.debug('city is %s', _city)
    if country is not None:
        _country = country
    else:
        _country = COUNTRY_DEFAULT
    logging.debug('country is %s', _country)
    if api_key is not None:
        _api_key = api_key
    else:
        _api_key = API_KEY_DEFAULT
    logging.debug('api_key is %s', _api_key)
    if cloud_coverage is not None:
        _cloud_coverage = cloud_coverage
    else:
        _cloud_coverage=None
    # illumination = initialiser(requested_hour=12)
    logging.debug('initialising illumination object')
    illumination = Illumination(
        requested_hour=_time,
        requested_day=_date,
        city=_city,
        country=_country,
        api_key=_api_key,
        cloud_coverage=_cloud_coverage)

    illumination_data = {}
    illumination_data['illuminance'] = illumination.daylight_illuminance
    illumination_data['time'] = illumination.current_time
    illumination_data['date'] = illumination.current_date
    illumination_data['city'] = illumination.city
    illumination_data['country'] = illumination.country
    illumination_data['cloud_coverage'] = illumination.cloud_coverage
    illumination_data['et_illuminance'] = illumination.et_illuminance
    illumination_data['direct_illuminance'] = illumination.direct_illuminance
    illumination_data[
        'horizontal_illuminance'
        ] = illumination.horizontal_illuminance
    illumination_data[
        'horizontal_sky_illuminance'
        ] = illumination.horizontal_sky_illuminance
    illumination_data['sunrise'] = illumination.sunrise
    illumination_data['sunset'] = illumination.sunset
    illumination_data['sun_altitude'] = illumination.altitude
    illumination_data['day'] = illumination.day
    illumination_data['clear_sky_index'] = illumination.clear_sky
    illumination_data['cs_irradiance'] = illumination.irradiance_clear
    illumination_data['irradiance'] = illumination.irradiance_cloud
    return illumination_data
