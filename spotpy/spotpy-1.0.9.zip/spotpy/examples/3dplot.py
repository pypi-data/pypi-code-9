'''
Copyright 2015 by Tobias Houska
This file is part of Statistical Parameter Estimation Tool (SPOTPY).

:author: Tobias Houska

This file shows how to make 3d surface plots.
'''
import spot

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from numpy import *


fig = plt.figure()
ax = fig.gca(projection='3d')
#
# Plot Rosenbrock surface
X = arange(-50, 50, 0.1)
Y = arange(-50, 50, 0.1)
X, Y = meshgrid(X, Y)

#from spot_setup_rosenbrock import spot_setup
from spot_setup_griewank import spot_setup
#from spot_setup_ackley import spot_setup

Z = np.zeros(X.shape)
for i in xrange(X.shape[0]):
    for j in xrange(X.shape[1]):
        sim=spot_setup().simulation([X[i,j],Y[i,j]])
        like=bcf.likelihoods.rmse(sim,[0])
        Z[i,j] = like


surf_Rosen = ax.plot_surface(X, Y, Z,rstride=5,linewidth=0, cmap=cm.rainbow)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('RMSE')



#surf_Rosen = ax.plot_surface(X_Rosen, Y_Rosen, Z_Rosen, rstride=1, cstride=1,
#   cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha = 0.3)

# Adjust axes
#ax.set_zlim(0, 600)
#ax.zaxis.set_major_locator(LinearLocator(5))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))

# Report minimum
#print 'Minimum location', v0_ori, '\nMinimum value', Rosenbrock(v0_ori), '\nNumber of function evaluations', f_evals

# Render plot
plt.show()