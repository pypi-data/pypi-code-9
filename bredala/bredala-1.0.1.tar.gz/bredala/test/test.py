#! /usr/bin/env python
##########################################################################
# Bredala - Copyright (C) AGrigis, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import unittest

# Bredala import
import bredala
bredala.USE_PROFILER = True
bredala.register("bredala.demo.myfunctions", names=["addition", "factorial"])
bredala.register("bredala.demo.myclasses", names=["Square.area",
                                                  "Triangle.area"])
from bredala.demo.myfunctions import addition, substraction, factorial
from bredala.demo.myclasses import Square, Triangle


class TestBredala(unittest.TestCase):
    """ Test the module functionalities.
    """
    def test_specific_functions(self):
        """ Test functions execution follow up.
        """
        addition(2, 1)
        substraction(2, 1)
        factorial(5)

    def test_specific_classes(self):
        """ Test class methods execution follow up.
        """
        o = Square("my_square")
        o.area(2)
        o = Triangle("my_square")
        o.area(2, 3)


def test():
    """ Function to execute unitest
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBredala)
    runtime = unittest.TextTestRunner(verbosity=2).run(suite)
    return runtime.wasSuccessful()


if __name__ == "__main__":
    test()
