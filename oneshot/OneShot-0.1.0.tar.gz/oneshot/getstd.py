import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np


# Get std dev (spot size) {{{
def getstd(res, h, xval):
    """
    .. deprecated:: 0.0.0

    I'm not really sure what this function does, but it's not referenced anywhere else.
    """
    stddevsq  = _np.zeros(res)
    indivbool = False
    if indivbool:
        figscan = plt.figure()  # noqa
    
    def gauss(x, A, mu, sig):
        return A*_np.exp(-_np.power(x-mu, 2)/(2*_np.power(sig, 2)))
    
    for i, row in enumerate(_np.transpose(h)):
        # A = max(row)
        mean = _np.sum(xval*row)/row.sum()
        var = _np.sum(_np.power(xval-mean, 2)*row)/row.sum()
        # root = _np.sqrt(var)
        # pguess = [A, mean, root]
        # popt = pguess
        # popt, pcov = spopt.curve_fit(gauss, xval, row, pguess)
        # # print "A: {}, mean: {}, sig: {}".format(popt[0], popt[1], popt[2])
        # # print "Percent diff: {}%".format(100*(popt[2]-root)/root)
        # fit = gauss(xval, popt[0], popt[1], popt[2])
        # unchangedroot = gauss(xval, popt[0], popt[1], root)
        # if indivbool: plt.plot(xval, row, xval, fit, xval, unchangedroot)
    
        # # plt.plot(xval, row)
        # if indivbool: raw_input("Any key.")
        # if indivbool: figscan.clf()
        # # stddevsq[i] = _np.power(popt[2], 2)
        stddevsq[i] = var
    
    # stddev=_np.sqrt(stddevsq)
    return stddevsq
# }}}
