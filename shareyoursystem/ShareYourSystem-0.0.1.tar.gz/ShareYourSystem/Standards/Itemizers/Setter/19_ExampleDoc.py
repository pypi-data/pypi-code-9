
#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass
@SYS.ClasserClass()
class MakerClass(SYS.SetterClass):

	def default_init(self,
			_MakingIntsList={
							'DefaultValueType':property,
							'PropertyInitVariable':None,
							'PropertyDocStr':'I am doing the thing here'
							},
			_MadeSumInt=0	
		):
		pass

	#Definition a binding function
	def propertize_setMakingIntsList(self,_SettingValueVariable):

		#debug
		self.debug('MakingIntsList is setted !')

		#set the value of the "hidden" property variable
		self._MakingIntsList=_SettingValueVariable

		#Bind with MadeInt setting
		self.MadeSumInt=sum(self._MakingIntsList)

#define and set
MyMaker=MakerClass(
	)

#print(MakerClass.)

#print
print('MyMaker before set is ')
SYS._print(MyMaker)

#set
MyMaker.__setitem__(
		'MakingIntsList',
		[3,4]
	)

#print
print('MyMaker is ')
SYS._print(MyMaker)

