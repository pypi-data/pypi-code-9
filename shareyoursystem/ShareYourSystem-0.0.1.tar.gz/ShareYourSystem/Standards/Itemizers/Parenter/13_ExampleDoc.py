
#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.ClasserClass()
class MakerClass(SYS.ParenterClass):

	def default_init(
						self,
						_MakingMyFloat=0.
					):
		SYS.ParenterClass.__init__(self)
		
	def propertize_setParentKeyStr(self,_SettingValueVariable):
		
		#set
		SYS.ParenterClass.propertize_setParentKeyStr(self,_SettingValueVariable)

		#debug
		self.debug(
			[	
				'I know my parent !',
				('self["^"].',self['^'],['ParentKeyStr'])
			]
		)

#Define
MyMaker=MakerClass(
	).set(
		'-Things',MakerClass()
	)

#print
print('MyMaker is ')
SYS._print(MyMaker)

#Define
@SYS.ClasserClass()
class BuilderClass(MakerClass):

	def propertize_setParentKeyStr(self,_SettingValueVariable):
		
		#call the base method
		MakerClass.propertize_setParentKeyStr(self,_SettingValueVariable)

		#debug
		self.debug(
			[	
				'and its id is :',
				('self["^"].',self['^'],['PrintIdInt'])
			]
		)

#Define
MyBuilder=BuilderClass(
	).set(
		'-Things',BuilderClass()
	)

#print
print('MyBuilder is ')
SYS._print(MyBuilder)