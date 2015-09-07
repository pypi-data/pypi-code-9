from factory import open_db_file
from shapely.geometry import Polygon, Point
import time


zones = {}
with open_db_file() as f:
	for line in f:
		p = line.split()
		name = p[2]
		if name not in zones:
			zones[name] = []
		zones[name].append((float(p[1]), float(p[0])))

zzz = []
zzz_names = []
for z in zones:
	if len(zones[z]) < 3:
		continue
	zzz.append(Polygon(zones[z]))
	zzz_names.append(z)

print zzz

t = time.time()

for j in range(10):
	i = 0
	for x in zzz:
		pnt = Point(-109.905347, 27.478088)
		if x.contains(pnt):
			print(zzz_names[i])
		i += 1

print("time spent %.5f" % (time.time() - t))