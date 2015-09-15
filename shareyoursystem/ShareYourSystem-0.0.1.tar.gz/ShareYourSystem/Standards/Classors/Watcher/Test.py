import operator
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Classors import Watcher
from ShareYourSystem.Functers import Hooker,Triggerer
from ShareYourSystem.Standards.Objects import Setter
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Watcher.WatcherClass.__dict__.items()))

#Print a version of this object
_print(Watcher.WatcherClass())

#Print a version of his __dict__
_print(Watcher.WatcherClass().__dict__)

#Test
@Watcher.WatcherClass()
class IncrementerClass(Setter.SetterClass):

	def default_init(self):
		self.Int=0
		Setter.SetterClass.__init__(self)

	def printIncrement(self):

		#Print finally
		self.debug(
					('self.',self,['Int'])
				)

	@Hooker.HookerClass(**{'HookingBeforeVariablesList':[{'CallingMethodStr':"printIncrement"}]})
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
print("Get an instance and set a default Int that will be already be binded")

#print(IncrementerClass.increment)
MyIncrementer=IncrementerClass().__setitem__('Int',3)




