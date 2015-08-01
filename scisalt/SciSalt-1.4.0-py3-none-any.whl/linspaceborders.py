# from .linspacestep import linspacestep as _linspacestep
import numpy as _np


def linspaceborders(arr):
    # Get and set left side
    dela = arr[1] - arr[0]
    new_arr = _np.array([arr[0] - dela / 2])

    # Add a point to the right side so the for loop works
    delb = arr[-1] - arr[-2]
    arr = _np.append(arr, arr[-1] + delb)
    for i, val in enumerate(arr):
        try:
            avg = (arr[i] + arr[i + 1]) / 2
            new_arr = _np.append(new_arr, avg)
        except:
            pass
    # start = arr[0] - dela / 2
    # end = arr[-1] + dela / 2
    # return _linspacestep(start, end, dela)
    return new_arr
