import bredala
bredala.USE_PROFILER = True
bredala.register("bredala.demo.myclasses", names=["Square.area", "Square.__init__",
                                                  "Triangle.area"])
from bredala.demo.myclasses import Square, Triangle
o = Square("my_square")
print(o.area(2))
o = Triangle("my_square")
o.area(2, 3)
