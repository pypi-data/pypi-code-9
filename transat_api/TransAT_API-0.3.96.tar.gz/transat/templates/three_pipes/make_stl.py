import sys

FREECADPATH = '/usr/lib/freecad/lib'
sys.path.append(FREECADPATH)

import FreeCAD
import Part
import math


def get_H(a, r, l):
    h2 = math.tan(a) * 2 * r
    h1 = l / math.cos(a)
    return h1 + h2


r = {r}
H = {H}
a1 = {a1}
a1 = math.pi * a1 / 180
l1 = {l1}
a2 = {a2}
a2 = math.pi * a2 / 180
l2 = {l2}

H1 = get_H(a1, r, l1)
H2 = get_H(a2, r, l2)

x1 = 0.0  # r- math.sin(a1)*r
y1 = math.cos(a1) * r

x2 = 0.0  # -r+math.sin(a2)*r
y2 = H - math.cos(a2) * r

cylinder1 = Part.makeCylinder(r, H1, FreeCAD.Base.Vector(x1, y1, 0), FreeCAD.Base.Vector(math.cos(a1), math.sin(a1), 0))
cylinder2 = Part.makeCylinder(r, H, FreeCAD.Base.Vector(0, 0, 0), FreeCAD.Base.Vector(0, 1, 0))
cylinder3 = Part.makeCylinder(r, H2, FreeCAD.Base.Vector(x2, y2, 0),
                              FreeCAD.Base.Vector(-math.cos(a2), -math.sin(a2), 0))

cylinder1.exportStl("cylinder1.stl")
cylinder2.exportStl("cylinder2.stl")
cylinder3.exportStl("cylinder3.stl")


