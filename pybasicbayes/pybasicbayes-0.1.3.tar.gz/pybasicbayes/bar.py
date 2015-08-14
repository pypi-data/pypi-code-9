from __future__ import division
import numpy as np
import numpy.random as npr

from distributions import RegressionNonconj

m, n = 2, 3
N = 10000

def rand_psd(n,k=None):
    k = k if k else n
    out = npr.randn(n,k)
    return out.dot(out.T)

d = RegressionNonconj(
    M_0=np.zeros((m,n)), Sigma_0=np.eye(m*n),
    nu_0=m+1, S_0=m*np.eye(m),
    A=npr.randn(m,n), sigma=rand_psd(m))

sigma = rand_psd(m)
A = npr.randn(m,n)
x = npr.randn(N,n)
y = A.dot(x.T).T + npr.multivariate_normal(np.zeros(m), sigma, N)


print A
print sigma
print
for _ in range(3):
    d.resample(np.hstack((x,y)),niter=10)
    print d.A
    print d.sigma
    print



