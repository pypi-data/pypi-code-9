#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:        example.py (Python 2.x/3.x).
# description: Example (Easy data entry and validation)
# author:      Antonio Suárez Jiménez, pherkad13@gmail.com
# date:        10-09-2015
#
#--------------------------------------------------------------------

'''Easy data entry and validation.'''

__author__ = 'Antonio Suárez Jiménez, pherkad13@gmail.com'
__title__= 'example'
__date__ = '2015-09-10'
__version__ = '0.0.9'
__license__ = 'GNU GPLv3'

import easyentry as ee

# Declares constants

# Message when entering an incorrect value:
# - You can type the message in your language
# - If the value is omitted, the default is the current (in English)

ee.error_message = 'Invalid input, please try again'

# Format date and time

ee.date_format = '%d-%m-%Y' # default value: '%Y-%m-%d'
ee.time_format = '%H:%M'    # default value: '%H:%M:%S'

ee.strict_return = False    # Return types of numbers: str (False) or int, float (True)
                            # if strict_return == True and value == '':
                            #     var int   --> return 0
                            #     var float --> return 0.0

ee.global_required = True   # True  -> You must enter a valid value in all fields
                            # False -> The field can be empty (default)
                            # The value of the 'required' property of a field
                            # overrides the global value

# The list of error messages can also be declared in its usual language. 
# - See the source code module

# ee.error_list = [] 

# Declares field properties

person = {}
person['name'] = {'type':'str'}
person['city'] = {'type':'str', 'default':'Seville'}
person['age']  = {'type':'int', 'minmax': [0,100]}
person['height']  = {'type':'float'}
person['bicycle']  = {'type':'str', 'options': ['y','n']}
person['datetrip'] = {'type':'date', 'default': 'now'}
person['email'] = {'type':'email', 'required':False}
person['passwd'] = {'type':'passwd'}
person['info'] = {'type':'menu', 'title': 'Select an option', 
                  'options':['phone','mail','none'], 'rindex':True}

# Enter and validate data

name = ee.entry('What is your name?', (person, 'name'))
city = ee.entry('What city you live?', (person, 'city'))
age = ee.entry('How old are you?', (person, 'age'))
height = ee.entry('Height?', (person, 'height'))
bicycle = ee.entry('Do you have a bicycle?', (person, 'bicycle'))
datetrip = ee.entry('Date of trip?', (person, 'datetrip'))
email = ee.entry('Your email address', (person, 'email'))
info = ee.entry('To receive information by...', (person, 'info'))
passwd = ee.entry('Enter password', (person, 'passwd'))
repeat = ee.entry('Repeat password', (person, 'passwd'))

# Show the entry data

print('Name:', name)
print('City:', city)
print('Age:', age)
print('Height:', height)
print('Bicycle:', bicycle)
print('Datetrip:', datetrip)
print('Email:', email)
print('Info:', info)
if passwd == repeat:
    print('Passwd:', passwd)
