#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


def addition(a, b):
    """ Demonstration function.
    """
    return a + b


def substraction(a, b):
    """ Demonstration function.
    """
    return a - b


def factorial(a):
    """ Demonstration function.
    """
    if a == 1:
        return 1
    else:
        return a * factorial(a - 1)
