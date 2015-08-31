import sys
sys.path.append('/home/atrus/Copy/pynoise')

from pynoise.noisemodule import  RidgedMulti
from pynoise.noiseutil import noise_map_plane, terrain_gradient, RenderImage

nm_ridged = noise_map_plane(lower_x=-180, upper_x=180, lower_z=-90, upper_z=90, width=256, height=256, source=RidgedMulti())
gradient = terrain_gradient()

r = RenderImage()
r.render(nm_ridged, 'ridged2.png', gradient)
