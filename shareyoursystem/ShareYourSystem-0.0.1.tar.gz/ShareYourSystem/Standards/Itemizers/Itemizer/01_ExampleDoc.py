
#ImportModules
import ShareYourSystem as SYS

@SYS.ClassorClass()
class MakerClass(SYS.ItemizerClass):
	
	def default_init(self,
			_MakingMyFloat=0.,
			_MadeMyInt=0
		):

		#call the init base method
		SYS.ItemizerClass.__init__(self)

	def do_make(self):

		#set
		self.MadeMyInt=self.MakingMyFloat

#define and itemize just like a get
MyMaker=MakerClass(
	).itemize(
		#ItemizingKeyVariable
		'MakingMyFloat'
	)

#print
print('MyMaker.getDo(SYS.ItemizerClass) for a simple get like is ')
print(SYS.indent(MyMaker.getDo(SYS.ItemizerClass)))

#define and itemize like a set
MyMaker=MakerClass(
	).itemize(
		#ItemizingKeyVariable
		'MakingMyFloat',
		#ItemizingValueVariable
		3.
	)

#print
print('MyMaker.getDo(SYS.ItemizerClass) for a set like is ')
print(SYS.indent(MyMaker.getDo(SYS.ItemizerClass)))

#define and itemize
MyMaker=MakerClass(
	).itemize(
		#ItemizingKeyVariable
		'make'
	)

#print
print('MyMaker.getDo(SYS.ItemizerClass) for a get method like is ')
print(SYS.indent(MyMaker.getDo(SYS.ItemizerClass)))

