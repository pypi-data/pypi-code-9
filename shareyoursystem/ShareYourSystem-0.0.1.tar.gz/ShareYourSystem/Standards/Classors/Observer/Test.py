#ImportModules
import operator
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Functers import Triggerer
from ShareYourSystem.Standards.Objects import Setter

#Test
class IncrementerClass(Setter.SetterClass):
	
	@Triggerer.TriggererClass(**{'TriggeringConditionVariable':[('SettingKeyVariable',(operator.eq,"Int"))]})
	def increment(self,**_KwargVariablesDict):
		
		#Print
		self.debug(
					[
						('I increment Int !'),
						('Int is before '+str(self.Int))
					]
				)

		#Increment
		self.Int+=1

		#Print
		self.debug(
					[
						('Int is now '+str(self.Int))
					]
				)

#Get an instance and set a default Int
print('')
print("Get an instance and set a default Int")
MyIncrementer=IncrementerClass().__setitem__('Int',3)

#Caa a first time the binding method
print('')
print("Call a first time the binding method")
MyIncrementer.increment()
print('')
print('MyIncrementer is now')
print(MyIncrementer)

#Call a setting that not bind
print('')
print('Call a setting that not bind')
MyIncrementer['MySecondInt']=3

#Call a setting that not bind
print('')
print('Call a setting that binds')
MyIncrementer['Int']=4

#Print finally
print('MyIncrementer is finally')
print(MyIncrementer)

#set a binding method externally of the definition of the class
def setMyStr(_InstanceVariable):
	_InstanceVariable.MyStr='Int is equal to '+str(_InstanceVariable.Int)+' here'
MyIncrementer.__class__.setMyStr=Triggerer.TriggererClass(
								**{'TriggeringConditionVariable':[('SettingKeyVariable',(operator.eq,"Int"))]}
								)(setMyStr)
MyIncrementer.setMyStr()

#Call a setting that not bind
print('')
print('Call a setting that binds')
MyIncrementer['Int']=6

#Print finally
print('MyIncrementer is finally')
print(MyIncrementer)
