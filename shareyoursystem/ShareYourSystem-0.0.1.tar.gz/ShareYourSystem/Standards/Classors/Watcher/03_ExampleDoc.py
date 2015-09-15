#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass with decorated make by a Watcher
@SYS.WatcherClass(**{
	'WatchingIsBool':True,
	#'ObservingWrapMethodStr':'do_make'
	#'ObservingWrapMethodStr':'superDo_make'
	'ObservingWrapMethodStr':'make'
	})
class MakerClass(object):

	#Definition
	RepresentingKeyStrsList=[
								'MakingMyFloat',
								'MadeMyInt'
							]

	def default_init(self,
				_MakingMyFloat=1.,
				_MadeMyInt=0
				):
		object.__init__(self)

	def do_make(self):

		#print
		print('self.MakingMyFloat is '+str(self.MakingMyFloat))
		print('self.MadeMyInt is '+str(self.MadeMyInt))
		print('')

		#Cast
		self.MadeMyInt=int(self.MakingMyFloat)

#Definition a MakerClass with decorated make by a Watcher
@SYS.WatcherClass(**{
	'WatchingIsBool':True,
	#'ObservingWrapMethodStr':'do_make'
	#'ObservingWrapMethodStr':'superDo_make'
	'ObservingWrapMethodStr':'make'
	})
class BuilderClass(MakerClass):

	#Definition
	RepresentingKeyStrsList=[
							]

	def default_init(self,
				):
		MakerClass.__init__(self)

	def do_buid(self):
		pass

#Definition an instance
MyBuilder=MakerClass()

#Print
print('Before make, MyBuilder is ')
SYS._print(MyBuilder)

#make once
MyBuilder.make(3.)

#Print
print('After the first make, MyBuilder is ')
SYS._print(MyBuilder)

#Definition the AttestedStr
print('BuilderClass.make is '+str(BuilderClass.make))
print('MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

