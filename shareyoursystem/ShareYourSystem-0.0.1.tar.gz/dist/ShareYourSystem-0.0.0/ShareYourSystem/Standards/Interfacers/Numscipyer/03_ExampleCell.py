
#ImportModules
import ShareYourSystem as SYS

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SizeTuple=(3,3),
		_SymmetryFloat=0.
	)

#print
print('Random dense: MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SizeTuple=(3,3),
		_SymmetryFloat=1.
	)

#print
print('Random dense symmetric : MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SizeTuple=(3,3),
		_SymmetryFloat=-1.
	)

#print
print('Random dense antisymmetric : MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)
