"""
.. module:: Postprocessing
   :platform: Unix, Windows
   :synopsis: Postprocessing module for TransAT output

.. moduleauthor:: Ascomp GmbH


"""
try:
    import para_reader as pa
except ImportError:
    print "Warning: Paraview python package is not installed"


class Postprocessing(object):
    def __init__(self):
        print "Created a new postprocessing object"
        self.pa = pa

    def pressure_drop(self, point1, point2):
        """Summary line.

        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        """
        print "pressure drop between " + point1 + " " + point2
        pass