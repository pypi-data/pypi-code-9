import numpy as _np
import scisalt as _ss


def fitimage(img, res, n_rows=None):
    """
    Fits Gaussians to the beam distribution in slices.
    """
    # ======================================
    # Interprets resolution
    # ======================================
    if _np.size(res) == 2:
        res_x, res_y = res
    elif _np.size(res) == 1:
        res_x = res
        res_y = res
    else:
        raise ValueError('Improper value for argument res: {}'.format(res))

    # ======================================
    # If not specified, n_rows is the #
    # of y pixels in the image
    # ======================================
    if n_rows is None:
        n_rows = img.shape[1]

    # ======================================
    # Slice into rows
    # ======================================
    hist_vec  = _ss.linspacestep(0, img.shape[1], n_rows)
    n_groups  = _np.size(hist_vec)
    x_pix     = _np.round(_ss.numpy.linspacestep(0, img.shape[0], 1))
    x_meter   = (x_pix - _np.mean(x_pix)) * res_x

    # ======================================
    # Initialize arrays for results
    # ======================================
    variance     = _np.zeros(n_groups)
    gaussresults = _np.empty(n_groups, object)
    # y            = _np.array([])

    for i in _ss.numpy.linspacestep(0, n_groups-1):
        # ======================================
        # Sum up a group
        # ======================================
        sum_x = _np.sum(img[:, i*n_rows:(i+1)*n_rows], 1)
        # y     = np.append(y, ystart+n_rows*i+(n_rows-1.)/2.)

        # ======================================
        # Fit single group
        # ======================================
        gaussresults[i] = _ss.numpy.GaussResults(x_meter, sum_x, sigma_y=_np.sqrt(sum_x), variance=True, background=True)
        variance[i]     = gaussresults[i].popt[2]

    # ======================================
    # Remove nan from arrays
    # ======================================
    nan_ind   = _np.logical_not(_np.isnan(variance))
    variance  = variance[nan_ind]
    gaussresults = gaussresults[nan_ind]
    # y         = y[nan_ind]

    return gaussresults, variance


def temp():
    # ======================================
    # Default Twiss and beam params
    # ======================================
    emitx  = 0.001363/gamma
    # betax  = 1
    # alphax = 0
    # gammax = (1+np.power(alphax, 2))/betax
    twiss    = sltr.BeamParams(
        beta  = 0.5,
        alpha = 0,
        emit  = emitx
        )

    # ======================================
    # Quadrupole values
    # ======================================
    QS1_K1 = setQS.QS1.K1
    QS2_K1 = setQS.QS2.K1

    logger.log(level=loggerlevel, msg='QS1_K1 is: {}'.format(QS1_K1))
    logger.log(level=loggerlevel, msg='QS2_K1 is: {}'.format(QS2_K1))

    # ======================================
    # Create beamlines
    # ======================================
    # beamline=bt.beamlines.IP_to_cherfar(twiss_x=twiss, twiss_y=twiss, gamma=gamma)
    if camname == 'ELANEX':
        beamline = bt.beamlines.IP_to_lanex(
            beam_x = twiss, beam_y=twiss,
            QS1_K1 = QS1_K1,
            QS2_K1 = QS2_K1
            )
        #  from PyQt4.QtCore import pyqtRemoveInputHook
        #  pyqtRemoveInputHook()
        #  pdb.set_trace()
    else:
        beamline = bt.beamlines.IP_to_cherfar(
            beam_x=twiss, beam_y=twiss,
            QS1_K1 = QS1_K1,
            QS2_K1 = QS2_K1
            )

    beamline_array = np.array([])
    for i, value in enumerate(eaxis):
        # beamline.gamma = value/5.109989e-4
        beamline.gamma = sltr.GeV2gamma(value)
        beamline_array = np.append(beamline_array, copy.deepcopy(beamline))
    
    # ======================================
    # Fudge error
    # ======================================
    chisq_factor = 1e-28
    # used_error   = stddev*np.sqrt(chisq_factor)
    used_error   = variance*np.sqrt(chisq_factor)

    # ======================================
    # Fit beamline scan
    # ======================================
    scanresults = bt.fitBeamlineScan(beamline_array,
            variance,
            # emitx,
            error=used_error,
            verbose=True,
            plot=False,
            eaxis=eaxis
            )
