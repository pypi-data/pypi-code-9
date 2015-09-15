#ImportModules
import ShareYourSystem as SYS

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SizeTuple=(5,5),
		_ProbabilityFloat=0.5,
		_MeanFloat=1.,
		_StdFloat=0.,
		_SymmetryFloat=0.,
	)

#print
print('Random sparse : MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SizeTuple=(5,5),
		_ProbabilityFloat=0.5,
		_MeanFloat=1.,
		_StdFloat=0.,
		_SymmetryFloat=0.5
	)

#print
print('Random sparse symmetric : MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)

#Build a norm dense matrix
MyNumscipyer=SYS.NumscipyerClass(
	).numscipy(
		_SizeTuple=(5,5),
		_ProbabilityFloat=0.5,
		_MeanFloat=1.,
		_StdFloat=0.,
		_SymmetryFloat=-0.5
	)

#print
print('Random sparse antisymmetric : MyNumscipyer.NumscipiedValueFloatsArray is ')
SYS._print(MyNumscipyer.NumscipiedValueFloatsArray)

