#!/usr/bin/env python
#-*- coding: utf-8
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
lambdas = [4, 10, 20]
colors = ['r-', 'b-', 'g-']
fig = plt.figure()
fig.suptitle('Poisson Distribution', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
for mu, ls in zip(lambdas, colors):
    dist = stats.poisson(mu)
    x = np.arange(0, 50)
    
    plt.plot(x, dist.pmf(x), ls, label = str(mu))
plt.xlim(0, 30)
plt.ylim(0, 0.3)
plt.xlabel('$x$', fontsize = 15)
plt.ylabel(r'$p(x|\mu)$', fontsize = 15)
plt.legend(loc = "upper right")
plt.show()