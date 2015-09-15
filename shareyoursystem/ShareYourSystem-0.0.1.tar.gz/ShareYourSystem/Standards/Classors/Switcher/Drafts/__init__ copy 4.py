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
BaseModuleStr="ShareYourSystem.Standards.Classors.Tester"
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
									'SwitchingMethodFunction', 				
									'SwitchedFunction',				
									'SwitchedFunctionStr', 				
									'SwitchedBoolSuffixStr', 			
									'SwitchedClassBoolKeyStr', 			
									'SwitchedInstanceBoolKeyStr', 	
								]

	def default_init(self,
						_SwitchingMethodFunction=None, 				
						_SwitchedFunction=None,				
						_SwitchedFunctionStr="", 				
						_SwitchedBoolSuffixStr="", 			
						_SwitchedClassBoolKeyStr="", 			
						_SwitchedInstanceBoolKeyStr="", 		
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
		'''
		self.debug(('self.',self,['SSwitchingMethodFunction']))
		'''

		#set the SwitchedFunctionStr this is the functing function..and we remove all the tagged Functer@ 
		self.SwitchedFunctionStr=self.SwitchingMethodFunction.__name__.split(
			Functer.FunctingDecorationStr)[-1]

		#debug
		'''
		self.debug(('self.',self,['SwitchedFunctionStr']))
		'''

		#Cut the pre attributing part if there is one
		if Functer.FunctingAttributeStr in self.SwitchedFunctionStr:
			self.SwitchedFunctionStr=self.SwitchedFunctionStr.split(
				Functer.FunctingAttributeStr
			)[-1]

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
		self.SwitchedInstanceBoolKeyStr='Switching'+self.SwitchedBoolSuffixStr
		self.SwitchedClassBoolKeyStr='SwitchedClass'+self.SwitchedBoolSuffixStr


		#debug
		'''
		self.debug(
			('self.',self,[
				'SwitchedInstanceBoolKeyStr',
				'SwitchedClassBoolKeyStr'
			]))
		'''

		#Definition the SwitchedFunction
		def SwitchedFunction(*_LiargVariablesList,**_KwargVariablesDict):

			#debug
			'''
			self.debug('We are in the SwitchedFunction !')
			'''

			#Alias
			InstanceVariable=_LiargVariablesList[0]

			#set at the class level
			SwitchedClass=InstanceVariable.__class__

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

				#debug
				'''
				self.debug('SwitchedClass is '+str(SwitchedClass))
				'''

				#set
				setattr(SwitchedClass,self.SwitchedInstanceBoolKeyStr,False)

				#set at the instance level
				InstanceVariable.__setattr__(self.SwitchedInstanceBoolKeyStr,False)

				#set also at the scale of 

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
			if hasattr(SwitchedClass,self.SwitchedClassBoolKeyStr)==False:	

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
						lambda __Class:
						SwitchedDoerStr==SYS.getNameStrWithClassStr(__Class.__name__),
						SwitchedClass.__mro__
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
							SwitchedClass,
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
				getattr(SwitchedClass(),TriggeredBeforeMethodStr)()

				#Say that it is ok
				setattr(SwitchedClass,self.SwitchedClassBoolKeyStr,True)
				
			#debug
			'''
			self.debug(
						[
							#('InstanceVariable is '+SYS._str(InstanceVariable)),
							('_LiargVariablesList is '+str(_LiargVariablesList)),
							('_KwargVariablesDict is '+str(_KwargVariablesDict))
						]
					)
			'''

			#Call the SwitchingMethodFunction
			self.SwitchingMethodFunction(*_LiargVariablesList,**_KwargVariablesDict)

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
		#return self

#</DefineClass>

