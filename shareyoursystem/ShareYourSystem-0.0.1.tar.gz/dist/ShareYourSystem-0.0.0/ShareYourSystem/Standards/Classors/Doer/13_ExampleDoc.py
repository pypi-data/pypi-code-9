#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.DoerClass()
class MakerClass(object):

	def default_init(self,
				_MakingMyFloat=0.,
				_MakingFirstList=None
				):
		object.__init__(self)

	def do_make(self):
		pass

#Define
@SYS.DoerClass()
class BuilderClass(MakerClass):

	def default_init(self,
				_BuildingMyStr=""
				):
		MakerClass.__init__(self)

	def do_build(self):
		pass
	
#define
MyBuilder=BuilderClass(
	).make(
		5.
	)

#print
print('MyBuilder.getDo() is')
print(SYS.indent(MyBuilder.getDo()))

#print
print('MyBuilder.__dict__ is')
print(SYS.indent(MyBuilder.__dict__))

#reset everything
MyBuilder.setDoing()

#print
print('MyBuilder.__dict__ is')
print(SYS.indent(MyBuilder.__dict__))



