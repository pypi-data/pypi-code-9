#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.DoerClass()
class MakerClass(object):

	def default_init(self,
				):
		object.__init__(self)

	def do_make(self):
		pass

#Define
@SYS.DoerClass()
class BuilderClass(MakerClass):

	def default_init(self,
				):
		MakerClass.__init__(self)

	def do_build(self):
		pass
	
#print
print('MakerClass.MroDoerClassesList is')
print(MakerClass.MroDoerClassesList)
print('BuilderClass.MroDoerClassesList is')
print(BuilderClass.MroDoerClassesList)

#print
print('MakerClass.DoMethodStrsList is')
print(MakerClass.DoMethodStrsList)
print('BuilderClass.DoMethodStrsList is')
print(BuilderClass.DoMethodStrsList)
