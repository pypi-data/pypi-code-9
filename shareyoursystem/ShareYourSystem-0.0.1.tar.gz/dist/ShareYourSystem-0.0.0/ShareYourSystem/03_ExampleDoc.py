#ImportModules
import ShareYourSystem as SYS

#Definition a FooClass decorated by the ClassorClass
@SYS.ClassorClass()
class FooClass(object):
	pass
	
#note that the SYS.indent does the same thing
print('FooClass.__dict__ is ')
print(SYS.indent(FooClass))

