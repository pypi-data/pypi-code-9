import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np


# Cherenkov Spot size strips {{{
def histcher(x, y, res):
    """
    .. deprecated:: 0.0.0

    I'm not really sure what this function does, but it's not referenced anywhere else.
    """
    h, xe, ye = _np.histogram2d(x, y, res)
    xval      = (xe[1]-xe[0])/2. + xe
    xval      = xval[0:-1]
    
    dely = (ye[1]-ye[0])
    yavg = dely/2. + ye
    yavg = yavg[0:-1]
    
    etay = 0.070673884756039224
    davg = (etay/(etay-yavg)) - 1
    # davg = yavg/etay
    
    # filt=(davg>-0.01) & (davg < 0.01)

    out = [h, xval, davg]
    return out
# }}}
