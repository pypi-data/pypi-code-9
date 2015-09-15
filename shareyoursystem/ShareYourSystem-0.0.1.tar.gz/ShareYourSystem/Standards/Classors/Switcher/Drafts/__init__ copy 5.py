# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Switcher 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Binder"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator

from ShareYourSystem.Standards.Classors import Doer,Representer
#</ImportSpecificModules>

#<DefineLocals>
SwitchingBeforeStr='Before'
SwitchingAfterStr='After'
SwitchingBindStr='trigger'
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class SwitcherClass(BaseClass):

	#Definition 
	RepresentingKeyStrsList=[
							'SwitchingUnboundMethodStr', 				
	]

	def default_init(self,
						_SwitchingUnboundMethodStr="", 						
						**_KwargVariablesDict
				):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#Call the parent init method
		BaseClass.__call__(self,_Class)

		#switch
		self.switch()

		#Return
		return _Class

	def do_switch(self):

		#get
		self.SwitchingMethodFunction=getattr(self.DoClass,self.SwitchingMethodStr)

		#debug
		self.debug(('self.',self,['SwitchingMethodFunction']))

		#set the SwitchedFunctionStr this is the functing function..and we remove all the tagged Functer@ 
		self.SwitchedFunctionStr=self.SwitchingMethodFunction.__name__.split(
			Functer.FunctingDecorationStr)[-1]

		#debug
		'''
		self.debug(('self.',self,['SwitchedFunctionStr']))
		'''

		#Check
		if self.SwitchedFunctionStr.startswith(Doer.DoingDoMethodStr):
			self.SwitchedFunctionStr=Doer.DoingDoMethodStr.join(
				self.SwitchedFunctionStr.split(Doer.DoingDoMethodStr)[1:])

		#Definition
		SwitchedDoStr=self.SwitchedFunctionStr[0].upper(
			)+self.SwitchedFunctionStr[1:]

		#Debug
		'''
		print('SwitchedDoStr is ',SwitchedDoStr)
		print('')
		'''

		#Set
		self.SwitchedBoolSuffixStr=SwitchedDoStr+'Bool'
		self.SwitchedInstanceBoolKeyStr='Switch'+self.SwitchedBoolSuffixStr

		#debug
		'''
		self.debug(
			('self.',self,[
				'SwitchedInstanceBoolKeyStr'
			]))
		'''

		#Definition the SwitchedFunction
		def SwitchedFunction(
				*_LiargVariablesList,
				**_KwargVariablesDict
			):

			#debug
			'''
			self.debug('We are in the SwitchedFunction !')
			'''

			#Alias
			InstanceVariable=_LiargVariablesList[0]

			#debug
			'''
			self.debug(
						[
							('self.',self,['SwitchedInstanceBoolKeyStr']),
							Representer.represent(InstanceVariable,**{'RepresentingAlineaIsBool':False})
						]
					)
			'''

			if hasattr(InstanceVariable,self.SwitchedInstanceBoolKeyStr)==False:

				#set at the instance level
				InstanceVariable.__setattr__(self.SwitchedInstanceBoolKeyStr,False)

			elif getattr(InstanceVariable,self.SwitchedInstanceBoolKeyStr):

				#debug
				'''
				self.debug('The Instance has already done this method')
				'''

				#Return
				return InstanceVariable

			#Call the SwitchingMethodFunction
			self.SwitchingMethodFunction(*_LiargVariablesList,**_KwargVariablesDict)

			#set True for the Bool after the call
			InstanceVariable.__setattr__(self.SwitchedInstanceBoolKeyStr,True)

			#debug
			'''
			self.debug(('InstanceVariable.',InstanceVariable,[self.SwitchedBoolSuffixStr]))
			'''

			#Return self for the wrapped method call
			return InstanceVariable


		#Definition the SwitchedDoerStr
		SwitchedDoerStr=Doer.getDoerStrWithDoStr(
			SwitchedDoStr
		)

		#debug
		'''
		print('SwitchedDoerStr is ',SwitchedDoerStr)
		print('')
		'''
		
		#Find the corresponding base class to reinit
		SwitchedDoerClass=SYS._filter(
				lambda __MroClass:
				SwitchedDoerStr==SYS.getNameStrWithClassStr(__MroClass.__name__),
				self.DoClass.__mro__
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
						("SwitchedClass is "+str(SwitchedClass)),
						("TriggeredBeforeMethodStr is "+TriggeredBeforeMethodStr),
						("Get Method is "+str(getattr(
							SwitchedClass,
							TriggeredBeforeMethodStr)
						) if hasattr(SwitchedClass,
							TriggeredBeforeMethodStr) else "None")
					]
				)
		'''
		
		#Link the triggerBefore function
		setattr(
					self.DoClass,
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

		#Return self
		#return self

#</DefineClass>

