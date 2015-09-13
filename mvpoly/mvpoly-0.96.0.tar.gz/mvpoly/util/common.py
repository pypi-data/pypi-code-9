import numpy as np


def kronn(b, c, *args) :
    """
    A version of :func:`numpy.kron` which takes an arbitrary
    number of arguments.
    """
    a = np.kron(b, c)
    for d in args :
        a = np.kron(a, d)
    return a


def max_or_default(iterable, default) :
    """
    Like :func:`max`, but returns a default value if the
    iterable is empty.
    """
    try :
        return max(iterable)
    except ValueError :
        return default


def binom(n, r) :
    """
    Returns the binomial coefficient as a long integer.
    """
    assert n >= 0
    assert 0 <= r <= n
    c = 1
    denom = 1
    for (num, denom) in zip(range(n, n - r, -1), range(1, r + 1, 1)) :
        c = (c * num) // denom
    return c


def as_numpy_scalar(x) :
    """
    Returns a :class:`numpy` scalar.
    """
    return np.array(x).dtype.type(x)


def monomial_indices(n, k) :
    """
    A generator which yields tuples of exponents of *n*-variate
    monomials up to order *k*.
    """
    def mono_ind_next(n, L, k) :
        j = next((i + 1 for i, x in enumerate(L[1:]) if x != 0), 0)
        if j == 0:
            if L[0] == k:
                return None
            t = L[0]
            L[0] = 0
            L[-1] = t + 1
        elif j < n - 1:
            L[j] -= 1
            t = L[0] + 1
            L[0] = 0
            L[j - 1] += t
        else:
            t = L[0]
            L[0] = 0
            L[j - 1] = t + 1
            L[j] -= 1
        return L

    if n < 1:
        raise ValueError('must have at least 1 variable (%i given)' % n)
    if k < 0:
        raise ValueError('order cannot be negative (%i given)' % k)
    L = [0] * n
    while L:
        yield tuple(reversed(L))
        L = mono_ind_next(n, L, k)
