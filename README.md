**illumipy** is a Python module for estimating outside Illumination levels for given location, date and time.
Requires an OpenWeatherMap [APIkey](https://openweathermap.org/appid)

## Features
- Provides an estimation of outside brightness level based on weather and astronomical data, location, time and empirical model.
- Calculates a variety of solar parameters that can be used for prediction of solar irradiance and solar energy production
- Can be adjustes for date, time, location, cloud coverage and many more.
- Can be used as imported Python module or accessed directly over CLI with a range of useful options
- Uses the free OpenWeatherMap API

## INSTALLATION

Installation is easiest using a package manager like [PIP](https://pip.pypa.io/en/stable/ ). To install pip run:
```bash
python -m ensurepip --upgrade 
```

To install illumipy with pip, run:
```bash
pip install illumipy 
```

Source files can be found on [GitHub](https://github.com/duckwilliam/illumipy), in case you want to tell install manually.   
  This package can be used via import function in Python or be run directly as a script with CLI options:

### Import
```python
import illumipy
# Create Illumination object using light_data() and pass options
illumipy.data.light_data([OPTIONS]) 
```
To use the module, simply import illumipy and call the function
data.light_data(): This returns a dictionary object with
the following information:
+ ['illuminance']: Outside Brightness in Lux
+ ['time']: Time used as %-H (e.g. 4 or ~~12)
+ ['date']: Date used as YYYY-MM-DD
+ ['city']: City Used
+ ['country']: Country Used
+ ['cloud_coverage']: Cloud coverage in %
+ ['et_illuminance']: Extraterrestrial Illuminance in Lux
+ ['direct_illuminance']: Direct Illuminance in Lux
+ ['horizontal_illuminance']: Horizontal Illuminance in Lux
+ ['horizontal_sky_illuminance']: Horizontal Sky Illuminance in Lux
+ ['sunrise']: Time of Sunrise as hh:mm
+ ['sunset']: Time of sunset as hh:mm
+ ['sun_altitude']: Sund altitude at [Time] in degrees.
+ ['day']: True if there is daylight at [Time].
+ ['clear_sky_index'] = Aproximation of Clear Sky Index based on cloud coverage
+ ['cs_irradiance'] = Estimated Clear Sky Irradiance in W/m^2 based on solar altitude.
+ ['irradiance'] = Estimated current Irradiance in W/m^2 based on solar altitude and cloud coverage.
+ coverage.
+ ['air_mass'] = calculated air mass for given solar altitude, based on empirical model.
+ ['azimuth'] = Calculated solar azimuth for given time and location.
+ ['declination'] = calculated solar declination angle for given date.
+ ['LSTM'] = Local standard time meridian in degrees.
+ ['EOT'] = Equation of Time.

It Takes the following arguments:
+ time: str=[0-24]
+ date: str=[YYYY-MM-DD]
+ city: str=['City']
+ country: str=['Country']
+ api_key: str=['api_key']
+ cloud_coverage: int=[0-100]  

*if no arguments are provided, defaults to values defined in defaults.py*  

### Command line 
To use as script with CLI run <python -m illumipy>.
To get a list of available CLI options run <
```bash
python -m illumipy -h
> usage: __main__.py [-h] [-t TIME] [-d DATE] [-c CITY]
                   [-C COUNTRY] [-a API]
                   [-o OUTPUT [OUTPUT ...]] [-D] [-v] [-A] [-s]

General-purpose solar brightness calculator.

options:
  -h, --help            show this help message and exit
  -t TIME, --time TIME  Time of the day in hours (0-24, e.g. 4
                        or 12). Defaults to current time if not
                        specified.
  -d DATE, --date DATE  Date as YYYY-MM-DD (e. g. 2023-06-01).
                        Defaults to current date if not
                        specified.
  -c CITY, --city CITY  City name (e. g. Berlin). Defaults to
                        {CITY_DEFAULT} if not specified.
  -C COUNTRY, --Country COUNTRY
                        Country name (e. g. Germany). Defaults
                        to {COUNTRY_DEFAULT} if not specified.
  -a API, --api API     OpeWeather API-Key (required).
                        Alternatively, a default API key can be
                        defined in main.py
  -o OUTPUT [OUTPUT ...], --output OUTPUT [OUTPUT ...]
                        Define the parameters to be returned.
                        Defaults to 'Illuminance' if not
                        specified. To see available values try
                        illumipy [-o|--output] help
  -D, --debug           Print lots of debugging statements
  -v, --verbose         Be verbose
  -A, --all             Print out entire dataset. Default is
                        just the Illuminance in Lux
  -s, --short           Print only values, no description
```
  
## Current issues
- cloud level, sunrise and sunset are not available for dates in the past. Results might therefore be unreliable. Times for sunrise and sunset will always be for the current day.

- ~~at 100% cloud coverage, Results might be unreliable.~~    

## Requirements
- Python3
- Python packages:
  - requests
  - logging
  - math
  - sys
  - datetime
  - argparse
- OpenWeatherMap API-Key

## About
Author: Kalle Fornia  
GitHub: https://github.com/duckwilliam/illumipy  
PyPi: https://pypi.org/project/illumipy  
Version: 1.3.1
10/2023 
