#!/usr/bin/env python3
"""
Classes for Getting and Calculating Data.
General-purpose solar irradiance and brightness calculator.
"""
import logging
from datetime import datetime, timedelta
import requests
from requests.exceptions import HTTPError


class Basedata:
    """
    BaseData class: Collects the relevant Data neccessary
    to calculate Illumination and Irradiance.
    """
    def __init__(self,
                 name=None,
                 api_key=None,
                 api_base=None,
                 api_loc=None,
                 city=None,
                 country=None,
                 requested_day=None,
                 requested_hour=None
                 ):
        logging.info("Initializing BaseData class.")
        if name is None:
            name = "basedata"
        self.name = name
        if api_key is None:
            self.api_key = None
        elif isinstance(api_key, str):
            self.api_key = api_key
        if api_base is None:
            self.api_base: str = 'https://api.openweathermap.org/'
        elif isinstance(api_base, str): 
            self.api_base = api_base
        if city is None:
            self.city = None
        elif isinstance(city, str):
            self.city = city
        if country is None:
            self.country = None
        elif isinstance(country, str):
            self.country = country
        if api_loc is None:
            self.api_loc: str = 'geo/1.0/direct?'
        elif isinstance(api_loc, str):
            self.api_loc = api_loc
        if requested_day is not None:
            self.requested_day = requested_day
        else:
            self._requested_day = None
        if requested_hour is not None:
            self.requested_hour = requested_hour
        else:
            self._requested_hour = None
     
     
    @property
    def sunrise_datetime(self):
        return self._sunrise_datetime
    
    @sunrise_datetime.setter
    def sunrise_datetime(self, value):
        logging.debug(f'set _sunrise_datetime to {value}')
        self._sunrise_datetime = value
    
    @property
    def sunset_datetime(self):
        return self._sunset_datetime
    
    @sunset_datetime.setter
    def sunset_datetime(self, value):
        logging.debug(f'set _sunset_datetime to {value}')
        self._sunset_datetime = value
    
    @property
    def api_key(self):
        return self._api_key
    
    @api_key.setter
    def api_key(self, value):
        logging.info(f"Setting api_key: {value}")
        self._api_key = str(value)
        
    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, value):
        logging.info(f"Setting city: {value}")
        self._city = str(value)
    
    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value):
        logging.info(f"Setting country: {value}")
        self._country = str(value)
    
    @property
    def requested_day(self):
        return self._requested_day
    
    @requested_day.setter
    def requested_day(self, value):
        logging.info(f"Setting requested_day: {value}")
        self._requested_day = str(value)

    @property
    def requested_hour(self):
        return self._requested_hour
    
    @requested_hour.setter
    def requested_hour(self, value):
        logging.info(f"Setting requested_hour: {value}")
        self._requested_hour = str(value)

    @property
    def current_date(self):
        """
        Returns current date as string (YYY-MM-DD),
        If a custom value is provided (self.requested_day)
        it will be returned instead.
        """
        if self.requested_day is not None and isinstance(self.requested_day, str):
            _current_date = self.requested_day
            logging.debug(f"{self.requested_day} is a valid date")
        else:
            logging.debug(f"{self.requested_day} is a not valid date")
            now = datetime.now()
            _current_date = now.strftime("%Y-%m-%d")
        logging.info(f"set current date to {_current_date}")
        return _current_date

    @property
    def day_of_the_year(self):
        """
        @brief Returns the day of the year. It is defined as the number of days since January 1 1970 00 : 00 : 00.
        @return a tuple of the form ( year month day )
        """
        _date_object = datetime.strptime(self.current_date, "%Y-%m-%d")
        _day_of_the_year = _date_object.timetuple().tm_yday
        logging.info(f"calculated day of the year: {_day_of_the_year}")
        return _day_of_the_year

    @property
    def current_time(self):
        """
        Returns current hour of day as string (e.g. 12),
        If a custom value is provided (self.requested_hour)
        it will be returned instead.
        """
        #print("current_time accessed")
        if self.requested_hour is not None and isinstance(self.requested_hour, str):
            _current_time = self.requested_hour
            logging.debug(f"{self.requested_hour} is a valid hour")
        else:
            now = datetime.now()
            logging.debug(f"{self.requested_hour} is a not valid hour")
            logging.debug(f'setting current_time to actual time')
            _current_time = now.strftime("%-H")
        logging.info(f"set current time to {_current_time}")
        return _current_time

    @property
    def latitude(self):
        """
        Calls OpenWeatherMap API to get latitude of the city and
        returns it as "latitude".
        """
        logging.debug('getting latitude')
        _parameters = {
            "q": f"{self.city},{self.country}",
            "limit": 1
        }
        logging.debug(f"parameters: {_parameters}")
        _api_suburl = self.api_loc
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw
        _latitude = _api_response[0]['lat']
        logging.info(f"latitude: {_latitude}")
        return float(_latitude)

    @property
    def longitude(self):
        """
        Calls OpenWeatherMap API to get longitude of the city and
        returns it as "longitude".
        """
        logging.debug('getting longitude')
        _parameters = {
            "q": f"{self.city},{self.country}",
            "limit": 1
        }
        logging.debug(f"parameters: {_parameters}")
        _api_suburl = str(self.api_loc)
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw.json()
        _longitude = _api_response[0]['lon']
        logging.info(f"longitude: {_longitude}")
        return float(_longitude)

    def requester(self, _api_suburl: str, parameters: dict):
        """
        Returns the response of the API request.
        Takes the specific sub-url and parameters as input.
        """
        logging.debug('using requester')
        _api_url: str = f"{self.api_base}{_api_suburl}"
        parameters["appid"] = self.api_key
        _parameters = parameters
        logging.debug(f"parameters: {_parameters}")
        try:
            _response = requests.get(_api_url, params=_parameters, timeout=10)
            _response.raise_for_status()
            # _response = _response_raw.json()
            logging.debug(f"response: {_response.json()}")
            return _response.json()
        except HTTPError as err:
            raise SystemExit(err) from err
       
    @property
    def tester(self):
        """
        test function.
        """
        _parameters = {
            "q": f"{self.city},{self.country}",
            "limit": 1
            }
        _api_suburl = self.api_loc
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw
        testdata = (_api_response)[0]['name']
        return testdata


class Weather(Basedata):
    """
    Weather class:
    Using the OpenWeatherMap API, get current weather
    infomation for given time and location.
    """
    def __init__(self,
                 name=None,
                 api_key=None,
                 api_base=None,
                 api_loc=None,
                 api_weather=None,
                 city=None,
                 country=None,
                 ):
        if name is None:
            name = "weather"
        self.name = name
        super().__init__(self)
        # self.api_key = api_key
        # self.api_base = api_base
        # self.city = city
        # self.country = country
        # self.api_loc = api_loc
           
        if api_weather is None:
            self.api_weather: str = '/data/2.5/weather?'
        elif isinstance(api_weather, str):
            self.api_weather = api_weather
        self.sunrise_unix = None
        self.sunset_unix = None
        self._cloud_coverage = None
        self._sunrise = None
        self._sunset = None
        self._sunrise_datetime = None
        self._sunset_datetime = None
     
    @property
    def sunset(self):
        self.sunset = datetime.strftime(self.sunset_datetime, "%H:%M:%S")
        return self._sunset
    
    @sunset.setter
    def sunset(self, value):
        self._sunset = value
    
    @property
    def sunrise(self):
        _sunrise = datetime.strftime(self.sunrise_datetime, "%H:%M:%S")
        return _sunrise
          
    @sunrise.setter
    def sunrise(self, value):
        self._sunrise = value


    @property
    def sunrise_datetime(self):
        if self._sunrise_datetime is None:
            self.suntimes()
        return self._sunrise_datetime
    
    @sunrise_datetime.setter
    def sunrise_datetime(self, value):
        if value is not None and isinstance(value, datetime):
            _sunrise_datetime = value
            logging.info(f"Setting sunrise datetime: {_sunrise_datetime}")
        else:
            raise TypeError(f"{value} must be Type datetime")
        self._sunrise_datetime = _sunrise_datetime

    @property
    def sunset_datetime(self):
        if self._sunset_datetime is None:
            self.suntimes()
        return self._sunset_datetime
    
    @sunset_datetime.setter
    def sunset_datetime(self, value):
        if value is not None and isinstance(value, datetime):
            _sunset_datetime = value
            logging.info(f"Setting sunset datetime: {_sunset_datetime}")
        else:
            raise TypeError(f"{value} must be Type datetime")
        self._sunset_datetime = _sunset_datetime

    def get_weather(self):
        """
        Calls OpenWeatherMap API to get cloud coverage of the city and
        returns it as "cloud_coverage".
        """
        logging.debug('getting weather data')
        _parameters = {
            "lat": self.latitude,
            "lon": self.longitude,
            }
        _api_suburl = self.api_weather
        _api_response = self.requester(_api_suburl, _parameters)
        # _api_response = _api_response_raw.json()
        _sunrise = _api_response['sys']['sunrise']
        _sunset = _api_response['sys']['sunset']
        logging.info(f"sunrise: {_sunrise}")
        logging.info(f"sunset: {_sunset}")
        # _time_shift = _api_response['timezone']
        self.sunrise_unix = int(_sunrise)
        self.sunset_unix = int(_sunset)
        if self.requested_day is not None:
            _cloud_coverage = 0
        else:
            _cloud_coverage = _api_response['clouds']['all']
        self._cloud_coverage = float(_cloud_coverage)
        logging.info(f"cloud coverage: {_cloud_coverage}")
        
          
    @property
    def cloud_coverage(self):
        logging.debug('getting cloud coverage')
        if self._cloud_coverage is None:
            self.get_weather()
        if isinstance(self._cloud_coverage, float):
            _cloud_coverage = self._cloud_coverage
            return _cloud_coverage
        else:
            raise TypeError("Cloud coverage must be a float.")

    def suntimes(self):
        if self.sunrise_unix or self.sunset_unix is None:
            self.get_weather()
        if isinstance(self.sunrise_unix, int) and isinstance(self.sunset_unix, int):
            _rise = datetime.fromtimestamp(self.sunrise_unix)
            _set = datetime.fromtimestamp(self.sunset_unix)
        else:
            raise TypeError("Sunrise and Sunset must be unix timestamps.")
        
        self.sunrise_datetime = _rise
        self.sunset_datetime = _set
        
        
    @property
    def sun_up(self):
        _rise: datetime = self.sunrise_datetime
        _set: datetime = self.sunset_datetime
        _date_actual = datetime.now()
        _date_actual_str = _date_actual.strftime("%Y-%m-%d")
        logging.debug(f"current date: {_date_actual_str}")
        _hour = float(self.current_time)
        _date = datetime.strptime(_date_actual_str, "%Y-%m-%d")
        _now = _date + timedelta(hours=_hour)
        logging.info(f"sunrise timestamp is {_rise}")
        logging.info(f"sunset timestamp is {_set}")
        logging.info(f"current time is {_now}")
        if _rise < _now < _set:
            _sun_up = True
        else:
            _sun_up = False
        logging.info(f"sun up: {_sun_up}")
        return _sun_up