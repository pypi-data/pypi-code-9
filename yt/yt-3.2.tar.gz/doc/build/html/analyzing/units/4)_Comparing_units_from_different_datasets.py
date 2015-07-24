
# Units that refer to the internal simulation coordinate system will have different CGS conversion factors in different datasets.  Depending on how a unit system is implemented, this could add an element of uncertainty when we compare dimensional arrays instances produced by different unit systems.  Fortunately, this is not a problem for `YTArray` since all `YTArray` unit systems are defined in terms of physical CGS units.
# 
# As an example, let's load up two enzo datasets from different redshifts in the same cosmology simulation.

# In[ ]:

# A high redshift output from z ~ 8
import yt

ds1 = yt.load('Enzo_64/DD0002/data0002')
print "z = %s" % ds1.current_redshift
print "Internal length units = %s" % ds1.length_unit
print "Internal length units in cgs = %s" % ds1.length_unit.in_cgs()


# In[ ]:

# A low redshift output from z ~ 0
ds2 = yt.load('Enzo_64/DD0043/data0043')
print "z = %s" % ds2.current_redshift
print "Internal length units = %s" % ds2.length_unit
print "Internal length units in cgs = %s" % ds2.length_unit.in_cgs()


# Given that these are from the same simulation in comoving units, the CGS length units are different by a factor of $(1+z_1)/(1+z_2)$:

# In[ ]:

print ds2.length_unit.in_cgs()/ds1.length_unit.in_cgs() == (1+ds1.current_redshift)/(1+ds2.current_redshift)


# It's not necessary to convert to CGS units either.  yt will automatically account for the fact that a comoving megapaersec in the first output is physically different compared to a comoving megaparsec in the second output.

# In[ ]:

print ds2.length_unit/ds1.length_unit


# Time series analysis is also straightforward.  Since dimensional arrays and quantities carry around the conversion factors to CGS with them, we can safely pickle them, share them with other processors, or combine them without worrying about differences in unit definitions.
# 
# The following snippet, which iterates over a time series and saves the `length_unit` quantity to a storage dictionary. This should work correctly on one core or in a script run in parallel.

# In[ ]:

import yt
yt.enable_parallelism()

ts = yt.load("Enzo_64/DD????/data????")

storage = {}

for sto, ds in ts.piter(storage=storage):
    sto.result_id = ds.current_time
    sto.result = ds.length_unit

if yt.is_root():
    for t in sorted(storage.keys()):
        print t.in_units('Gyr'), storage[t].in_units('Mpc')

