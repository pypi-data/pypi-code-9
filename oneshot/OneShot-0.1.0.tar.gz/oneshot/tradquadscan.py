import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np
import copy
import collections as col
import scisalt.scipy as ssc


# Fit bowtie {{{
def tradquadscan(beamline, y, twiss, emitx, error=None, verbose=False):
    """
    .. deprecated:: 0.0.0

    I'm not really sure what this function does, but it's not referenced anywhere else.
    """
    # beamline_manip = copy.deepcopy(beamline)
    numsteps = beamline.size
    betax          = twiss.beta
    alphax         = twiss.alpha
    gammax         = twiss.gamma
    y              = y[_np.newaxis]
    # gamma          = (1+x)*40000
    X              = _np.zeros([numsteps, 3])
    spotexpected   = _np.zeros(numsteps)
    R              = _np.zeros([6, 6, numsteps])
    betaf          = _np.zeros(numsteps)
    
    for i, bl in enumerate(beamline):
        R11             = bl.R[0, 0]
        R12             = bl.R[0, 1]
        R[:, :, i]        = bl.R
        X[i, 0]          = R11*R11
        X[i, 1]          = 2*R11*R12
        X[i, 2]          = R12*R12
        T2              = _np.dot(_np.dot(R[0:2, 0:2, i], twiss.T), _np.transpose(R[0:2, 0:2, i]))
        betaf[i]        = T2[0, 0]
        spotexpected[i] = _np.sqrt((R11*R11*betax - 2*R11*R12*alphax + R12*R12*gammax)*emitx)
    
    if verbose:
        # mt.figure('Expected')
        # xax=_np.linspace(1, numsteps, numsteps)
        # plt.plot(xax, _np.sqrt(y.transpose()), xax, spotexpected)
        # plt.show()
        pass

    # beta is the best solution of beam parameters:
    # sig^2 = R11^2 <x^2> + 2 R11 R12 <xx'> + R12^2 <x'^2>
    # beta[0, 0] = <x^2>
    # beta[1, 0] = <xx'>
    # beta[2, 0] = <x'^2>

    X_unweighted = copy.deepcopy(X)
    # if ( False ):
    if error is not None:
        for i, el in enumerate(X):
            X[i, :] = el/error[i]
        y_err = y/error

    # This is the linear least squares matrix formalism
    y_err = y_err.transpose()
    beta  = _np.dot(_np.linalg.pinv(X) , y_err)
    covar = _np.linalg.inv(_np.dot(_np.transpose(X), X))
    
    emit = _np.sqrt( beta[0, 0] * beta[2, 0] - _np.square(beta[1, 0]) )
    del_emit_sq = _np.power(1/(2*emit), 2) * \
        (
            _np.power(beta[2, 0] * covar[0, 0]   , 2) +
            _np.power(2*beta[1, 0] * covar[1, 1] , 2) +
            _np.power(beta[0, 0] * covar[2, 2]   , 2)  # +
            # 2 * (-beta[2, 0] * 2 * beta[1, 0]) * covar[0, 1] +
            # 2 * (beta[2, 0] * beta[0, 0]) * covar[0, 2] +
            # 2 * (-2*beta[1, 0] * beta[0, 0]) * covar[1, 2]
        )

    chisq_red = ssc.chisquare(y.transpose(), _np.dot(X_unweighted, beta), error, ddof=3, verbose=verbose)

    if verbose:
        print('Emittance error is:\t\t{}.'.format(_np.sqrt(del_emit_sq)))
        beta0 = beta[0, 0]/emit
        gamma0 = beta[2, 0]/emit
        alpha0 = -_np.sign(beta[1, 0])*_np.sqrt(beta0*gamma0-1)
        print('Emittance fit:\t\t\t{}.'.format(emit))
        print('Normalized emittance fit:\t{}.'.format(emit*40000))
        print('Initial beta fit:\t\t{}.'.format(beta0))
        print('Initial alpha fit:\t\t{}.'.format(alpha0))
        print('Initial gamma fit:\t\t{}.'.format(gamma0))
        print('Initial spot from fit:\t\t{}.'.format(_np.sqrt(beta[0, 0])))

    output = col.namedtuple('fitbowtie_output', ['spotexpected', 'X', 'X_unweighted', 'beta', 'covar', 'chisq_red'])
    out = output(spotexpected, X, X_unweighted, beta, covar, chisq_red)

    return out
# }}}
