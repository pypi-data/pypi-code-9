#<ImportSpecificModules>
import operator

,Doer,Representer
from ShareYourSystem.Functers import Functer,Triggerer,Hooker
BaseModuleStr="ShareYourSystem.Functers.Functer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer")
#</ImportSpecificModules>

#<DefineLocals>
SYS.setSubModule(globals())

SwitchingBeforeStr='Before'
SwitchingAfterStr='After'
SwitchingBindStr='bind'
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class SwitcherClass(BaseClass):

	def default_init(self,**_KwargVariablesDict):
		
		#<DefineSpecificDo>
		self.SwitchingFunction=None 				#<NotRepresented>
		self.SwitchedFunction=None					#<NotRepresented>
		self.SwitchedFunctionStr="" 				#<NotRepresented>
		self.SwitchedBoolSuffixStr="" 			#<NotRepresented>
		self.SwitchedClassBoolKeyStr="" 			#<NotRepresented>	
		self.SwitchedInstanceBoolKeyStr="" 		#<NotRepresented>
		#</DefineSpecificDo>

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

			#At the level of the class set the new binding set function
			if hasattr(InstanceVariable.__class__,self.SwitchedClassBoolKeyStr)==False:	

				#Definition the SwitchedDoerStr
				SwitchedDoerStr=Doer.getDoerStrWithDoStr(
					SwitchedDoStr
				)

				
				
				#debug
				print('SwitchedDoerStr is ',SwitchedDoerStr)
				print(InstanceVariable.__class__.__mro__)
				print('')

				#Find the corresponding base class to reinit
				SwitchedDoerClass=SYS._filter(
						lambda _Class:
						SwitchedDoerStr==Classor.getNameStrWithClassStr(_Class.__name__),
						InstanceVariable.__class__.__mro__
					)[0]
					
				#Definition the binding function that will call the init one
				def bindBefore(*_TriggeringVariablesList,**_TriggeringVariablesDict):

					#Alias
					TriggeredInstanceVariable=_TriggeringVariablesList[0]

					#debug
					'''
					self.debug('Reinit with '+Representer.represent(
						TriggeredInstanceVariable.SettingKeyVariable,**{'RepresentingAlineaIsBool':False}
						)
					)
					'''


					"""
					FIRST METHOD

					#Definition the init method to trigger
					SwitchedInitMethod=Functer.getFunctingFunctionWithFuncFunction(
						SwitchedDoerClass.init
					)

					#debug
					'''
					self.debug(
								[
									'SwitchedInitMethod is '+str(SwitchedInitMethod),
									"SwitchedInitMethod.func_globals['__file__'] is "+SwitchedInitMethod.func_globals['__file__']
								]
							)
					'''

					#Call the init method (just at the level of this class definition) (so IMPORTANT this is init not __init__)
					SwitchedInitMethod(TriggeredInstanceVariable)

					"""

				#set the name
				TriggeredBeforeMethodStr='bindBeforeWith'+self.SwitchedBoolSuffixStr
				bindBefore.__name__=TriggeredBeforeMethodStr

				#debug
				'''
				self.debug(
							[
								("self.",self,['SwitchedDoneFunctionStr','SwitchedBoolSuffixStr']),
								("TriggeredMethodStr is "+TriggeredMethodStr)
							]
						)
				'''

				#Link the bindBefore function
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
							)(bindBefore)
						)

				#Call with a default instance this bind function to be installed
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

