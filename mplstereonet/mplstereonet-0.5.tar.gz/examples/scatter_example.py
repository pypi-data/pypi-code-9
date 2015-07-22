"""Plot plunge, bearings along with a third attribute displayed as color."""
import matplotlib.pyplot as plt
import numpy as np
import mplstereonet
from scipy.interpolate import Rbf

# In this case, we have separate sequences
plunges = 20, 10, 70, 50
bearings = 210, 40, 20, 315
z = 3, 4, 1, 2

# For this plot, we need to use ``scatter``, which requires "native" x and y
# coordinates. Therefore, we'll convert our measurements to "stereonet coords".
x, y = mplstereonet.line(plunges, bearings)

fig, ax = mplstereonet.subplots()

yi, xi = np.mgrid[-np.pi:np.pi:50j, -np.pi:np.pi:50j]
interp = Rbf(x, y, z)
zi = interp(xi.ravel(), yi.ravel())
zi = zi.reshape(xi.shape)
ax.contourf(xi, yi, zi)

ax.scatter(x, y, c=z, s=100)

ax.grid(True)
ax.set_azimuth_ticks([])

fig, ax = plt.subplots()
ax.imshow(zi)
plt.show()


