#!/usr/bin/env python3
"""
General-purpose solar irradiance and brightness calculator.
"""
import logging
import math
from illumipy.classes.base_classes import Basedata, Weather

class Illumination(Basedata):
    """
    Class Illuminaion:
    Calculate Outside Illumination in Lux
    for given location and time
    """
 
    def __init__(self,
                 name=None,
                 api_key=None,
                 api_base=None,
                 api_loc=None,
                 api_weather=None,
                 city=None,
                 country=None,
                 requested_day=None,
                 requested_hour=None,
                 cloud_coverage=None,
                 day=None
                 ):
        logging.debug("initialising illumination class")
        if name is None:
            name = "illumination"
        logging.info("initialising parent class")
        super().__init__(self)
        if name is not None:
            self.name = name
        if api_key is not None:
            self.api_key = api_key
            logging.info(f'setting api_key in illumination object: {self.api_key}')
        if api_base is not None:
            self.api_base = api_base
        if city is not None:
            self.city = city
            logging.info(f'setting city in illumination object: {self.city}')
        if country is not None:
            self.country = country
            logging.info(f'setting country in illumination object: {self.country}')
        if api_loc is not None:
            self.api_loc = api_loc
        if api_weather is not None:
            self.api_weather = api_weather
        # print("creating weather object")
        logging.info('creating Weather object')
        weather = Weather(self)
        # print("created weather object, setting Hour value in weather")
        if requested_day is not None:
            self.requested_day = requested_day
            logging.info(f'setting requested_day in illumination object: {self.requested_day}')
            weather.requested_day = self.requested_day
            logging.info(f'setting requested_day in weather object: {weather.requested_day}')
        #print(f"setting requested_hour in illumination object: {self.requested_hour}")
        if requested_hour is not None:
            self.requested_hour = requested_hour
            logging.info(f'setting requested_hour in illumination object: {self.requested_hour}')
            weather.requested_hour = self.requested_hour
            logging.info(f'setting requested_hour in weather object: {weather.requested_hour}')
        weather.city = self.city
        logging.debug(f'setting city in weather object: {weather.city}')
        weather.country = self.country
        logging.debug(f'setting country in weather object: {weather.country}')
        weather.api_key = self.api_key
        logging.debug(f'setting api_key in weather object: {weather.api_key}')
        if cloud_coverage is None:
            cloud_coverage = weather.cloud_coverage
        if day is None:
            day = weather.sun_up
        self.day = day
        self.sunrise = weather.sunrise
        self.sunset = weather.sunset
        self.timezone = weather.timezone
        self.cloud_coverage = cloud_coverage
        self.altitude_cached = 90

    def rounder(self, number: float, decimals: int):
        """
        Rounds a number to a specific number of decimals.
        """
        return round(number+10**(-len(str(number))-1), decimals)

    @property
    def et_illuminance(self):
        """
        Returns the ET Illuminance in Lux
        based on time of the year.
        """
        _day_of_the_year = self.day_of_the_year
        _et_illuminance = float(129) * (1 + 0.034 * math.cos(((2 * math.pi)/356) * (_day_of_the_year - 2)))
        logging.info(f'calculated extraterrestrial_illuminance: {_et_illuminance}')
        return self.rounder(_et_illuminance, 2)

    @property
    def local_standard_time_meridian_rad(self):
        """
        calculates local standard time meridian
        """
        _lstm_rad = math.radians(15) * self.timezone
        return self.rounder(_lstm_rad, 2)

    @property
    def equation_of_time_rad(self):
        _doy = self.day_of_the_year
        _B_rad = math.radians((360/365) * (_doy - 81))
        _eot_rad = 9.87 * math.sin(2 * _B_rad) - 7.53 * math.cos(_B_rad) - 1.5 * math.sin(_B_rad)
        return self.rounder(_eot_rad, 2)
    
    @property
    def time_correction_factor_rad(self):
        _eot_rad = self.equation_of_time_rad
        _lsmt_rad = self.local_standard_time_meridian_rad
        long_rad = math.radians(self.longitude)
        _tcf_rad = 4 * (long_rad - _lsmt_rad) + _eot_rad
        return self.rounder(_tcf_rad, 2)
        
    @property
    def local_solar_time_rad(self):
        _lt = int(self.current_time)
        _tcf_rad = self.time_correction_factor_rad
        _lst = _lt + (_tcf_rad / 60)
        return self.rounder(_lst, 2)
        
    @property
    def hour_angle_rad(self):
        _lst = self.local_solar_time_rad
        _hra_rad = math.radians(15) * (_lst - 12)
        return self.rounder(_hra_rad, 2)
        
    @property
    def declination_angle_rad(self):
        _doy = self.day_of_the_year
        _da_rad = math.radians(-23.45) * math.cos(math.radians((360/365) * (_doy + 10)))
        return self.rounder(_da_rad, 2)
    
    @property
    def altitude(self):
        """
        Calculates the solar altitude for a given longitude, date and time.
        Returns solar altitude in degrees.
        """
        _lat_rad = math.radians(self.latitude)
        _hra_rad = self.hour_angle_rad
        _da_rad = self.declination_angle_rad
        _alt_rad = math.asin(math.sin(_da_rad) * math.sin(_lat_rad) + math.cos(_da_rad) * math.cos(_lat_rad) * math.cos(_hra_rad))
        _alt_deg = math.degrees(_alt_rad)
        self.altitude_cached = self.rounder(_alt_deg, 2)
        logging.info(f"altitude: {_alt_deg}")
        return self.rounder(_alt_deg, 2)
    
    @property 
    def solar_azimuth(self):
        _lat_rad = math.radians(self.latitude)
        _alt_rad = math.radians(self.altitude)
        _hra_rad = self.hour_angle_rad
        _da_rad = self.declination_angle_rad
        _azi_rad = math.acos(((math.sin(_da_rad) * math.cos(_lat_rad)) - (math.cos(_da_rad) * math.sin(_lat_rad) * math.cos(_hra_rad))) / math.cos(_alt_rad))
        _azi_deg = math.degrees(_azi_rad)
        return self.rounder(_azi_deg, 2)
        
    @property
    def clear_sky(self):
        """
        calculate clear sky index from cloud cover
        """
        cloud_fraction = self.cloud_coverage / 100
        if cloud_fraction == 1:
            cloud_oct = 1.0882
        else: 
            cloud_oct = cloud_fraction
        csi = 0.75 * (cloud_oct)**3.4
        return self.rounder(csi, 2)
        
    @property
    def irradiance_clear(self):
        """
        Calculates solar irradiance for clear skies 
        """
        _alt_rad = self.altitude
        _irradiance_clear = 910 * math.sin(_alt_rad) - 30
        return self.rounder(_irradiance_clear, 2)
    
    @property
    def solar_radiation_direct(self):
        _am_rad = self.air_mass
        _srd = 1.353 * 0.7 ** (_am_rad ** 0.670)
    
    @property
    def irradiance_cloud(self):
        """
        calculates solar irradiance for given 
        cloud level 
        """
        _irradiance_clear = self.irradiance_clear
        _csi = self.clear_sky
        _irradiance_cloud = _irradiance_clear * (1 - _csi) 
        return self.rounder(_irradiance_cloud, 2)
    
    @property
    def air_mass(self):
        """
        Calculates the air mass for a given solar altitude.
        """
        _altitude = self.altitude
        _am_rad = 1/(math.cos(math.radians(90 - _altitude)) + 0.50572/(96.07995 - math.radians(90 - _altitude))**1.6364)
      #  _air_mass = 1 / (math.cos(_altitude) + 0.50572 * (96.07995 - _altitude)**-1.6364)
        logging.info(f"air_mass: {_am_rad}")
        return self.rounder(_am_rad, 2)
    
    @property
    def cloud_coefficients(self):
        """
        Gets current cloud coverage from OpenWeather API and
        uses it to set coefficients for later calculation.
        """
        _clear_sky = self.clear_sky
        if _clear_sky < 0.3:
            _cloud_coefficients = {
                "c": 0.21,
                "A": 0.8,
                "B": 15.5,
                "C": 0.5
            }
        elif _clear_sky < 0.8:
            _cloud_coefficients = {
                "c": 0.8,
                "A": 0.3,
                "B": 45.0,
                "C": 1.0
            }
        else:
            _cloud_coefficients = {
                "c": None,
                "A": 0.3,
                "B": 21.0,
                "C": 1.0
            }
        logging.info(f"cloud_coefficients: {_cloud_coefficients}")
        return _cloud_coefficients

    @property
    def direct_illuminance(self):
        """
        converts extraterrestrial illuminance into
        direct illuminance by factoring in air mass and atmospheric
        extinction, estimated by cloud coverage.
        """
        _c = self.cloud_coefficients.get('c')
        _air_mass = self.air_mass
        _et_illuminance = self.et_illuminance
        if _c is None:
            _direct_illuminance = 0
        else:
            _direct_illuminance = _et_illuminance * math.exp(-1 * _c * _air_mass)
        logging.info(f"direct_illuminance: {_direct_illuminance}")
        return self.rounder(_direct_illuminance, 2)

    @property
    def horizontal_illuminance(self):
        """
        converts direct illuminance into horizontal illuminence
        by taking into account the current solar altitude.
        """
        _altitude = self.altitude
        _direct_illuminance = self.direct_illuminance
        _horizontal_illuminance = _direct_illuminance * math.sin(_altitude)
        logging.info(f"horizontal_illuminance: {_horizontal_illuminance}")
        return self.rounder(_horizontal_illuminance, 2)
    
    @property
    def horizontal_sky_illuminance(self):
        """
          @brief Returns the illuminance of the sky. This is defined as A + B * ( sin ( theta ) ** C )) where theta is the altitude in degrees. The coefficients A B and C are used to calculate the illuminance.
          @return sky illuminance as a floating point number
        """         
        _altitude_temp = self.altitude_cached
        # This function sets the altitude to the given value.
        if isinstance(_altitude_temp, float):
            _altitude = _altitude_temp
        else:
            _altitude = float(_altitude_temp)
            
        _coefficients = self.cloud_coefficients
        _A_temp = _coefficients.get('A')
        _B_temp = _coefficients.get('B')
        _C_temp = _coefficients.get('C')
        # float _C_temp float _C_temp float _C_temp
        if isinstance(_A_temp, float):
            _A = _A_temp
        else:
            _A = float(_A_temp)
        if isinstance(_B_temp, float):
            _B = _B_temp
        else:
            _B = float(_B_temp)
        if isinstance(_C_temp, float):
            _C = _C_temp
        else:
            _C = float(_C_temp)
        _sky_illuminance = _A + (_B * (math.sin(_altitude))**_C)
        logging.info(f"horizontal__sky_illuminance: {_sky_illuminance}")
        return self.rounder(_sky_illuminance, 2)
    
    @property
    def daylight_illuminance(self):
        """
        @brief Returns the illuminance of the sky. This is defined as A + B * ( sin ( theta ) ** C )) where theta is
        the altitude in degrees. The coefficients A B and C are used to calculate the illuminance.
        @return sky illuminance as a floating point number
        """
        if self.day is True:
            _sky_illuminance = self.horizontal_sky_illuminance
            _horizontal_illuminance = self.horizontal_illuminance        
            _daylight = (_sky_illuminance + _horizontal_illuminance) * 1000
        elif self.day is False:
            _daylight = 0
        else:
            raise ValueError("Invalid value for day.")
        return int(self.rounder(number=_daylight, decimals=0))