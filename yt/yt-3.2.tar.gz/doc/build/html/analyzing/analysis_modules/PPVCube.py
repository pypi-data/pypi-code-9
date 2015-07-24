
# Detailed spectra of astrophysical objects sometimes allow for determinations of how much of the gas is moving with a certain velocity along the line of sight, thanks to Doppler shifting of spectral lines. This enables "data cubes" to be created in RA, Dec, and line-of-sight velocity space. In yt, we can use the `PPVCube` analysis module to project fields along a given line of sight traveling at different line-of-sight velocities, to "mock-up" what would be seen in observations.

# In[ ]:

import yt
import numpy as np

from yt.analysis_modules.ppv_cube.api import PPVCube


# To demonstrate this functionality, we'll create a simple unigrid dataset from scratch of a rotating disk galaxy. We create a thin disk in the x-y midplane of the domain of three cells in height in either direction, and a radius of 10 kpc. The density and azimuthal velocity profiles of the disk as a function of radius will be given by the following functions:

# Density: $\rho(r) \propto r^{\alpha}$

# Velocity: $v_{\theta}(r) \propto \frac{r}{1+(r/r_0)^{\beta}}$

# where for simplicity we won't worry about the normalizations of these profiles. 

# First, we'll set up the grid and the parameters of the profiles:

# In[ ]:

nx,ny,nz = (256,256,256) # domain dimensions
R = 10. # outer radius of disk, kpc
r_0 = 3. # scale radius, kpc
beta = 1.4 # for the tangential velocity profile
alpha = -1. # for the radial density profile
x, y = np.mgrid[-R:R:nx*1j,-R:R:ny*1j] # cartesian coordinates of x-y plane of disk
r = np.sqrt(x*x+y*y) # polar coordinates
theta = np.arctan2(y, x) # polar coordinates


# Second, we'll construct the data arrays for the density and the velocity of the disk. Since we have the tangential velocity profile, we have to use the polar coordinates we derived earlier to compute `velx` and `vely`. Everywhere outside the disk, all fields are set to zero.  

# In[ ]:

dens = np.zeros((nx,ny,nz))
dens[:,:,nz/2-3:nz/2+3] = (r**alpha).reshape(nx,ny,1) # the density profile of the disk
vel_theta = r/(1.+(r/r_0)**beta) # the azimuthal velocity profile of the disk
velx = np.zeros((nx,ny,nz))
vely = np.zeros((nx,ny,nz))
velx[:,:,nz/2-3:nz/2+3] = (-vel_theta*np.sin(theta)).reshape(nx,ny,1) # convert polar to cartesian
vely[:,:,nz/2-3:nz/2+3] = (vel_theta*np.cos(theta)).reshape(nx,ny,1) # convert polar to cartesian
dens[r > R] = 0.0
velx[r > R] = 0.0
vely[r > R] = 0.0


# Finally, we'll package these data arrays up into a dictionary, which will then be shipped off to `load_uniform_grid`. We'll define the width of the grid to be `2*R` kpc, which will be equal to 1  `code_length`. 

# In[ ]:

data = {}
data["density"] = (dens,"g/cm**3")
data["velocity_x"] = (velx, "km/s")
data["velocity_y"] = (vely, "km/s")
data["velocity_z"] = (np.zeros((nx,ny,nz)), "km/s") # zero velocity in the z-direction
bbox = np.array([[-0.5,0.5],[-0.5,0.5],[-0.5,0.5]]) # bbox of width 1 on a side with center (0,0,0)
ds = yt.load_uniform_grid(data, (nx,ny,nz), length_unit=(2*R,"kpc"), nprocs=1, bbox=bbox)


# To get a sense of what the data looks like, we'll take a slice through the middle of the disk:

# In[ ]:

slc = yt.SlicePlot(ds, "z", ["density","velocity_x","velocity_y","velocity_magnitude"])


# In[ ]:

slc.set_log("velocity_x", False)
slc.set_log("velocity_y", False)
slc.set_log("velocity_magnitude", False)
slc.set_unit("velocity_magnitude", "km/s")
slc.show()


# Which shows a rotating disk with a specific density and velocity profile. Now, suppose we wanted to look at this disk galaxy from a certain orientation angle, and simulate a 3D FITS data cube where we can see the gas that is emitting at different velocities along the line of sight. We can do this using the `PPVCube` class. First, let's assume we rotate our viewing angle 60 degrees from face-on, from along the z-axis into the y-axis. We'll create a normal vector:

# In[ ]:

i = 60.*np.pi/180.
L = [0.0,np.sin(i),np.sin(i)]


# Next, we need to specify a field that will serve as the "intensity" of the emission that we see. For simplicity, we'll simply choose the gas density as this field, though it could be any field (including derived fields) in principle. We also need to specify the dimensions of the data cube, and optionally we may choose the bounds in line-of-sight velocity that the data will be binned into. Otherwise, the bounds will simply be set to the negative and positive of the largest speed in the dataset.

# In[ ]:

cube = PPVCube(ds, L, "density", dims=(200,100,50), velocity_bounds=(-1.5,1.5,"km/s"))


# Following this, we can now write this cube to a FITS file:

# In[ ]:

cube.write_fits("cube.fits", clobber=True, length_unit=(5.0,"deg"))


# Now, we'll look at the FITS dataset in yt and look at different slices along the velocity axis, which is the "z" axis:

# In[ ]:

ds = yt.load("cube.fits")


# In[ ]:

# Specifying no center gives us the center slice
slc = yt.SlicePlot(ds, "z", ["density"])
slc.show()


# In[ ]:

import yt.units as u
# Picking different velocities for the slices
new_center = ds.domain_center
new_center[2] = ds.spec2pixel(-1.0*u.km/u.s)
slc = yt.SlicePlot(ds, "z", ["density"], center=new_center)
slc.show()


# In[ ]:

new_center[2] = ds.spec2pixel(0.7*u.km/u.s)
slc = yt.SlicePlot(ds, "z", ["density"], center=new_center)
slc.show()


# In[ ]:

new_center[2] = ds.spec2pixel(-0.3*u.km/u.s)
slc = yt.SlicePlot(ds, "z", ["density"], center=new_center)
slc.show()


# If we project all the emission at all the different velocities along the z-axis, we recover the entire disk:

# In[ ]:

prj = yt.ProjectionPlot(ds, "z", ["density"], proj_style="sum")
prj.set_log("density", True)
prj.set_zlim("density", 1.0e-3, 0.2)
prj.show()

