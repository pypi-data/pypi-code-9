# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Switcher decorates a method for making it like a unique calling method.
If we want to swith on again the method, the Switched<DoneStr>Bool needs to be 
setted again to False.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Functers.Functer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
from ShareYourSystem.Standards.Classors import Doer,Representer
from ShareYourSystem.Functers import Functer,Triggerer,Hooker
#</ImportSpecificModules>

#<DefineLocals>
SwitchingBeforeStr='Before'
SwitchingAfterStr='After'
SwitchingBindStr='trigger'
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class SwitcherClass(BaseClass):

	def default_init(self,
						_SwitchingFunction=None, 				
						_SwitchedFunction=None,				
						_SwitchedFunctionStr="", 				
						_SwitchedBoolSuffixStr="", 			
						_SwitchedClassBoolKeyStr="", 			
						_SwitchedInstanceBoolKeyStr="", 		
						**_KwargVariablesDict
				):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Variable):

		#Switch
		self.switch(_Variable)

		#Link
		self.FunctedFunction=self.SwitchedFunction

		#Call the call of the parent class
		return BaseClass.__call__(self,self.SwitchingFunction)

	def switch(self,_Variable=None):

		#set the switching Function
		if self.SwitchingFunction==None:
			self.SwitchingFunction=_Variable

		#set the SwitchedFunctionStr this is the functing function..and we remove all the tagged Functer@ 
		self.SwitchedFunctionStr=self.SwitchingFunction.__name__.split(Functer.FunctingDecorationStr)[-1]

		#debug
		'''
		self.debug(('self.',self,['SwitchedFunctionStr']))
		'''

		#Cut the pre attributing part if there is one
		if Functer.FunctingAttributeStr in self.SwitchedFunctionStr:
			self.SwitchedFunctionStr=self.SwitchedFunctionStr.split(Functer.FunctingAttributeStr)[-1]
		SwitchedDoStr=self.SwitchedFunctionStr[0].upper()+self.SwitchedFunctionStr[1:]
		self.SwitchedBoolSuffixStr=SwitchedDoStr+'Bool'
		self.SwitchedInstanceBoolKeyStr='Switching'+self.SwitchedBoolSuffixStr
		self.SwitchedClassBoolKeyStr='SwitchedClass'+self.SwitchedBoolSuffixStr

		#debug
		'''
		self.debug(('self.',self,['SwitchedInstanceBoolKeyStr','SwitchedClassBoolKeyStr']))
		'''

		#Definition the SwitchedFunction
		def SwitchedFunction(*_LiargVariablesList,**_KwargVariablesDict):

			#Alias
			InstanceVariable=_LiargVariablesList[0]

			#debug
			'''
			self.debug(
						[
							('self.',self,['SwitchedClassBoolKeyStr','SwitchedInstanceBoolKeyStr']),
							Representer.represent(InstanceVariable,**{'RepresentingAlineaIsBool':False})
						]
					)
			'''

			#set the SwitchedBool if it was not already
			if hasattr(InstanceVariable,self.SwitchedInstanceBoolKeyStr)==False:

				#debug
				'''
				self.debug('The InstanceVariable has not the SwitchedBoolSuffixStr..so set it to False')
				'''

				#set
				InstanceVariable.__setattr__(self.SwitchedInstanceBoolKeyStr,False)

			elif getattr(InstanceVariable,self.SwitchedInstanceBoolKeyStr):

				#debug
				'''
				self.debug('The Instance has already done this method')
				'''

				#Return
				return InstanceVariable

			#debug
			'''
			self.debug(('self.',self,['SwitchedBoolSuffixStr']))
			'''

			#At the level of the class set the new triggering set function
			if hasattr(InstanceVariable.__class__,self.SwitchedClassBoolKeyStr)==False:	

				#Definition the SwitchedDoerStr
				SwitchedDoerStr=Doer.getDoerStrWithDoStr(
					SwitchedDoStr
				)

				
				
				#debug
				'''
				print('SwitchedDoerStr is ',SwitchedDoerStr)
				print(InstanceVariable.__class__.__mro__)
				print('')
				'''

				#Find the corresponding base class to reinit
				SwitchedDoerClass=SYS._filter(
						lambda _Class:
						SwitchedDoerStr==SYS.getNameStrWithClassStr(_Class.__name__),
						InstanceVariable.__class__.__mro__
					)[0]
					
				#Definition the triggering function that will call the init one
				def triggerBefore(*_TriggeringVariablesList,**_TriggeringVariablesDict):

					#Alias
					TriggeredInstanceVariable=_TriggeringVariablesList[0]

					#debug
					'''
					self.debug('Reinit with '+Representer.represent(
						TriggeredInstanceVariable.SettingKeyVariable,**{'RepresentingAlineaIsBool':False}
						)
					)
					'''

					#Update with the DoneAttributeVariablesOrderedDict
					map(
							lambda __ItemTuple:
							TriggeredInstanceVariable.__setattr__(__ItemTuple[0],__ItemTuple[1]),
							SwitchedDoerClass.DoneAttributeVariablesOrderedDict.items()
						)
					

				#set the name
				TriggeredBeforeMethodStr='triggerBeforeWith'+self.SwitchedBoolSuffixStr
				triggerBefore.__name__=TriggeredBeforeMethodStr

				#debug
				'''
				self.debug(
							[
								("self.",self,['SwitchedDoneFunctionStr','SwitchedBoolSuffixStr']),
								("TriggeredMethodStr is "+TriggeredMethodStr)
							]
						)
				'''

				#Link the triggerBefore function
				setattr(
							InstanceVariable.__class__,
							TriggeredBeforeMethodStr,
							Triggerer.TriggererClass(**
								{
									'TriggeringConditionVariable':[
															(
																'SettingKeyVariable',
																(operator.eq,self.SwitchedInstanceBoolKeyStr)
															),
															(
																self.SwitchedInstanceBoolKeyStr,
																(operator.eq,True)
															),
															('SettingValueVariable',(operator.eq,False))
														],
									'TriggeringHookStr':"Before"
								}
							)(triggerBefore)
						)

				#Call with a default instance this trigger function to be installed
				getattr(InstanceVariable.__class__(),TriggeredBeforeMethodStr)()

				#Say that it is ok
				setattr(InstanceVariable.__class__,self.SwitchedClassBoolKeyStr,True)
				
			#debug
			'''
			self.debug(
						[
							#('InstanceVariable is '+SYS._str(InstanceVariable)),
							('_LiargVariablesList is '+str(_LiargVariablesList))
						]
					)
			'''

			#Call the SwitchingFunction
			self.SwitchingFunction(*_LiargVariablesList,**_KwargVariablesDict)

			#debug
			'''
			self.debug(('self.',self,['SwitchedBoolSuffixStr']))
			'''

			#set True for the Bool after the call
			InstanceVariable.__setattr__(self.SwitchedInstanceBoolKeyStr,True)

			#debug
			'''
			self.debug(('InstanceVariable.',InstanceVariable,[self.SwitchedBoolSuffixStr]))
			'''

			#Return self for the wrapped method call
			return InstanceVariable

		#set
		self.SwitchedFunction=SwitchedFunction

		#Return self
		return self

#</DefineClass>

