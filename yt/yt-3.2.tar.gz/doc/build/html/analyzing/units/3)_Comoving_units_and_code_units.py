
# In yt 3.0, we want to make it easier to access "raw" simulation data that a code writes directly to disk. The new unit system makes it much simpler to convert back and forth between phsical coordinates and the unscaled "raw" coordinate system used internally in the simulation code.  In some cases, this conversion involves transforming to comoving coordinates, so that is also covered here.

#### Code units

# Let's take a look at a cosmological enzo dataset to play with converting between physical units and code units:

# In[ ]:

import yt
ds = yt.load('Enzo_64/DD0043/data0043')


# The conversion factors between Enzo's internal unit system and the physical CGS system are stored in the dataset's `unit_registry` object.  Code units have names like `code_length` and `code_time`. Let's take a look at the names of all of the code units, along with their CGS conversion factors for this cosmological enzo dataset:

# In[ ]:

reg = ds.unit_registry

for un in reg.keys():
    if un.startswith('code_'):
        fmt_tup = (un, reg.lut[un][0], reg.lut[un][1])
        print "Unit name:      {:<15}\nCGS conversion: {:<15}\nDimensions:     {:<15}\n".format(*fmt_tup)


# Most of the time you will not have to deal with the unit registry.  For example, the conversion factors to code units are stored as attributes of the dataset object:

# In[ ]:

print "Length unit: ", ds.length_unit
print "Time unit: ", ds.time_unit
print "Mass unit: ", ds.mass_unit
print "Velocity unit: ", ds.velocity_unit


# Conversion factors will be supplied in CGS by default.  We can also ask what the conversion factors are in code units.

# In[ ]:

print "Length unit: ", ds.length_unit.in_units('code_length')
print "Time unit: ", ds.time_unit.in_units('code_time')
print "Mass unit: ", ds.mass_unit.in_units('code_mass')
print "Velocity unit: ", ds.velocity_unit.in_units('code_velocity')


# as expected, all the conversion factors are unity in code units.

# We can also play with unit conversions on `ds.domain_width`.  First, we see for enzo how code length units are defined relative to the domain width:

# In[ ]:

ds.domain_width


# In[ ]:

ds.domain_width.in_cgs()


# In[ ]:

ds.domain_width.in_units('Mpccm/h')


#### Comoving units

# This last example uses a cosmological unit.  In english, I asked for the domain width in comoving megaparsecs, scaled as if the hubble constant were 100 km/s/Mpc.  Although $h$ isn't really a unit, yt treats it as one for the purposes of the unit system.  
# 
# As an aside, Darren Croton's [research note](http://arxiv.org/abs/1308.4150) on the history, use, and interpretation of $h$ as it appears in the astronomical literature is pretty much required reading for anyone who has to deal with factors of $h$ every now and then.
# 
# In yt, comoving length unit symbols are named following the pattern “(length symbol)cm”, i.e. `pccm` for comoving parsec or `mcm` for a comoving meter.  A comoving length unit is different from the normal length unit by a factor of $(1+z)$:

# In[ ]:

z = ds.current_redshift
 
print ds.quan(1, 'Mpc')/ds.quan(1, 'Mpccm')
print (1+z)


# As we saw before, $h$ is treated like any other unit symbol. It has `dimensionless` units, just like a scalar:

# In[ ]:

print ds.quan(1, 'Mpc')/ds.quan(1, 'Mpc/h')
print ds.hubble_constant


# These units can be used in readily used in plots and anywhere a length unit is appropriate in yt.

# In[ ]:

slc = yt.SlicePlot(ds, 0, 'density', width=(128, 'Mpccm/h'))
slc.set_figure_size(6)


#### The unit registry

# When you create a `YTArray` without referring to a unit registry, yt uses the default unit registry, which does not include code units or comoving units.

# In[ ]:

from yt import YTQuantity

a = YTQuantity(3, 'cm')

print a.units.registry.keys()


# When a dataset is loaded, yt infers conversion factors from the internal simulation unit system to the CGS unit system.  These conversion factors are stored in a `unit_registry` along with conversion factors to the other known unit symbols.  For the cosmological Enzo dataset we loaded earlier, we can see there are a number of additional unit symbols not defined in the default unit lookup table:

# In[ ]:

print sorted([k for k in ds.unit_registry.keys() if k not in a.units.registry.keys()])


# Since code units do not appear in the default unit symbol lookup table, one must explicitly refer to a unit registry when creating a `YTArray` to be able to convert to the unit system of a simulation.

# To make this as clean as possible, there are array and quantity-creating convenience functions attached to the `Dataset` object:
# 
# * `ds.arr()`
# * `ds.quan()`
# 
# These functions make it straightforward to create arrays and quantities that can be converted to code units or comoving units.  For example:

# In[ ]:

a = ds.quan(3, 'code_length')

print a
print a.in_cgs()
print a.in_units('Mpccm/h')


# In[ ]:

b = ds.arr([3, 4, 5], 'Mpccm/h')
print b
print b.in_cgs()

