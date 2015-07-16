import numpy as _np

E0 = 20.35
# y0 = 456.149271788
y0 = 452.777049004

# def E200_cam_E_cal(h5file, y, res):
#     _checkres(res)
#     # ====================================
#     # Calibration depends on good orbit through quads,
#     # spectrometer magnet strength, and ...?
#     # ====================================
#
#     # ====================================
#     # Get the magnet strength
#     # ====================================
#     B_spect = _get_B(h5file)
#
#     # ====================================
#     # The dispersion at y0
#     # ====================================
#     # yc = y0 + etay/res
#     yc = _yc(y0, etay, res)
#
#     # ====================================
#     # Convert to energy axis
#     # E_axis = -etay*E0./(y-y0)
#     # E_axis = E0./( 1-((y-y0)/etay) )
#     # E_axis = E0*( 1- (y-y0)/etay )
#     E_axis = -etay*E0 / ( (y-yc)*res )
#
#     return E_axis
#
#     # display(-etay*(0.01)+y0)
#     # display(-etay*(-0.01)+y0)

# def y_to_E(y, h5file, res):
#         _checkres(res)
#         # y = float(y)
#         B_spect = _get_B(h5file)
#         # E0 = 20.35
#         # yc = y0 + etay/res
#         yc = _yc(y0, etay, res)
#         E = -etay*E0 / ( (y-yc)*res )
#         return E


def E_to_y(E, h5file, res):
    _checkres(res)

    B_spect = _get_B(h5file)

    etay = _etay(B_spect)

    # E0 = 20.35
    # yc = y0 + etay/res
    yc = _yc(y0, etay, res)
    y = -etay*(E0/E)/res - yc

    return y


def avg_E(y1, y2, h5file, res):
    _checkres(res)

    B_spect = _get_B(h5file)
    etay    = _etay(B_spect)

    # E0 = 20.35
    # yc = y0 + etay/res
    yc = _yc(y0, etay, res)

    out = -(etay*E0/res) * _np.log( (y2+yc)/(y1+yc) ) / (y2-y1)
    return out


def _get_B(h5file):
    return h5file[h5file['data']['raw']['scalars']['LI20_LGPS_3330_BDES']['dat'][0, 0]][0, 0]


def _etay(B_spect=20.35):
    # Theoretical dispersion
    # etay0=-62e-3
    # etay = etay0 * (B_spect/20.35) * (9.28/10.33)

    # My calibrated dispersion
    etaym = -23.94e-3
    etay  = etaym

    return etay


def _yc(y0, etay, res):
    _checkres(res)
    yc = -y0 - etay/res
    return yc


def _checkres(res):
    if res > 1:
        raise ValueError('Resolution should be on the order of 1e-6. res={} given.'.format(res))
