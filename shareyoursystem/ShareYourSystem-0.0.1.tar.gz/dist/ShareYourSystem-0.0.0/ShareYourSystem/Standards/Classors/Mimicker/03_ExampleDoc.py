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

		#print
		print('self.MakingMyFloat is '+str(self.MakingMyFloat))
		print('self.MadeMyInt is '+str(self.MadeMyInt))
		print('')

		#Cast
		self.MadeMyInt=int(self.MakingMyFloat)

#Definition
@SYS.MimickerClass(**{
	'MimickingDoMethodStr':"make"
})
class BuilderClass(MakerClass):

	def default_init(self,
					**_KwarVariablesDict
				):
		MakerClass.__init__(self,**_KwarVariablesDict)

	def mimic_make(self):
		
		#print
		print('I am in the mimic_make of the Builder')

		#call the parent method
		MakerClass.make(self)

		#cast
		self.MadeMyInt+=10

	def do_build(self):
		pass


#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

#print 
print('MyBuilder.getSwitch() is ')
print(SYS.indent(MyBuilder.getSwitch()))

#make once
MyBuilder.make(3.)

#Print
print('After the first make, MyBuilder is ')
print(SYS.indent(MyBuilder.__dict__))

#print 
print('MyBuilder.getSwitch() is ')
print(SYS.indent(MyBuilder.getSwitch()))

#make again
MyBuilder.make(5.)

#Print
print('After the second make, MyBuilder is ')
print(SYS.indent(MyBuilder.__dict__))

#make again
print('Now we switch')
MyBuilder.setSwitch(_DoMethodVariable=['make'])

#Print
print('After the switch MyBuilder is ')
print(SYS.indent(MyBuilder.__dict__))

