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

#Definition a FeeClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FeeClass(FooClass):

	def default_init(self,
						_MyBool=True,
				):
		FooClass.__init__(self)

#put in the SYS scope
SYS.FeeClass=FeeClass

#Definition 
MyFee=FeeClass(**{
	'MyFloat':5.,
	'MyInt':9,
	'MyBool':False
})

#Before default
print('Before setDefault MyFee.__dict__ is')
print(SYS.indent(MyFee.__dict__))

#default and also init the mutable variables
MyFee.setDefault(
	#ClassVariable,
	[FooClass,'FeeClass'],
	**{'DefaultMutableBool':True}
)

#print
print('\nMyFee.__dict__ is ')
print(SYS.indent(MyFee.__dict__))



