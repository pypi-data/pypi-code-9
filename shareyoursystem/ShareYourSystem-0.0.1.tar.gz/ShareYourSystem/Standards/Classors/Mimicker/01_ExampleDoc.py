#ImportModules
import ShareYourSystem as SYS

#Definition 
@SYS.DoerClass()
class MakerClass(object):

	def default_init(self,
					_MakingMyFloat=0.,
					_MakingFirstInt=0,
					_MakingSecondInt=1,
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
@SYS.MimickerClass(**{
	'MimickingDoMethodStr':'make'
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

#Definition an instance
MyBuilder=BuilderClass()

#Print
print('Before make, MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

#make once
MyBuilder.make(
	3.,
	_FirstInt=2,
	**{
		'MakingSecondInt':5
	}
)

#Print
print('After the first make, MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

#Definition the AttestedStr
print('BuilderClass.make is '+str(BuilderClass.make))

#print
print('MyBuilder.__dict__ is ')
print(SYS.indent(MyBuilder.__dict__))

#Check
print('MakerClass.make.BaseDoClass is ')
print(MakerClass.make.BaseDoClass)
print('BuilderClass.make.BaseDoClass is ')
print(BuilderClass.make.BaseDoClass)




