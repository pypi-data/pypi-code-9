import numpy as np
import pyfilm as pf

x = np.random.rand(100,10,10)

pf.make_film_2d(x, options={'title':'Hello'})
