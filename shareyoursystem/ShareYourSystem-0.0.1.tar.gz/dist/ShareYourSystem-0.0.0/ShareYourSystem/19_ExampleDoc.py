#ImportModules
import ShareYourSystem as SYS
import numpy as np

#init
FirstArray=np.array(
	[
		[1,2,3],
		[4,5,6]
	]
)

#init
SecondArray=np.array(
	[
		[8,9,10],
		[3,2,1]
	]
)

#setMatrixArray
SYS.setMatrixArray(
	FirstArray,
	SecondArray
)

#print
print('FirstArray is ')
print(FirstArray)

#init
ThirdArray=np.array(
	[
		[1,2,3],
		4
	]
)

#setMatrixArray
SYS.setMatrixArray(
	FirstArray,
	ThirdArray,
	np.ndarray.__mul__
)

#print
print('FirstArray is ')
print(FirstArray)

#setMatrixArray
SYS.setMatrixArray(
	FirstArray,
	2,
	np.ndarray.__add__
)

#print
print('FirstArray is ')
print(FirstArray)

#init
FourthArray=np.array(
	[
		[2.,0.5],
		0.5,
		1.
	]
)

#setMatrixArray
SYS.setMatrixArray(
	FirstArray,
	FourthArray,
	np.ndarray.__mul__,
	_AxisInt=1
)

#print
print('FirstArray is ')
print(FirstArray)






