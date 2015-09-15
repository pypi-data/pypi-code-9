#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass(**{
	'SwitchingIsBool':True,
	#'ObservingWrapMethodStr':'do_make'
	#'ObservingWrapMethodStr':'superDo_make'
	'SwitchingWrapMethodStr':'make'
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

	def getWatchAfterMakeWithMakerBool(self):

		#try
		try:
			return getattr(self,'_WatchAfterMakeWithMakerBool')
		except:
			return False

	def setWatchAfterMakeWithMakerBool(self,_SettingValueVariable):

		#set the value of the "hidden" property variable
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

	def delWatchAfterMakeWithMakerBool(self):
		self.__delattr__('_WatchAfterMakeWithMakerBool')

	WatchAfterMakeWithMakerBool=property(
			getWatchAfterMakeWithMakerBool,
			setWatchAfterMakeWithMakerBool,
			delWatchAfterMakeWithMakerBool,
			'WatchAfterMakeWithMakerBool is now reactive !'
		)

#Definition an instance
MyMaker=MakerClass()

#Print
print('Before make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make once
MyMaker.make(3.)

#Print
print('After the first make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make again
MyMaker.make(5.)

#Print
print('After the second make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make again
print('Now we switch')
MyMaker.setSwitch()

#Print
print('After the switch MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make again
MyMaker.make(7.)

#Print
print('After the third make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MakerClass.make is '+str(MakerClass.make))

#print
print('MyMaker.__dict__ is '+SYS._str(MyMaker.__dict__))



