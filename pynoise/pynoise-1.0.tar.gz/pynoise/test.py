from module import Perlin
from noiseutil import RenderImage, noise_map_plane, terrain_gradient

perlin = Perlin()
# print(perlin.get_value(1.25, 0.75, 0.5))

nm = noise_map_plane(lower_x=2, upper_x=6, lower_z=1, upper_z=5,
    width=256, height=256, source=perlin)

gradient = terrain_gradient()

render = RenderImage(light_enabled=True, light_contrast=3, light_brightness=2)
render.render(nm, 'test.png', gradient)
