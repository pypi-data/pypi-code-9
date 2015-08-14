from __future__ import division
import numpy as np
import numpy.random as npr

from distributions import RegressionFixedSigma

m, n = 2, 3
N = 10000

def rand_psd(n,k=None):
    k = k if k else n
    out = npr.randn(n,k)
    return out.dot(out.T)

sigma = rand_psd(m)
# sigma = 2*np.eye(m)

d = RegressionFixedSigma(
    M_0=np.zeros((m,n)), Sigma_0=np.eye(m*n), sigma=sigma)


A = npr.randn(m,n)
x = npr.randn(N,n)
y = A.dot(x.T).T + npr.multivariate_normal(np.zeros(m), sigma, N)


print A
for _ in range(3):
    d.resample(np.hstack((x,y)))
    print d.A

