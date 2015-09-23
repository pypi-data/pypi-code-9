import random
import math

class ColorGenerator:

    def get_random_color_set(self, s=None, v=None):
        self.colors = []
        self.saturation = s
        self.value = v

        for i in range(0,24):
            color = self.generate_new_color()
            self.colors.append(color)

        return ['#%02X%02X%02X' % c for c in self.colors]

    def get_random_hsv(self):
        r = lambda: random.random()

        h = random.randint(0, 360)
        s = self.saturation if self.saturation else r()
        v = self.value if self.value else r()

        return (h, s, v)

    def generate_new_color(self):
        h,s,v = self.get_random_hsv()
        return tuple(self.hsv_to_rgb(h,s,v))

    def hsv_to_rgb(self, h, s, v):
        # One might ask himself why I don't use colorsys here.
        # Well, just out of stupidity i guess. And I wanted to implement the
        # algorithm found at https://en.wikipedia.org/wiki/HSL_and_HSV as
        # readable as possible.

        h = float(h)
        s = float(s)
        v = float(v)
        c = v * s
        hi = h / 60.0
        x = c * (1- abs(hi % 2 - 1))
        m = v - c
        r,g,b = 0,0,0

        if 0 <= hi < 1: r,g,b = c, x, 0
        elif 1 <= hi < 2: r,g,b = x, c, 0
        elif 2 <= hi < 3: r,g,b = 0, c, x
        elif 3 <= hi < 4: r,g,b = 0, x, c
        elif 4 <= hi < 5: r,g,b = x, 0, c
        elif 5 <= hi < 6: r,g,b = c, 0, x

        return map(self.from_float, (r+m,g+m,b+m))

    def from_float(self, value, domain=255):
        return int(round(value * domain))
