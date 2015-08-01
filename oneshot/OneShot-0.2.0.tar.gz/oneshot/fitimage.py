def fitimage(img, energy, beamline):
    """
    Fits Gaussians to the beam distribution in slices.
    """
    # ======================================
    # Create a histogram of std dev
    # ======================================
    hist_vec  = mt.linspacestep(ystart, ystop, n_rows)
    n_groups  = np.size(hist_vec)
    # hist_data = np.zeros([n_groups, 2])
    x_pix     = np.round(mt.linspacestep(xstart, xstop-1, 1))
    x_meter   = (x_pix-np.mean(x_pix)) * res
    if camname == 'ELANEX':
        logger.log(level=logging.INFO, msg='Lanex is tipped at 45 degrees: dividing x axis by sqrt(2)')
        x_meter = x_meter/np.sqrt(2)
    # x_sq      = x_meter**2
    
    num_pts      = n_groups
    variance     = np.zeros(num_pts)
    gaussresults = np.empty(num_pts, object)
    stddev       = np.zeros(num_pts)
    varerr       = np.zeros(num_pts)
    chisq_red    = np.zeros(num_pts)
    y            = np.array([])

    for i in mt.linspacestep(0, n_groups-1):
        sum_x = np.sum(img[:, i*n_rows:(i+1)*n_rows], 1)
        y = np.append(y, ystart+n_rows*i+(n_rows-1.)/2.)
        # popt, pcov, chisq_red[i] = mt.gaussfit(x_meter, sum_x, sigma_y=np.sqrt(sum_x), plot=False, variance_bool=True, verbose=False, background_bool=True)
        gaussresults[i] = mt.gaussfit(x_meter, sum_x, sigma_y=np.sqrt(sum_x), plot=False, variance_bool=True, verbose=False, background_bool=True)
        variance[i]         = gaussresults[i].popt[2]
        # varerr[i]           = pcov[2, 2]
        # stddev[i]           = np.sqrt(pcov[2, 2])

    # ======================================
    # Remove nan from arrays
    # ======================================
    nan_ind   = np.logical_not(np.isnan(variance))
    variance  = variance[nan_ind]
    stddev    = stddev[nan_ind]
    varerr    = varerr[nan_ind]
    chisq_red = chisq_red[nan_ind]
    y         = y[nan_ind]

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
