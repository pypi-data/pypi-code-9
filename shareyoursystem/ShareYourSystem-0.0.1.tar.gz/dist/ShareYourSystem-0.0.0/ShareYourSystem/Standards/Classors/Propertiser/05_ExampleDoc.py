#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(object):

	def default_init(self,
			_MakingMyFloat={
							'DefaultValueType':property,
							'PropertyInitVariable':3.,
							'PropertyDocStr':'I am doing the thing here'
							},
			_MakingMyList={
							'DefaultValueType':property,
							'PropertyInitVariable':[],
							'PropertyDocStr':'I am doing the thing here'
							},
			_MakingMyInt={'DefaultValueType':int},
			_MadeMyInt=0	
		):
		object.__init__(self)

	def propertize_setMakingMyFloat(self,_SettingValueVariable):

		#Print
		#print('I am going to make the job directly !')

		#set the value of the "hidden" property variable
		self._MakingMyFloat=_SettingValueVariable

		#Bind with MadeInt setting
		self.MadeMyInt=int(self._MakingMyFloat)

	def propertize_setMakingMyList(self,_SettingValueVariable):

		#set the value of the "hidden" property variable
		self._MakingMyList=_SettingValueVariable+['Hellllllo']


#Define
@SYS.PropertiserClass()
class BuilderClass(MakerClass):

	def default_init(
						self
					):
		SYS.MakerClass.__init__(self)

	def propertize_setMakingMyList(self,_SettingValueVariable):

		#call the base method
		MakerClass.propertize_setMakingMyList(self,_SettingValueVariable)

		#set the value of the "hidden" property variable
		self._MakingMyList+=['Build en plus !']

	#We need here to redefine
	MakingMyList=property(
			MakerClass.MakingMyList.fget,
			propertize_setMakingMyList,
			MakerClass.MakingMyList.fdel
		)

#Definition a special instance
SpecialBuilder=BuilderClass(_MakingMyFloat=5,_MakingMyList=[4])

#Definition the AttestedStr
print('\n'.join(
	[
		'What are you saying SpecialBuilder ?',
		'SpecialBuilder.__dict__ is '+str(SpecialBuilder.__dict__),
		'SpecialBuilder.MakingMyFloat is '+str(SpecialBuilder.MakingMyFloat),
		'SpecialBuilder.MakingMyList is '+str(SpecialBuilder.MakingMyList),
		'SpecialBuilder.MadeMyInt is '+str(SpecialBuilder.MadeMyInt),
	]
	)
) 

#Print
