#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the DefaultorClass
@SYS.DefaultorClass()
class FooClass(object):

	def default_init(self,
						Int,
						_MyFloat=1.,
						_MyInt={
									'DefaultValueType':int
								}
				):
		#call the base method
		object.__init__(self)
		
		#Definition an attribute
		self.MyStr='I am a Foo with MyFloat equal to '+str(self.MyFloat)+' and Int equal to '+str(Int)


#print
print("\n".join(
		[
		'FooClass.__init__ is '+str(FooClass.__init__),
		'FooClass has some special attributes',
		#'FooClass.InitInspectDict is '+SYS._str(FooClass.InitInspectDict),
		'FooClass.DefaultAttributeVariablesOrderedDict is '+SYS.indent(
			FooClass.DefaultAttributeVariablesOrderedDict),
		'FooClass.MyFloat is '+str(FooClass.MyFloat),
		'FooClass.MyInt is '+str(FooClass.MyInt),
		]
	)
)

#Definition a default instance that will take its values from the default classed attributes
DefaultFoo=FooClass(3)

#print
print("\n"+"\n".join(
	[
		'What are you saying DefaultFoo ?',
		'DefaultFoo.__dict__ is '+str(DefaultFoo.__dict__),
		'DefaultFoo.MyFloat is '+str(DefaultFoo.MyFloat),
		'DefaultFoo.MyInt is '+str(DefaultFoo.MyInt)
	]
))

#Definition a special instance that sets in its __dict__
SpecialFoo=FooClass(
			3,
			**{'MyInt':5}
		)

#print
print("\n"+"\n".join(
	[
		'What are you saying SpecialFoo ?',
		'SpecialFoo.__dict__ is '+str(SpecialFoo.__dict__),
		'SpecialFoo.MyFloat is '+str(SpecialFoo.MyFloat),
		'SpecialFoo.MyInt is '+str(SpecialFoo.MyInt)
	]
	)
)

#Change a classed attribute
FooClass.MyFloat=7.

#Add
print("\n"+"\n".join(
		[
		'After reset at the level of the class',
		'DefaultFoo.MyFloat is '+str(DefaultFoo.MyFloat),
		'SpecialFoo.MyFloat is '+str(SpecialFoo.MyFloat),
		]
	)
)


