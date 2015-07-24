
# # Welcome to the yt bootcamp!
# 
# In this brief tutorial, we'll go over how to load up data, analyze things, inspect your data, and make some visualizations.
# 
# Our documentation page can provide information on a variety of the commands that are used here, both in narrative documentation as well as recipes for specific functionality in our cookbook.  The documentation exists at http://yt-project.org/doc/.  If you encounter problems, look for help here: http://yt-project.org/doc/help/index.html.
# 
# ## Acquiring the datasets for this tutorial
# 
# If you are executing these tutorials interactively, you need some sample datasets on which to run the code.  You can download these datasets at http://yt-project.org/data/.  The datasets necessary for each lesson are noted next to the corresponding tutorial.
# 
# ## What's Next?
# 
# The Notebooks are meant to be explored in this order:
# 
# 1. Introduction
# 2. Data Inspection (IsolatedGalaxy dataset)
# 3. Simple Visualization (enzo_tiny_cosmology & Enzo_64 datasets)
# 4. Data Objects and Time Series (IsolatedGalaxy dataset)
# 5. Derived Fields and Profiles (IsolatedGalaxy dataset)
# 6. Volume Rendering (IsolatedGalaxy dataset)

# The following code will download the data needed for this tutorial automatically using `curl`. It may take some time so please wait when the kernel is busy. You will need to set `download_datasets` to True before using it.

# In[ ]:

download_datasets = False
if download_datasets:
    get_ipython().system(u'curl -sSO http://yt-project.org/data/enzo_tiny_cosmology.tar')
    print "Got enzo_tiny_cosmology"
    get_ipython().system(u'tar xf enzo_tiny_cosmology.tar')
    
    get_ipython().system(u'curl -sSO http://yt-project.org/data/Enzo_64.tar')
    print "Got Enzo_64"
    get_ipython().system(u'tar xf Enzo_64.tar')
    
    get_ipython().system(u'curl -sSO http://yt-project.org/data/IsolatedGalaxy.tar')
    print "Got IsolatedGalaxy"
    get_ipython().system(u'tar xf IsolatedGalaxy.tar')
    
    print "All done!"

