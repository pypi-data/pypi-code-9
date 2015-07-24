
# This example shows how to embed an animation produced by `matplotlib` into an IPython notebook.  This example makes use of `matplotlib`'s [animation toolkit](http://matplotlib.org/api/animation_api.html) to transform individual frames into a final rendered movie.  
# 
# Additionally, this uses Jake VanderPlas' [`JSAnimation`](https://github.com/jakevdp/JSAnimation) library to embed the movie as a javascript widget, directly in the notebook.  This does not use `ffmpeg` to stitch the frames together and thus does not require `ffmpeg`.  However, you must have `JSAnimation` installed.
# 
# To do so, clone to git repostiory and run `python setup.py install` in the root of the repository.

# In[ ]:

import yt
from JSAnimation import IPython_display
from matplotlib import animation


# Here we set up the animation.  We use yt to load the data and create each frame and use matplotlib to stitch the frames together.  Note that we customize the plot a bit by calling the `set_zlim` function.  Customizations only need to be applied to the first frame - they will carry through to the rest.
# 
# This may take a while to run, be patient.

# In[ ]:

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

prj = yt.ProjectionPlot(yt.load('Enzo_64/DD0000/data0000'), 0, 'density', weight_field='density',width=(180,'Mpccm'))
prj.set_figure_size(5)
prj.set_zlim('density',1e-32,1e-26)
fig = prj.plots['density'].figure

# animation function.  This is called sequentially
def animate(i):
    ds = yt.load('Enzo_64/DD%04i/data%04i' % (i,i))
    prj._switch_ds(ds)

# call the animator.  blit=True means only re-draw the parts that have changed.
animation.FuncAnimation(fig, animate, frames=44, interval=200, blit=False)

