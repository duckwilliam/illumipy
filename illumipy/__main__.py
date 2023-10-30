#!/usr/bin/env python3
"""
__main__ module for running from cli
"""

import logging
import argparse
import sys
from sys import stderr
from illumipy.data import light_data
from illumipy.defaults import CITY_DEFAULT, COUNTRY_DEFAULT, API_KEY_DEFAULT

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(
        description='General-purpose solar brightness calculator.'
        )
    argParser.add_argument(
        "-t", "--time",
        default=None,
        help="Time of the day in hours (0-24, e.g. 4 or 12). \
            Defaults to current time if not specified."
        )
    argParser.add_argument(
        "-d",
        "--date",
        default=None,
        help="Date as YYYY-MM-DD (e. g. 2023-06-01). \
            Defaults to current date if not specified."
        )
    argParser.add_argument(
        "-c", "--city",
        default=CITY_DEFAULT,
        help="City name (e. g. Berlin). \
            Defaults to {CITY_DEFAULT} if not specified."
        )
    argParser.add_argument(
        "-C",
        "--Country",
        default=COUNTRY_DEFAULT,
        help="Country name (e. g. Germany). \
            Defaults to {COUNTRY_DEFAULT} if not specified."
        )
    argParser.add_argument(
        "-a",
        "--api",
        default=API_KEY_DEFAULT,
        help="OpeWeather API-Key (required). \
            Alternatively, a default API key can be defined in main.py"
        )
    argParser.add_argument(
        "-o",
        "--output",
        default=['illuminance'],
        help="Define the parameters to be returned. \
            Defaults to 'Illuminance' if not specified.\
                    To see available values try illumipy\
                        [-o|--output] help",
        nargs='+',
        )
    argParser.add_argument(
        '-D', '--debug',
        help="Print lots of debugging statements",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    argParser.add_argument(
        '-v',
        '--verbose',
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    argParser.add_argument(
        "-A",
        "--all",
        help="Print out entire dataset. Default is just the Illuminance in Lux",
        action="store_true",
        default=False,
    )
    argParser.add_argument(
        "-s",
        "--short",
        help="Print only values, no description",
        action="store_true",
        default=False,
        )

    args = argParser.parse_args()

    LOG_FORMAT = '[%(levelname)s]:  \t%(module)s.%(funcName)s() \
        (Ln. %(lineno)d):\n\t\t\t>>> %(message)s\n'
    logging.basicConfig(level=args.loglevel, format=LOG_FORMAT)

    time_arg = args.time
    date_arg = args.date
    city_arg = args.city
    country_arg = args.Country
    api_arg = args.api
    print_all = args.all
    output_arg = args.output
    short_arg = args.short
    
    if output_arg == ['help']:
        print("Available values for output:\n\
                \t['illuminance']: Outside Brightness in Lux\n\
                \t['time']: Time used as %-H (e.g. 4 or 12)\n\
                \t['date']: Date used as YYYY-MM-DD\n\
                \t['city']: City Used\n\
                \t['country']: Country Used\n\
                \t['cloud_coverage']: Cloud coverage in %\n\
                \t['et_illuminance']: Extraterrestrial illuminance in Lux\n\
                \t['direct_illuminance']: Direct Illuminance in Lux\n\
                \t['horizontal_illuminance']: Horizontal Illuminance in Lux\n\
                \t['horizontal_sky_illuminance']: Horizontal Sky Illuminance in Lux\n\
                \t['sunrise']: Time of Sunrise as hh:mm\n\
                \t['sunset']: Time of sunset as hh:mm\n\
                \t['sun_altitude']: Sun altitude at [Time] in degrees\n\
                \t['day']: True if there is daylight at [Time]\n\
                \t['clear_sky_index'] = Aproximation of Clear Sky Index based on cloud coverage\n\
                \t['cs_irradiance'] = Estimated Clear Sky Irradiance in W/m^2 based on solar altitude.\n\
                \t['irradiance'] = Estimated current Irradiance in W/m^2 based on solar altitude and cloud coverage.")
        exit()
        
    args_debug = f"time={time_arg}, date={date_arg}, city={city_arg},\
        country={country_arg}, api_key={api_arg}"
    logging.info('Calling main function in main.py')
    logging.debug('Using these args: %s', args_debug)

    try:
        brightness = light_data(time=time_arg,
                        date=date_arg,
                        city=city_arg,
                        country=country_arg,
                        api_key=api_arg)
        if print_all is True:
            dataset = brightness.keys()
        else:
            dataset = output_arg
        for item in dataset:
            if short_arg is True:
                print(brightness[item])
            else:
                print(f"{item}: {brightness[item]}")
    except KeyboardInterrupt:
        stderr.write("Interrupted by User, exiting...\n")
        sys.exit(1)
