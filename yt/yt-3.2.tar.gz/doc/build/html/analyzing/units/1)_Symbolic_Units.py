
#### Dimensional analysis

# The fastest way to get into the unit system is to explore the quantities that live in the `yt.units` namespace:

# In[ ]:

from yt.units import meter, gram, kilogram, second, joule
print kilogram*meter**2/second**2 == joule
print kilogram*meter**2/second**2


# In[ ]:

from yt.units import m, kg, s, W
kg*m**2/s**3 == W


# In[ ]:

from yt.units import kilometer
three_kilometers = 3*kilometer
print three_kilometers


# In[ ]:

from yt.units import gram, kilogram
print gram+kilogram

print kilogram+gram

print kilogram/gram


# These unit symbols are all instances of a new class we've added to yt 3.0, `YTQuantity`. `YTQuantity` is useful for storing a single data point.

# In[ ]:

type(kilogram)


# We also provide `YTArray`, which can store arrays of quantities:

# In[ ]:

arr = [3,4,5]*kilogram

print arr

print type(arr)


#### Creating arrays and quantities

# Most people will interact with the new unit system using `YTArray` and `YTQuantity`.  These are both subclasses of numpy's fast array type, `ndarray`, and can be used interchangably with other NumPy arrays. These new classes make use of the unit system to append unit metadata to the underlying `ndarray`.  `YTArray` is intended to store array data, while `YTQuantitity` is intended to store scalars in a particular unit system.
# 
# There are two ways to create arrays and quantities. The first is to explicitly create it by calling the class constructor and supplying a unit string:

# In[ ]:

from yt.units.yt_array import YTArray

sample_array = YTArray([1,2,3], 'g/cm**3')

print sample_array


# The unit string can be an arbitrary combination of metric unit names.  Just a few examples:

# In[ ]:

from yt.units.yt_array import YTQuantity
from yt.utilities.physical_constants import kboltz
from numpy.random import random
import numpy as np

print "Length:"
print YTQuantity(random(), 'm')
print YTQuantity(random(), 'cm')
print YTQuantity(random(), 'Mpc')
print YTQuantity(random(), 'AU')
print ''

print "Time:"
print YTQuantity(random(), 's')
print YTQuantity(random(), 'min')
print YTQuantity(random(), 'hr')
print YTQuantity(random(), 'day')
print YTQuantity(random(), 'yr')
print ''

print "Mass:"
print YTQuantity(random(), 'g')
print YTQuantity(random(), 'kg')
print YTQuantity(random(), 'Msun')
print ''

print "Energy:"
print YTQuantity(random(), 'erg')
print YTQuantity(random(), 'g*cm**2/s**2')
print YTQuantity(random(), 'eV')
print YTQuantity(random(), 'J')
print ''

print "Temperature:"
print YTQuantity(random(), 'K')
print (YTQuantity(random(), 'eV')/kboltz).in_cgs()


# Dimensional arrays and quantities can also be created by multiplication with another array or quantity:

# In[ ]:

from yt.units import kilometer
print kilometer


# In[ ]:

three_kilometers = 3*kilometer
print three_kilometers


# When working with a YTArray with complicated units, you can use `unit_array` and `unit_quantity` to conveniently apply units to data:

# In[ ]:

test_array = YTArray(np.random.random(20), 'erg/s')

print test_array


# `unit_quantity` returns a `YTQuantity` with a value of 1.0 and the same units as the array it is a attached to.

# In[ ]:

print test_array.unit_quantity


# `unit_array` returns a `YTArray` with the same units and shape as the array it is a attached to and with all values set to 1.0.

# In[ ]:

print test_array.unit_array


# These are useful when doing arithmetic:

# In[ ]:

print test_array + 1.0*test_array.unit_quantity


# In[ ]:

print test_array + np.arange(20)*test_array.unit_array


# For convenience, `unit_quantity` is also available via `uq` and `unit_array` is available via `ua`.  You can use these arrays to create dummy arrays with the same units as another array - this is sometimes easier than manually creating a new array or quantity.

# In[ ]:

print test_array.uq

print test_array.unit_quantity == test_array.uq


# In[ ]:

from numpy import array_equal

print test_array.ua

print array_equal(test_array.ua, test_array.unit_array)


# Unit metadata is encoded in the `units` attribute that hangs off of `YTArray` or `YTQuantity` instances:

# In[ ]:

from yt.units import kilometer, erg

print "kilometer's units:", kilometer.units
print "kilometer's dimensions:", kilometer.units.dimensions

print ''

print "erg's units:", erg.units
print "erg's dimensions: ", erg.units.dimensions


#### Arithmetic with `YTQuantity` and `YTArray`

# Of course it wouldn't be very useful if all we could do is create data with units.  The real power of the new unit system is that we can add, subtract, mutliply, and divide using quantities and dimensional arrays:

# In[ ]:

a = YTQuantity(3, 'cm')
b = YTQuantity(3, 'm')

print a+b
print b+a
print ''

print (a+b).in_units('ft')


# In[ ]:

a = YTQuantity(42, 'mm')
b = YTQuantity(1, 's')

print a/b
print (a/b).in_cgs()
print (a/b).in_mks()
print (a/b).in_units('km/s')
print ''

print a*b
print (a*b).in_cgs()
print (a*b).in_mks()


# In[ ]:

m = YTQuantity(35, 'g')
a = YTQuantity(9.8, 'm/s**2')

print m*a
print (m*a).in_units('dyne')


# In[ ]:

from yt.utilities.physical_constants import G, kboltz

print "Newton's constant: ", G
print "Newton's constant in MKS: ", G.in_mks(), "\n"

print "Boltzmann constant: ", kboltz
print "Boltzmann constant in MKS: ", kboltz.in_mks()


# In[ ]:

rho = YTQuantity(1, 'g/cm**3')
t_ff = (G*rho)**(-0.5)

print t_ff


# An exception is raised if we try to do a unit operation that doesn't make any sense:

# In[ ]:

from yt.utilities.exceptions import YTUnitOperationError

a = YTQuantity(3, 'm')
b = YTQuantity(5, 'erg')

try:
    print a+b
except YTUnitOperationError as e:
    print e


# A plain `ndarray` or a `YTArray` created with empty units is treated as a dimensionless quantity and can be used in situations where unit consistency allows it to be used: 

# In[ ]:

a = YTArray([1.,2.,3.], 'm')
b = np.array([2.,2.,2.])

print "a:   ", a
print "b:   ", b
print "a*b: ", a*b


# In[ ]:

c = YTArray([2,2,2])

print "c:    ", c
print "a*c:  ", a*c

