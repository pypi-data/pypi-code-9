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

	def default_init(self,
				_MakingMyFloat=1.,
				_MadeMyInt=0
				):
		object.__init__(self)

	def do_make(self):

		#print
		#print('self.MakingMyFloat is '+str(self.MakingMyFloat))
		#print('self.MadeMyInt is '+str(self.MadeMyInt))
		#print('')

		#Cast
		self.MadeMyInt=int(self.MakingMyFloat)

	def setWatchAfterMakeWithMakerBool(self,_SettingValueVariable):

		#set
		self._WatchAfterMakeWithMakerBool=_SettingValueVariable

		#Check
		if _SettingValueVariable:

			#debug
			print('\n**We have Made here !**')
			print('self.MakingMyFloat is '+str(self.MakingMyFloat))
			print('self.MadeMyInt is '+str(self.MadeMyInt))
			print('')

		else:

			#debug
			print(
				'\n**We have switch the Make here !**\n'
			)


#Definition an instance
MyMaker=MakerClass()

#Print
print('Before make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make once
MyMaker.make(3.)

#print
print('After the first make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MakerClass.make is '+str(MakerClass.make))

#Check that the watch_superDo_make has access to the BaseDoClass
print('MakerClass.make.BaseDoClass is ')
print(MakerClass.make.BaseDoClass)
