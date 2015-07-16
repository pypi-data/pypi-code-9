# from .linspacestep import linspacestep as _linspacestep
import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np


def linspaceborders(array):
    """
    Given a 1-D *array*, generate a new array with numbers between the numbers of the input *array*. Adds elements to the left and right sides to get the exterior border as well.

    Returns a :class:`numpy.ndarray`.
    """
    # Get and set left side
    dela = array[1] - array[0]
    new_arr = _np.array([array[0] - dela / 2])

    # Add a point to the right side so the for loop works
    delb = array[-1] - array[-2]
    array = _np.append(array, array[-1] + delb)
    for i, val in enumerate(array):
        try:
            avg = (array[i] + array[i + 1]) / 2
            new_arr = _np.append(new_arr, avg)
        except:
            pass
    # start = array[0] - dela / 2
    # end = array[-1] + dela / 2
    # return _linspacestep(start, end, dela)
    return new_arr
