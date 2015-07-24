
# This example shows how to embed an animation produced by `matplotlib` into an IPython notebook.  This example makes use of `matplotlib`'s [animation toolkit](http://matplotlib.org/api/animation_api.html) to transform individual frames into a final rendered movie.  
# 
# Matplotlib uses [`ffmpeg`](http://www.ffmpeg.org/) to generate the movie, so you must install `ffmpeg` for this example to work correctly.  Usually the best way to install `ffmpeg` is using your system's package manager.

# In[ ]:

import yt
from matplotlib import animation


# First, we need to construct a function that will embed the video produced by ffmpeg directly into the notebook document. This makes use of the [HTML5 video tag](http://www.w3schools.com/html/html5_video.asp) and the WebM video format.  WebM is supported by Chrome, Firefox, and Opera, but not Safari and Internet Explorer.  If you have trouble viewing the video you may need to use a different video format.  Since this uses `libvpx` to construct the frames, you will need to ensure that ffmpeg has been compiled with `libvpx` support.

# In[ ]:

from tempfile import NamedTemporaryFile

VIDEO_TAG = """<video controls>
 <source src="data:video/x-webm;base64,{0}" type="video/webm">
 Your browser does not support the video tag.
</video>"""

def anim_to_html(anim):
    if not hasattr(anim, '_encoded_video'):
        with NamedTemporaryFile(suffix='.webm') as f:
            anim.save(f.name, fps=6, extra_args=['-vcodec', 'libvpx'])
            video = open(f.name, "rb").read()
        anim._encoded_video = video.encode("base64")
    
    return VIDEO_TAG.format(anim._encoded_video)


# Next, we define a function to actually display the video inline in the notebook.

# In[ ]:

from IPython.display import HTML

def display_animation(anim):
    plt.close(anim._fig)
    return HTML(anim_to_html(anim))


# Finally, we set up the animation itsself.  We use yt to load the data and create each frame and use matplotlib to stitch the frames together.  Note that we customize the plot a bit by calling the `set_zlim` function.  Customizations only need to be applied to the first frame - they will carry through to the rest.
# 
# This may take a while to run, be patient.

# In[ ]:

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

prj = yt.ProjectionPlot(yt.load('Enzo_64/DD0000/data0000'), 0, 'density', weight_field='density',width=(180,'Mpccm'))
prj.set_zlim('density',1e-32,1e-26)
fig = prj.plots['density'].figure

# animation function.  This is called sequentially
def animate(i):
    ds = yt.load('Enzo_64/DD%04i/data%04i' % (i,i))
    prj._switch_ds(ds)

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=44, interval=200, blit=False)

# call our new function to display the animation
display_animation(anim)

