#ImportModules
import ShareYourSystem as SYS
import operator

#Definition 
@SYS.ClasserClass(**{
	'ClassingSwitchMethodStrsList':[
		'make'
	]
})
class MakerClass(object):

	def default_init(self,
					_MakingMyFloat=0.,
					_MadeMyInt=0,
					**_KwarVariablesDict
				):
		object.__init__(self,**_KwarVariablesDict)

	def do_make(self):
		
		#print
		print('I am in the do_make of the Maker')

		#cast
		self.MadeMyInt=int(self.MakingMyFloat)

#Definition
@SYS.ClasserClass(**{
	'ClassingSwitchMethodStrsList':[
		'make',
		'build'
	]
}
)
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
SYS._print(MyBuilder.__dict__)

#make once
MyBuilder.make(3.)

#Print
print('After the first make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
MyBuilder.make(5.)

#Print
print('After the second make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
print('Now we switch all')
MyBuilder.setSwitch('make',BuilderClass)

#Print
print('After the switch MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#make again
MyBuilder.make(7.)

#Print
print('After the third make, MyBuilder.__dict__ is ')
SYS._print(MyBuilder.__dict__)

#Definition the AttestedStr
SYS._attest(
	[
		'BuilderClass.WatchBeforeMakeWithMakerBool is '+str(BuilderClass.WatchBeforeMakeWithMakerBool),
		'BuilderClass.make is '+str(BuilderClass.make),
		'BuilderClass.build is '+str(BuilderClass.build),
		'MyBuilder.__dict__ is '+SYS._str(
			MyBuilder.__dict__
		)
	]
) 

#Print



