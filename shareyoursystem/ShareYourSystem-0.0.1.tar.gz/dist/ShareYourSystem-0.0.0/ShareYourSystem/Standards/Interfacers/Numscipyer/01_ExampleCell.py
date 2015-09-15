
#ImportModules
import ShareYourSystem as SYS

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SizeTuple=(3,2)
	)

#print
print('MyNumscipyer is ')
SYS._print(MyNumscipyer)

#Build a sparse diluted matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SparseFloat=0.5,
		_SizeTuple=(10,10)
	)

#print
print('MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)

#Build a sparse binary matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SparseFloat=0.5,
		_MeanFloat=1.,
		_SwitchFloat=0.5,
		_StdFloat=0.,
		_SizeTuple=(10,10)
	)

#print
print('MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)

