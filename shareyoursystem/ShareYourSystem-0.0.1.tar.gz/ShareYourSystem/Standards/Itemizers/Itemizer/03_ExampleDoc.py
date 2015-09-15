
#ImportModules
import ShareYourSystem as SYS

@SYS.DoerClass()
class MakerClass(SYS.ItemizerClass):
	
	def default_init(self,
			_MakingMyFloat=0.,
			_MadeMyInt=0
		):

		#call the init base method
		SYS.ItemizerClass.__init__(self)

	def do_make(self):

		#set
		self.MadeMyInt=(int)(self.MakingMyFloat)

#Define how to get a list from the args in the ItemizedValueMethod
#(Module definition level)
def getMapList(_LiargVariablesList):
	return map(
		lambda __Variable:
		[__Variable],
		_LiargVariablesList[0]
	)
#Define what to outpu from the instance 
#(Class definition level)
MakerClass.getMapValueVariable=lambda _SelfVariable:_SelfVariable.MadeMyInt

#define and itemize just like a get
MyMaker=MakerClass(
	).itemize(
		#ItemizingKeyVariable
		'#map@make',
	)

#show the map
print("MyMaker.ItemizedValueMethod([3.,6.]).ItemizedMapValueVariablesList is ")
print(MyMaker.ItemizedValueMethod([3.,6.]).ItemizedMapValueVariablesList)

