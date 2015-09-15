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
		print('self.MakingMyFloat is '+str(self.MakingMyFloat))
		print('self.MadeMyInt is '+str(self.MadeMyInt))
		print('')

		#Cast
		self.MadeMyInt=int(self.MakingMyFloat)

#print 
print('MakerClass.SwitchMethodDict is ')
print(SYS.indent(MakerClass.SwitchMethodDict))

#Definition an instance
MyMaker=MakerClass()

#print 
print('MyMaker.getSwitch() is ')
print(SYS.indent(MyMaker.getSwitch()))

#Print
print('Before make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#make once
print('We make for the first time')
MyMaker.make(3.)

#Print
print('After the first make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print 
print('MyMaker.getSwitch() is ')
print(SYS.indent(MyMaker.getSwitch()))

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

#print 
print('MyMaker.getSwitch() is ')
print(SYS.indent(MyMaker.getSwitch()))

#make again
MyMaker.make(7.)

#Print
print('After the third make, MyMaker.__dict__ is ')
SYS._print(MyMaker.__dict__)

#print
print('MakerClass.make is '+str(MakerClass.make))

#print
print('MyMaker.__dict__ is '+SYS._str(MyMaker.__dict__))


