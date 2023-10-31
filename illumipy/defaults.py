#!/usr/bin/env python3
"""
Default Values for illumipy
"""
import os

__all__ = ['API_KEY_DEFAULT', 'CITY_DEFAULT', 'COUNTRY_DEFAULT']

class Constants:
    def __init__(self, 
                 os_const: str, 
                 py_constant: str
                 ):
        self.os_const = os_const
        self.py_constant = py_constant
        self.value = None
        
    @property
    def value(self):
        try:
            _value = os.environ[os_const]
        except KeyError:
            print(f"{os_const} not defined:\n\t{_value = :^>20}\n\tRun <python -m illumipy --defaults set> to add missing values to your os environment")
        except:
            print(f"could not assign a value to {py_const}") 
        else:
            self.value = _value
            return self._value
            
    @value.setter
    def value(self, new_value)
        self._value = new_value
   

os_env_vals = {
    'API_KEY_DEFAULT': 'OPENWEATHERMAP_API_KEY', 
    'CITY_DEFAULT': 'OPENWEATHERMAP_CITY', 
    'COUNTRY_DEFAULT': 'OPENWEATHERMAP_COUNTRY'
   } 

py_const_vals = {} 

for pyc, osc in os_env_vals.items():
    constant = Constants(os_const=osc, py_const=pyc)
    py_constant_vals[pyc]=constant
    

API_KEY_DEFAULT = py_constant_vals['API_KEY_DEFAULT']
CITY_DEFAULT = py_constant_vals['CITY_DEFAULT']
COUNTRY_DEFAULT = py_constant_vals['COUNTRY_DEFAULT']

def set_os_env():
    APIkey = input('Enter OpenWeatherMap API key: ') 
    City = input('Enter default city: ')
    Country = input('Enter default country: ')
    
    _api = f"export OPENWEATHERMAP_API_KEY='{APIkey}'"
    _City = f"export OPENWEATHERMAP_CITY='{City}'"
    _Country = f"export OPENWEATHERMAP_COUNTRY='{Country}'"
    
    with open(os.path.join((os.path.expanduser('~'), '.bashrc'), "a") as bashrc:
        bashrc.write(f"{_APIkey}\n{_City}\n{_Country}")
   
        