import numpy as _np

def linspacestep(start,stop,step=1):
	# Find an integer number of steps
	numsteps = _np.int((stop-start)/step)
	# Do a linspace over the new range
	# that has the correct endpoint
	return _np.linspace(start,start+step*numsteps,numsteps+1)
