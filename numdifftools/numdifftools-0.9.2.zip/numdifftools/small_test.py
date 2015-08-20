# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:42:50 2015

@author: pab
"""
from __future__ import print_function
from matplotlib import pyplot as plt
import numdifftools.nd_cstep as nd
from numdifftools.test_functions import function_names

num_extrap = 0
method = 'central'
for name in function_names[3:4]:
    for n in range(1, 5):
        if method != 'complex':
            num_steps = n + 1 + num_extrap
            if method == 'central':
                num_steps = (n+1) // 2 + num_extrap
        else:
            num_steps = 1 + num_extrap
        step_ratio = 2  # 4**(1./n),
        epsilon = nd.StepsGenerator(num_steps=num_steps,
                                 step_ratio=step_ratio,
                                 offset=0, use_exact_steps=True)
        plt.figure()
        nd._example3(x=0.5, fun_name=name, epsilon=epsilon, method=method,
                  scale=None, n=n)
plt.show('hold')