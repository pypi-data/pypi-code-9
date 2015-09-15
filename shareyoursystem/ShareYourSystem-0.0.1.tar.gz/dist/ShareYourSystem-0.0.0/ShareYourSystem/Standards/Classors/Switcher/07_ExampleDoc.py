#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass(**{
	'SwitchingIsBool':True,
	'SwitchingWrapMethodStr':'make'
})
class MakerClass(object):

	def default_init(self,
				_MakingMyFloat=1.,
				_MadeMyInt=0
				):
		object.__init__(self)

	def do_make(self):

		#Cast
		self.MadeMyInt=int(self.MakingMyFloat)

		#print
		print('self.MadeMyInt is ')
		print(self.MadeMyInt)

#Definition a MakerClass with decorated make by a Switcher
@SYS.SwitcherClass()
class BuilderClass(MakerClass):

	def default_init(self,
				):
		MakerClass.__init__(self)


#print 
print('BuilderClass.SwitchMethodDict is ')
print(SYS.indent(BuilderClass.SwitchMethodDict))

#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#print
print('MyBuilder.getSwitch()')
print(SYS.indent(MyBuilder.getSwitch()))

#make once
print('We make')
print(MyBuilder.make)
MyBuilder.make(3.)

#print
print('MyBuilder.getSwitch()')
print(SYS.indent(MyBuilder.getSwitch()))

#Print
print('After the make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
print('Now we switch')
MyBuilder.setSwitch()

#Switch by default it is just the last Name and the the last do in the mro
print('Now we switch')
MyBuilder.setSwitch('make')

#Print
print('After the switch MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)


