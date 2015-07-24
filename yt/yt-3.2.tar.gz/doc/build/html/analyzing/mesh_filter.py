
# Let us demonstrate this with an example using the same dataset as we used with the boolean masks.

# In[ ]:

import yt
ds = yt.load("Enzo_64/DD0042/data0042")


# The only argument to a cut region is a conditional on field output from a data object.  The only catch is that you *must* denote the data object in the conditional as "obj" regardless of the actual object's name.  
# 
# Here we create three new data objects which are copies of the all_data object (a region object covering the entire spatial domain of the simulation), but we've filtered on just "hot" material, the "dense" material, and the "overpressure and fast" material.

# In[ ]:

ad = ds.all_data()
hot_ad = ad.cut_region(["obj['temperature'] > 1e6"])
dense_ad = ad.cut_region(['obj["density"] > 1e-29'])
overpressure_and_fast_ad = ad.cut_region(['(obj["pressure"] > 1e-14) & (obj["velocity_magnitude"].in_units("km/s") > 1e2)'])


# Upon inspection of our "hot_ad" object, we can still get the same results as we got with the boolean masks example above:

# In[ ]:

print 'Temperature of all data: ad["temperature"] = \n%s' % ad["temperature"] 
print 'Temperature of "hot" data: hot_ad["temperature"] = \n%s' % hot_ad['temperature']


# However, now we can use this cut_region object as a data source in generated Projections or Profiles or any other number of tasks.  Let's look at a density projection of the densest material, or the material which is overpressure and hot.

# In[ ]:

proj = yt.ProjectionPlot(ds, 'x', "density", weight_field="density")
proj.annotate_title('All Data, No Cuts')
proj.show()


# In[ ]:

proj = yt.ProjectionPlot(ds, 'x', "density", weight_field="density", data_source=dense_ad)
proj.annotate_title('Only Dense Material')
proj.set_zlim("density", 3e-31, 3e-27)
proj.show()


# In[ ]:

proj = yt.ProjectionPlot(ds, 'x', "density", weight_field="density", data_source=overpressure_and_fast_ad)
proj.annotate_title('Only Overpressure and Fast Material')
proj.set_zlim("density", 3e-31, 3e-27)
proj.show()

