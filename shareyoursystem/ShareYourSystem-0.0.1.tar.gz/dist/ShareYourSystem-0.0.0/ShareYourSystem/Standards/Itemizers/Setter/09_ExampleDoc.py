#ImportModules
import ShareYourSystem as SYS
import collections

#Define and automatically set in a child setter
MySetter=SYS.SetterClass(
	).set(
		'ChildSetter',
		{
			'MyStr':"hello"
		}
	)

#Note just that a numpy array can be setted in a list... SuffixStr
import numpy
MySetter['MyList']=numpy.array([1,4])

#print
MySetter.set('MyStr',2,_TypeBool=False)
MySetter['#untype:MyOtherStr']=3

#print
print('MySetter is ')
SYS._print(MySetter)

#print the ChildSetter keystr with which it was setted
print('MySetter.ChildSetter.SetDeriveSetter is ')
SYS._print(MySetter.ChildSetter.SetDeriveSetter)

#print its setter
print("MySetter.ChildSetter['<'] is ")
SYS._print(MySetter.ChildSetter['<'])





