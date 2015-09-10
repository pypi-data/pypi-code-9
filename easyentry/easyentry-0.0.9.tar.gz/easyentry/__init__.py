#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:        easyentry.py (Python 2.x/3.x).
# description: Easy data entry and validation
# author:      Antonio Suárez Jiménez, pherkad13@gmail.com
# date:        10-09-2015
#
#--------------------------------------------------------------------

'''Easy data entry and validation.'''

__author__ = 'Antonio Suárez Jiménez, pherkad13@gmail.com'
__title__= 'easyentry'
__date__ = '2015-09-10'
__version__ = '0.0.9'
__license__ = 'GNU GPLv3'

from getpass import getpass
from datetime import datetime
import re

try:
    input = raw_input
except NameError:
    pass

# Declare constants

# Message when entering an incorrect value:
# - You can type the message in your language
# - If the value is omitted, the default is the current (in English)

error_message = 'Invalid input, please try again'

# Format date and time
             
date_format = '%Y-%m-%d' # default value: '%Y-%m-%d'
time_format = '%H:%M:%S' # default value: '%H:%M:%S'

strict_return = False    # Return types of numbers: str (False) or int, float (True)
                         # if strict_return == True and value == '':
                         #     var int   --> return 0
                         #     var float --> return 0.0

global_required = False  # True  -> You must enter a valid value in all fields
                         # False -> The field can be empty (default)
                         # The value of the 'required' property of a field
                         # overrides the global value

# List of error messages (Errors description of fields and their properties):
# - You can type the message in your language

error_list = ["Error type.",
              "Error in 'default'.",
              "Error in 'options'.",
              "Error in 'minmax'.",
              "Default value not exist in 'options'.",
              "Default value not included in 'minmax'.",
              "Default value is empty.",
              "Unavailable 'minmax' with 'options'.",
              "Field without defined properties.",
              "Field not exist.",
              "Argument 'valid' is incorrect.",
              "Error in 'title'.",
              "Error in 'sorted'.",
              "Error in 'rindex'.",
              "Error in 'required'"]

# Public functions

def entry(message='', valid=()):
    '''Enter data from standard input and validate this information

    message -- Text message
    valid -- Tuple of two values: name of the dictionary that contains 
             description of all fields (properties) and name of the current field
             
    Example:

    import easyentry as ee
    
    person = {}
    person['name'] = {'type':'str'}
    person['city'] = {'type':'str', 'default':'Seville'}
    person['age']  = {'type':'int', 'minmax': [0,100]}
    person['height']  = {'type':'float'}
    person['bicycle']  = {'type':'str', 'options': ['y','n']}
    person['datetrip'] = {'type':'date', 'default': 'now'}
    person['email'] = {'type':'email', 'required': False}
    
    name = ee.entry('What is your name?', (person, 'name'))
    city = ee.entry('What city you live?', (person, 'city'))
    age = ee.entry('How old are you?', (person, 'age')) 
    height = ee.entry('Height?', (person, 'height'))
    bicycle = ee.entry('Do you have a bicycle?', (person, 'bicycle'))
    datetrip = ee.entry('Date of trip?', (person, 'datetrip'))
    email = ee.entry('Your email address', (person, 'email'))
                 
    Returns value or if the data is not considered valid must be entered another
    
    Properties of the data types available:
                                                                     empty
                                                              empty  entry
                                                              entry  ('')
                                                              ('')   strict
    type required options minmax default sorted rindex return return return
    ------------------------------------------------------------------------
    str     X       X   or   X     X       -     -     str    str    str
    int     X       X   or   X     X       -     -     int    str    int(0)
    float   X       X   or   X     X       -     -     float  str    float(0.0)
    date    X       X   or   X   x/now     -     -     str    str    str
    hour    X       X   or   X   x/now     -     -     str    str    str
    passwd  X       -        -     -       -     -     str    str    str
    email   X       -        -     -       -     -     str    str    str
    menu    X       X        -     X       X     X     str    str    str
    ------------------------------------------------------------------------
    
    '''    
    errors_accept = []
    intro = ''
    intro_correct = False
    leave = False
    field_valid = 'Error'
    if type(valid) is tuple and len(valid)==2:
            dict_valid = valid[0]
            field_valid = valid[1]
            if field_valid in dict_valid:            
                dict_field = dict_valid[field_valid]
                if len(dict_field)>0:
                    data_type, posibilities, default, mode, options, \
                    minmax, keys_options, rindex, \
                    required = __validata(dict_field, field_valid)
                    while True:                        
                        if data_type=='passwd':                            
                            intro=getpass(message+": ")
                        else:                                                       
                            intro=input(__build_message(message, posibilities, default))                                                     
                            
                        if intro=='':
                            intro=default                            

                        if data_type == 'menu':
                            if keys_options.count(intro) > 0:
                                pos_def = keys_options.index(intro)
                                if rindex:
                                    options = keys_options
                                    intro = keys_options[pos_def]
                                else:
                                    intro = options[pos_def]
                            else:
                                intro = ''

                        if data_type != 'passwd' and data_type != 'menu':
                            intro, intro_correct = __convert_datatype(data_type, intro)

                        if (mode==0 and intro_correct) or \
                            (mode==1 and __valid_default(data_type, intro)) or \
                            (mode==2 and __valid_default_options(data_type, options, intro)) or \
                            (mode==3 and __valid_default_minmax(data_type, minmax, intro)) or \
                            (mode==4) or (mode==5 and intro_correct):
                                leave = True
                                 
                        if required and intro == '':
                            leave = False
                        
                        if not required and intro == '' and \
                            (mode == 2 or mode == 3):
                                leave = True
                        
                        if leave:
                            break
                        else:
                            print(error_message)
                else:
                    errors_accept.append(error_list[8])
            else:
                errors_accept.append(error_list[9])
    else:
        errors_accept.append(error_list[10])        

    if len(errors_accept) > 0:        
        print('('+field_valid+'): ' + ' '.join(map(str, errors_accept)))
        
    return intro

# Private functions

def __valid_format_datetime(data_type):
    '''Check data type (date or time)

    data_type -- data type of the current field
                 
    Returns the current format for date or time     
    '''    
    if data_type == 'date':
        valid_format = date_format
    else:
        valid_format = time_format
        
    return valid_format   

def __valid_default(data_type, default_value):
    '''Check if default value has the same type as the input field

    data_type -- data type of the current field
    default_value -- default value
    
    Returns 'true' if the type of 'default' is the same as the field type
    '''    
    valid_data = False
    if data_type in ('str', 'int', 'float') and \
        type(default_value) is eval(data_type):
            valid_data = True
    elif data_type in ('date', 'time') and type(default_value) is str:
        try:
            valid_format = __valid_format_datetime(data_type)
            valid_datetime = datetime.strptime(default_value, valid_format)
            valid_data = True
        except:
            valid_data = False
    elif data_type == 'menu' and type(default_value) is str:
        valid_data = True
    return valid_data

def __valid_options(data_type, options):
    '''Check if the valus 'options' has the same type as the input field

    data_type -- data type of the current field
    options -- Options list
    
    Returns 'true' if the type of 'options' is the same as the field type
    '''    
    valid_data = False
    if data_type == 'menu':
        data_type = 'str'            
    if data_type in ('str', 'int', 'float'):
        valid_data = True
        for option in options:            
            if type(option) is not eval(data_type):
                valid_data = False
    elif data_type in ('date', 'time'):
        valid_data = True
        for option in options:
            try:
                valid_format = __valid_format_datetime(data_type)
                valid_datetime = datetime.strptime(option, valid_format)
            except:
                valid_data = False
    return valid_data

def __valid_minmax(data_type, minmax):
    '''Check if the values 'minmax' have the same type as the input field
    and min value < max value

    data_type -- Data type of the current field
    minmax -- List minimum and maximum value: [min, max]
    
    Returns 'true' if the type of 'minmax' is the same as the field type
    and min value < max value
    '''    
    valid_data = False
    min_value = minmax[0]
    max_value = minmax[1]
    if data_type in ('str', 'int', 'float'):
        if type(min_value) is eval(data_type) and \
            type(max_value) is eval(data_type) and min_value < max_value:
                valid_data = True
    elif data_type in ('date', 'time'):
        try:
            valid_format = __valid_format_datetime(data_type)
            min_value = datetime.strptime(min_value, valid_format)
            max_value = datetime.strptime(max_value, valid_format)                
            if  min_value < max_value:
                valid_data = True                
        except:
            valid_data = False
    return valid_data            

def __valid_default_options(data_type, options, default_value):
    '''Check if the default is in the options

    data_type -- Data type of the current field
    options -- Options list
    default_value -- Default value
    
    Returns 'true' if the default is in the options
    '''
    valid_data = False
    if data_type in ('str', 'int', 'float', 'menu'):
        valid_data = True
        if default_value not in options:
            valid_data = False
    elif data_type in ('date', 'time'):
        valid_data = True
        try:
            valid_format = __valid_format_datetime(data_type)
            valid_datetime = datetime.strptime(default_value, valid_format)
            if default_value not in options:
                valid_data = False
        except:
            valid_data = False
    return valid_data    
    
def __valid_default_minmax(data_type, minmax, default_value):
    '''Check if the default is between the minimum and maximum

    data_type -- Data type of the current field
    minmax -- List minimum and maximum value: [min, max]
    default_value -- Default value
    
    Returns 'true' if the default is between the minimum and maximum
    '''
    valid_data=False
    min_value = minmax[0]
    max_value = minmax[1]    
    if data_type in ('str', 'int', 'float'):
        if type(default_value) is eval(data_type) and \
        default_value >= min_value and default_value <= max_value:    
            valid_data = True
    elif data_type in ('date', 'time') and type(default_value) is str:
        try:
            valid_format = __valid_format_datetime(data_type)
            valid_datetime = datetime.strptime(default_value, valid_format)
            min_value = datetime.strptime(min_value, valid_format)
            max_value = datetime.strptime(max_value, valid_format)
            if valid_datetime >= min_value and valid_datetime <= max_value:
                valid_data = True
        except:
            valid_data = False
    return valid_data    

def __validata(dict_field, field_valid):
    '''Check the properties and values of the current field
    and if errors are detected displays an informational message

    dict_field -- Dictionary with the properties and values
    field_valid -- Current field  
    
    Returns values obtained and other calculated values
    '''
    errors = []
    options = []
    minmax = []
    keys_options = []
    mode = 0
    posibilities = ''
    default = ''
    default_value = ''
    title = ''
    default_exist = False
    default_error = False
    rindex = False
    required = global_required
    type_list = ['str', 'int', 'float', 'date', 'time', 'menu']
    data_type = dict_field.get('type', 'error') 
    if data_type in type_list:
        if 'default' in dict_field:
            default_value=dict_field['default']
            default_exist = True
            if data_type in ('date', 'time') and default_value == 'now':
                valid_format = __valid_format_datetime(data_type)
                if data_type == 'date':
                    default_value = datetime.now().date()
                else:
                    default_value = datetime.now().time()
                default_value = default_value.strftime(valid_format)
            if __valid_default(data_type, default_value):
                mode = 1
            else:
                default_error = True
                errors.append(error_list[1])
                
        if 'options' in dict_field:
            options=dict_field['options']            
            if type(options) is list and len(options)>0 and \
                __valid_options(data_type, options):
                if data_type != 'menu':
                    posibilities = '('+'/'.join(map(str, options))+')'
                mode = 2
                if default_exist and not default_error:
                    if __valid_default_options(data_type, options, default_value):
                        default = default_value
                    else:
                        errors.append(error_list[4])
                        default_error = True                                        
            else:
                errors.append(error_list[2])
                                
            if 'minmax' in dict_field:
                errors.append(error_list[7])
                
        elif 'minmax' in dict_field:
            minmax=dict_field['minmax']
            if type(minmax) is list and len(minmax)== 2 and \
                __valid_minmax(data_type, minmax):
                posibilities = '('+'-'.join(map(str, minmax))+')'
                mode = 3
                if default_exist and not default_error:
                    if __valid_default_minmax(data_type, minmax, default_value):
                        default = default_value
                    else:
                        errors.append(error_list[5])
                        default_error = True                                                                        
            else:
                errors.append(error_list[3])

        if default_exist and default =='' and not default_error: 
            if default_value !='':
                default = default_value
            else:
                errors.append(error_list[6])
                
        if data_type == 'menu' and len(options) > 0:
            if 'title' in dict_field and type(dict_field['title']) is str:
                title=dict_field['title']
            else:
                errors.append(error_list[11])
                
            if 'sorted' in dict_field:
                sorter=dict_field['sorted']
                if type(sorter) is bool:
                    if sorter:
                        options.sort()
                else:
                    errors.append(error_list[12])
                    
            if 'rindex' in dict_field:
                rindex=dict_field['rindex']
                if type(rindex) is not bool:
                    rindex=False
                    errors.append(error_list[13])

            len_opt = len(options)
            len_opt = len(str(len_opt))
            if default !='' and options.count(default) > 0:
                pos_def = options.index(default) + 1
            else:
                pos_def = len(options)
            default = str(pos_def)
            
            posibilities = '\n'
            for number in range(len(options)):
                index = str(number + 1)
                keys_options.append(index)
                posibilities += '('+index+') '+str(options[number])+'\n'
            
            posibilities += title
                        
    elif data_type == 'passwd':
        mode = 4
        
    elif data_type == 'email':
        mode = 5
        
    else:
        errors.append(error_list[0])
    
    if 'required' in dict_field:
        required=dict_field['required']
        if type(required) is not bool:
            errors.append(error_list[14])
    
    if len(errors) > 0:
        print('('+field_valid+'): ' + ' '.join(map(str, errors)))

    return data_type, posibilities, default, mode, \
        options, minmax, keys_options, rindex, required

def __build_message(message='', posibilities='', default=''):  
    '''Build message

    message -- String with message
    posibilities -- String with 'options' or 'minmax'
    default -- String with default value
    
    Returns a string with message of the current entry
    '''            
    if posibilities!='':
        message+=' '+posibilities
    if default!='':
        message+=' ['+str(default)+']'
    message+=': '
    return message.lstrip()

def __convert_datatype(data_type, intro):
    '''Converts data type (int and float) text string to number
    (if 'strict_return' is true) and check if the entered value is correct

    data_type -- Data type of the current field
    intro -- entered value
    
    Returns entered value (or converted) and 'True' if a valid value
    '''            
    intro_correct = True
    if data_type in ('int', 'str', 'float'):
        try:
            if strict_return:
                if data_type=='int' and intro=='':
                    intro=0
                elif data_type=='float' and intro=='':
                    intro=0.0
            else:
                if data_type=='int':
                    intro=int(intro)
                elif data_type=='float':
                    intro=float(intro)
        except:
            pass
        
    if data_type in ('int', 'float') and \
        type(intro) is str and intro !='':
            if data_type == 'int':
                try:
                    int(intro)
                except:
                    intro_correct = False
            else:
                try:
                    float(intro)
                except:
                    intro_correct = False
                            
    if data_type in ('date', 'time'):
        try:
            if intro != '':
                valid_format = __valid_format_datetime(data_type)                                                                        
                intro = datetime.strptime(intro, valid_format)
                intro = intro.strftime(valid_format)
                intro_correct = True                                
        except:
            intro_correct = False
            
    if data_type == 'email' and (not re.match(r'.+\@.+\..+', intro) and \
        intro !=''):
            intro_correct = False
 
    return intro, intro_correct


