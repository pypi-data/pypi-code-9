#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


class Form(object):
    """ Demonstration class.
    """
    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError()


class Square(Form):
    """ Demonstration class.
    """
    def area(self, length_of_side):
        return length_of_side ** 2


class Triangle(Form):
    """ Demonstration class.
    """
    def area(self, base, vertical_height):
        return 0.5 * base * vertical_height
