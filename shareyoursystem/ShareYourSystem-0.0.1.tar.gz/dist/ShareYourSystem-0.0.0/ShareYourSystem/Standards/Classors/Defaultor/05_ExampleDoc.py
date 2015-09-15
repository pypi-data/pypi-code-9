#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

	def default_init(self,
						_ShareClassor=SYS.ClassorClass(),
						_SpecificClassor=None
				):
		object.__init__(self)

#Definition 
FooClass.ShareClassor.MyInt=2
MyFirstFoo=FooClass()
MySecondFoo=FooClass()

#Definition the AttestedStr
print("\n".join(
	[
		'MyFirstFoo.ShareClassor.__dict__ is ',SYS.indent(
			MyFirstFoo.ShareClassor.__dict__),
		'MyFirstFoo.__dict__ is '+SYS.indent(MyFirstFoo.__dict__),
		'MyFirstFoo.SpecificClassor is '+str(MyFirstFoo.SpecificClassor)
	]
	)
)


