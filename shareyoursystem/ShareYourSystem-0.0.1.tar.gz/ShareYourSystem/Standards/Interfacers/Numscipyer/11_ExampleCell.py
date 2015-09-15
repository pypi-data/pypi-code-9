
#import 
import ShareYourSystem as SYS
from matplotlib import pyplot
import numpy as np

#set
LenInt=10
DimensionInt=2

#init
MyArray=np.zeros([LenInt]*DimensionInt,dtype=bool)

#define
def _set(_RowInt,_ColInt):

	#set
	CheckBool=True if _RowInt>_ColInt else False

	#set
	MyArray.__setitem__(
		(_RowInt,_ColInt),
		CheckBool
	)

	#plot
	pyplot.plot(_RowInt,_ColInt,marker='o',color="blue" if CheckBool else "red")

#init
map(
	lambda __RowInt:
	map(
		lambda __ColInt:
		_set(__RowInt,__ColInt),
		xrange(LenInt)
	),
	xrange(LenInt)
)

#get
ContourIntsArray=SYS.contour(MyArray)

#plot
pyplot.plot(
	ContourIntsArray[:,0],
	ContourIntsArray[:,1],
	'-'
)

#plot
pyplot.show()

