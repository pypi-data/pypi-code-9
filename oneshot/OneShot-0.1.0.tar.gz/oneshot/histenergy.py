import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np


# Energy spot size strips {{{
def histenergy(x, d, res):
    """
    .. deprecated:: 0.0.0

    I'm not really sure what this function does, but it's not referenced anywhere else.
    """
    h, xe, ye = _np.histogram2d(x, d, res)
    xval      = (xe[1]-xe[0])/2. + xe
    xval      = xval[0:-1]
    
    davg = (ye[1]-ye[0])/2. + ye
    davg = davg[0:-1]
    
    # filt=(davg>-0.01) & (davg < 0.01)

    out = [h, xval, davg]
    return out
# }}}
