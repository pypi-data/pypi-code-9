
# In the past, querying a data object with a field name returned a NumPy `ndarray` . In the new unit system, data object queries will return a `YTArray`, a subclass of `ndarray` that preserves all of the nice properties of `ndarray`, including broadcasting, deep and shallow copies, and views. 

#### Selecting data from an object

# `YTArray` is 'unit-aware'.  Let's show how this works in practice using a sample Enzo dataset:

# In[ ]:

import yt
ds = yt.load('IsolatedGalaxy/galaxy0030/galaxy0030')
          
dd = ds.all_data()
maxval, maxloc = ds.find_max('density')

dens = dd['density']


# In[ ]:

print maxval


# In[ ]:

print dens


# In[ ]:

mass = dd['cell_mass']

print "Cell Masses in CGS: \n", mass, "\n"
print "Cell Masses in MKS: \n", mass.in_mks(), "\n"
print "Cell Masses in Solar Masses: \n", mass.in_units('Msun'), "\n"
print "Cell Masses in code units: \n", mass.in_units('code_mass'), "\n"


# In[ ]:

dx = dd['dx']
print "Cell dx in code units: \n", dx, "\n"
print "Cell dx in centimeters: \n", dx.in_cgs(), "\n"
print "Cell dx in meters: \n", dx.in_units('m'), "\n"
print "Cell dx in megaparsecs: \n", dx.in_units('Mpc'), "\n"


#### Unit conversions

# YTArray defines several user-visible member functions that allow data to be converted from one unit system to another:
# 
# * `in_units`
# * `in_cgs`
# * `in_mks`
# * `convert_to_units`
# * `convert_to_cgs`
# * `convert_to_mks`

# The first method, `in_units`, returns a copy of the array in the units denoted by a string argument:

# In[ ]:

print dd['density'].in_units('Msun/pc**3')


# `in_cgs` and `in_mks` return a copy of the array converted CGS and MKS units, respectively:

# In[ ]:

print (dd['pressure'])
print (dd['pressure']).in_cgs()
print (dd['pressure']).in_mks()


# The next two methods do in-place conversions:

# In[ ]:

dens = dd['density']
print dens

dens.convert_to_units('Msun/pc**3')
print dens


# One possibly confusing wrinkle when using in-place conversions is if you try to query `dd['density']` again, you'll find that it has been converted to solar masses per cubic parsec:

# In[ ]:

print dd['density']

dens.convert_to_units('g/cm**3')

print dens


# Since the unit metadata is preserved and the array values are still correct in the new unit system, all numerical operations will still be correct.
# 
# One of the nicest aspects of this new unit system is that the symbolic algebra for mathematical operations on data with units is performed automatically by sympy.  This example shows how we can construct a field with density units from two other fields that have units of mass and volume:

# In[ ]:

print dd['cell_mass']
print dd['cell_volume'].in_units('cm**3')

print (dd['cell_mass']/dd['cell_volume']).in_cgs()


#### Working with views and converting to ndarray

# There are two ways to convert the data into a numpy array.  The most straightforward and safe way to do this is to create a copy of the array data.  The following cell demonstrates four equivalent ways of doing this, in increasing degree of terseness.

# In[ ]:

import numpy as np

dens = dd['cell_mass']

print dens.to_ndarray()
print np.array(dens)
print dens.value
print dens.v


# Since we have a copy of the data, we can mess with it however we wish without disturbing the original data returned by the yt data object.

# Another way to touch the raw array data is to get a _view_.  A numpy view is a lightweight array interface to a memory buffer. There are four ways to create views of YTArray instances:

# In[ ]:

print dd['cell_mass'].ndarray_view()
print dd['cell_mass'].view(np.ndarray)
print dd['cell_mass'].ndview
print dd['cell_mass'].d


# When working with views, rememeber that you are touching the raw array data and no longer have any of the unit checking provided by the unit system.  This can be useful where it might be more straightforward to treat the array as if it didn't have units but without copying the data.

# In[ ]:

density_values = dd['density'].d
density_values[0:10] = 0

# The original array was updated
print dd['density']


#### Round-Trip Conversions to and from AstroPy's Units System

# Finally, a `YTArray` or `YTQuantity` may be converted to an [AstroPy quantity](http://astropy.readthedocs.org/en/latest/units/), which is a NumPy array or a scalar associated with units from AstroPy's units system. You may use this facility if you have AstroPy installed. 

# Some examples of converting from AstroPy units to yt:

# In[ ]:

from astropy import units as u
from yt import YTQuantity, YTArray

x = 42.0 * u.meter
y = YTQuantity.from_astropy(x) 


# In[ ]:

print x, type(x)
print y, type(y)


# In[ ]:

a = np.random.random(size=10) * u.km/u.s
b = YTArray.from_astropy(a)


# In[ ]:

print a, type(a)
print b, type(b)


# It also works the other way around, converting a `YTArray` or `YTQuantity` to an AstroPy quantity via the method `to_astropy`. For arrays:

# In[ ]:

temp = dd["temperature"]
atemp = temp.to_astropy()


# In[ ]:

print temp, type(temp)
print atemp, type(atemp)


# and quantities:

# In[ ]:

from yt.utilities.physical_constants import kboltz
kb = kboltz.to_astropy()


# In[ ]:

print kboltz, type(kboltz)
print kb, type(kb)


# As a sanity check, you can show that it works round-trip:

# In[ ]:

k1 = kboltz.to_astropy()
k2 = YTQuantity.from_astropy(kb)
print k1 == k2


# In[ ]:

c = YTArray.from_astropy(a)
d = c.to_astropy()
print a == d

