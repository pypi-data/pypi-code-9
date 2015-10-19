#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2015, IBM Corp.
# All rights reserved.
#
# Distributed under the terms of the BSD Simplified License.
#
# The full license is in the LICENSE file, distributed with this software.
#-----------------------------------------------------------------------------

""" Utility functions """

# Python 2 compatibility
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import input
from future import standard_library
standard_library.install_aliases()

import sys
import os
import warnings
from time import time
from functools import wraps

import six

#-----------------------------------------------------------------------------
# Environment variable setter

def set_verbose(is_verbose):
    """
    Set the environment variable "VERBOSE" to 'TRUE' or 'FALSE'
    If it is set to 'TRUE', all SQL request will be printed in the console
    """
    if is_verbose is True:
        os.environ['VERBOSE'] = 'True'
    elif is_verbose is False:
        os.environ['VERBOSE'] = 'False'
    else:
        raise ValueError("is_verbose should be a boolean")

def set_autocommit(is_autocommit):
    """
    Set the environment variable "AUTCOMMIT" to 'TRUE' or 'FALSE'
    If it is set to 'TRUE', all operations will be commited automatically
    """
    if is_autocommit is True:
        os.environ['AUTOCOMMIT'] = 'True'
    elif is_autocommit is False:
        os.environ['AUTOCOMMIT'] = 'False'
    else:
        raise ValueError("is_autocommit should be a boolean")

#-----------------------------------------------------------------------
# Performance measurement wrapper

def timed(function):
    """
    Perform mesurement of elapsed time on custom functions of the package.
    Should be used as a decorator.
    """
    @wraps(function)
    def wrapper(*args, **kwds):
        """Calculate elapsed time in seconds"""
        start = time()
        result = function(*args, **kwds)
        elapsed = time() - start
        if os.environ['VERBOSE'] == 'True':
            print("Execution time: %s seconds." %elapsed)
        return result
    return wrapper

def query_yes_no(question, default=None):
    """
    Ask a yes/no question via raw_input() and return their answer.

    Parameters
    ----------
    question : str
        Question to be ask to the user. Should be a yes/no question
    default : "yes"/"no"
        The presumed answer if the user just hits <Enter>.

    Returns
    -------
    bool
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower() # in Python 2.7, it is raw_input
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def check_tablename(tablename):
    """
    Check if a string is in upper case, upper cases it and check if it is a
    valid table name

    Parameters
    ----------
    tablename : str
        string to check

    Returns
    -------
    str
        Checked and upper cased table name

    Notes
    -----
        Table names should be composed of capital letters or numbers separated
        by underscores ("_") characters
    """
    tablename = check_case(tablename)
    if not all([(char.isalnum() | (char == '_') | (char == '.')) for char in tablename]):
        raise ValueError("Table name is not valid, only alphanum characters and underscores are allowed.")
    if tablename.count(".") > 1:
        raise ValueError("Table name is not valid, only one '.' character is allowed.")
    return tablename

def check_viewname(viewname):
    """
    Convenience function. Just an alternative name to check_tablename for
    checking names for view, which have the same prerequisites as tablenames.
    See check_tablename documentation.
    """
    return check_tablename(viewname)

def check_case(name):
    """
    Check if the name given as parameter is in upper case and upper cases it
    """
    if name != name.upper():
        warnings.warn("Mixed case names are not supported in database object names.", UserWarning)
    return name.upper()

def _convert_dtypes(idadf, data):
    """
    DEPRECATED - CURRENTLY NOT IN USE
    was used for formatting dataframe types

    Convert datatypes in a dataframe to float or to int according to the
    corresponding type in database. Work only if the dataframe given as
    parameter has the same columns as the current IdaDataFrame.
    """
    # Note : Here I made the choice to convert every numeric attributes to
    # float, the reason is that converting to int for an attribute that has
    # missing values leads to an error, this is known as a pandas' gotcha
    # We could use statistics._get_number_of_nas to know if there are
    # missing values for each attributes, but I made the choice no to do it,
    # this for reducing complexity and improve performance. However, it no
    # efficient in terms of memory.
    import pdb ; pdb.set_trace() ;
    original_dtype = idadf.dtypes

    int_attributes = ['SMALLINT', 'INTEGER', 'BIGINT', 'BOOLEAN']
    float_attributes = ['REAL', 'DOUBLE', 'FLOAT', 'DECIMAL',
                        'DECFLOAT', 'APPROXIMATE', 'NUMERIC']
    for index, dtype in enumerate(original_dtype.values):
        if dtype[0] in int_attributes + float_attributes:
            data[[data.columns[index]]] = data[[data.columns[index]]].astype(float)
        else:
            data[[data.columns[index]]] = data[[data.columns[index]]].astype(object)
    return data

def _reset_attributes(idaobject, attributes):
    """
    Detele an attribute of list of attributes of an object, if they exist.
    """
    if (not hasattr(attributes, "__iter__"))|isinstance(attributes, six.string_types):
        attributes = [attributes]
    for attribute in attributes:
        try:
            delattr(idaobject, attribute)
        except AttributeError:
            pass
