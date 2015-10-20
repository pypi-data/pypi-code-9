# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

import numpy as np
from .nleq2 import nleq2


def solve(func, jacfunc, guess, maxiter=100):
    """
    Solves a system of nonlinear equations using the NLEQ2 Fortran code

    Parameters
    ----------
    func: callback
        signature (xvector, ifail) -> (fvector, ifail)
    jacfunc: callback
        signature
    """

    guess = np.asarray(guess, dtype=np.float64)
    x0 = guess.copy()
    s_scale = guess.copy()

    N = len(x0)
    iwk = np.zeros((N+52), 'i')
    rwk_len = N*(N + max(N, 10) + 15) + 61
    rwk = np.zeros(rwk_len, 'd')
    iopt = np.zeros(50, 'i')

    rtol = np.finfo(np.float64).eps*10*N
    iopt[2] = 1  # User supplied jacobian
    iopt[11] = 6
    iopt[13] = 6
    iopt[15] = 6
    iopt[30] = 4
    iopt[31] = 1

    iwk[30] = maxiter

    ierr = 0

    idx = 0
    while True:
        res, s_scale, rtol, iopt, ierr = nleq2(func, jacfunc, x0, s_scale,
                                               rtol, iopt, iwk, rwk)
        if ierr == 0:
            break  # success
        elif ierr == 21:
            print('negative rtol')
            break
        elif ierr == 2:
            print('nitmax reached')
            break
        idx += 1
    return res, ierr
