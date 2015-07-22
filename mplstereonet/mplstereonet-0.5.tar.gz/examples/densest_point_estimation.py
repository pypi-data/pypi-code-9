"""A basic example of producing a density contour plot of poles to planes."""
import matplotlib.pyplot as plt
import numpy as np
import mplstereonet

fig, ax = mplstereonet.subplots()

# Generate a random scatter of planes around the given plane
strike, dip = 90, 80 
num = 10
strikes = strike + 10 * np.random.randn(num)
dips = dip + 10 * np.random.randn(num)

# Estimate the point density on a regular grid.
lon, lat, density = mplstereonet.density_grid(strikes, dips)

# Find index of "densest" point
i, j = np.unravel_index(density.argmax(), density.shape)

# Plot the grid (these steps are basically what "density_contour" does)
ax.contourf(lon, lat, density)

# Plot the pole
ax.plot(lon[i,j], lat[i,j], 'ko')

# Plot a plane
strike, dip = mplstereonet.geographic2pole(lon[i,j], lat[i,j])
ax.plane(strike, dip)

plt.show()
