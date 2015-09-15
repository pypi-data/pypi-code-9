#ImportModules
import ShareYourSystem as SYS

#define
@SYS.ClassorClass()
class MakerClass(object):

	def default_init(self,
			_MakingMyStr,
			_MakingMyInt=0,
			**_KwargVariablesDict
		):
		object.__init__(self,**_KwargVariablesDict)

	def do_make(self):

		#str
		self.MadeMyStr=str(self.MakingMyStr)

#print
print('MakerClass.InspectInspectDict is ')
print(SYS.indent(
		MakerClass.InspectInspectDict
	)
)
 

