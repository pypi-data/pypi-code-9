
from math import pi, cos, sin, radians, sqrt

def cot(x):
    return cos(x)/sin(x)

def f_delta(delta):
    factor = 1/(sin(radians(delta))**4+cos(radians(delta))**4)
    return factor

def circle_a(dm, s):
    term = dm**2*pi/4*1000/s
    return term

def circle_dm(a, s):
    term = sqrt(a*4*s/(pi*1000))
    return term

def printf(meth):
	doc = getdoc(meth).split()
	print('{0:>6s} {1:>12s}: {2:>9.2f} {3:<6s}'.format(doc[0], doc[1], meth(), doc[2]))






