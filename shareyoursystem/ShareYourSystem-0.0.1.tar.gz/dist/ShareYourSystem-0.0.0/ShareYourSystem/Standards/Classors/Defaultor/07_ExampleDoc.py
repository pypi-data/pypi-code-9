#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

	def default_init(self,
						_MyFloat=1.,
						_MyShareList=[],
						_MyFirstSpecificList=None,
						_MySecondSpecificList=None,
						_MyInt={
									'DefaultValueType':int
								}
				):
		object.__init__(self)

#Definition 
MyFoo=FooClass(**{'MyFloat':5.,'MyInt':9})
MyFoo.MyShareList.append(7)
MyFoo.MyFirstSpecificList=['hello']

#Before default
print('Before setDefault MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#default
MyFoo.setDefault(
	#ClassVariable
	#it can be a Class, ClassKeyStr or [Class]
	FooClass,
	#AttributeKeyStrsList 
	#it can be just a KeyStr a [<KeyStr>] and if None it is all the KeyStr from all the Classes
	['MyFloat','MyFirstSpecificList']
)

#After default
print('\nAfter setDefault MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#default
MyFoo.setDefaultMutable(
	#ClassVariable
	#it can be a Class, ClassKeyStr or [Class]
	FooClass,
	#AttributeKeyStrsList 
	#it can be just a KeyStr a [<KeyStr>] and if None it is all the KeyStr from all the Classes
	['MyFirstSpecificList']
)

#After default
print('\nAfter setDefaultMutable MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#append to the share list
MyFoo.MyShareList.append(8)

#After default
print('\nAfter setDefault MyFoo.__dict__ is')
print(SYS.indent(MyFoo.__dict__))

#define
print('\nFooClass.DefaultAttributeVariablesOrderedDict is '+SYS.indent(
			FooClass.DefaultAttributeVariablesOrderedDict)
)

#print
print('\nMyFoo.__dict__ is ')
print(SYS.indent(MyFoo.__dict__))



