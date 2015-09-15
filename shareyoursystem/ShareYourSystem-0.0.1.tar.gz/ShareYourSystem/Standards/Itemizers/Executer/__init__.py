# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


An Executer can exec commands with the six.exec_ function
"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Setter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import six
Setter=BaseModule
from ShareYourSystem.Standards.Itemizers import Getter
#</ImportSpecificModules>

#<DefineLocals>
ExecutionPrefixStr=">>"
ExecutionDotStr="."
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ExecuterClass(BaseClass):

	def default_init(self,
				_ExecutingCodeStr="" ,
				_ExecutedLocalsDict=None,
				**_KwargVariablesDict):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_execute(self):

		#debug
		'''
		self.debug(
			[
				'We execute here',
				('self.',self,[
						'ExecutingCodeStr'
					])
			]
		)
		'''
		
		#give the sys
		locals()['SYS']=SYS

		#Execute
		six.exec_(
			self.ExecutingCodeStr,
			locals()
		)

		#alias
		self.ExecutedLocalsDict=locals()

	def mimic_get(self):

		#debug
		'''
		self.debug(
				('self.',self,['GettingKeyVariable'])
			)
		'''

		#Check
		if type(self.GettingKeyVariable
			)==str:

			#Check
			if self.GettingKeyVariable.startswith(ExecutionPrefixStr):

				#deprefix
				ExecutedStr="ExecutedVariable="+SYS.deprefix(
							self.GettingKeyVariable,
							ExecutionPrefixStr
						)

				#debug
				'''
				self.debug('ExecutedStr is '+ExecutedStr)
				'''

				#execute
				self.execute(
						ExecutedStr
					)

				#alias
				self.GettedValueVariable=self.ExecutedLocalsDict['ExecutedVariable']

				#stop the getting
				return {'HookingIsBool':False}

			elif self.GettingKeyVariable.startswith(
					Getter.GetDirectPrefixStr
				)==False and ExecutionDotStr in self.GettingKeyVariable:

				#debug
				'''
				self.debug(
					[
						'we get an attribute of the GettingKeyVariable',
						[('self.',self,['GettingKeyVariable'])]
					]
				)
				'''
				
				#previous
				GetKeyStr,AttributeStr=SYS.previous(
							self.GettingKeyVariable,
							ExecutionDotStr
						)

				#debug
				'''
				self.debug(
					[
						'GetKeyStr is '+GetKeyStr,
						'AttributeStr is '+AttributeStr,
						'self is '+SYS._str(self)
					]
				)
				'''
				
				#get
				GetValueVariable=self[GetKeyStr]

				#debug
				'''
				self.debug(
					[
						'GetValueVariable is '+SYS._str(GetValueVariable)
					]
				)
				'''

				#get the get
				AttributeValueVariable=getattr(
						GetValueVariable,
						AttributeStr	
					)

				#debug
				'''
				self.debug(
						[
							('self.',self,['GettingKeyVariable']),
							'GetValueVariable is '+SYS._str(GetValueVariable),
							'AttributeValueVariable is '+SYS._str(AttributeValueVariable)
						]
					)
				'''

				#call
				if callable(AttributeValueVariable):

					#get the method and call it
					self.GettedValueVariable=AttributeValueVariable()

				else:

					#alias
					self.GettedValueVariable=AttributeValueVariable

				#stop the setting
				return {'HookingIsBool':False}


		#call the base method
		BaseClass.get(self)

	def mimic_set(self):

		#Check
		if type(self.SettingValueVariable
			)==str:

			#/####################/#
			# Case of a call of an execution str
			#

			#Check
			if self.SettingValueVariable.startswith(ExecutionPrefixStr):

				#debug
				'''
				self.debug('we execute here')
				'''

				#deprefix
				ExecutedStr="ExecutedVariable="+SYS.deprefix(
							self.SettingValueVariable,
							ExecutionPrefixStr
						)

				#debug
				'''
				self.debug('ExecutedStr is '+ExecutedStr)
				'''

				#execute
				self.execute(
					ExecutedStr
				)

				#alias
				self[self.SettingKeyVariable]=self.ExecutedLocalsDict['ExecutedVariable']

				#stop the getting
				return {'HookingIsBool':False}

		#/####################/#
		# Case of a call of a method of a child object
		#

		#Check
		if type(
				self.SettingKeyVariable
			)==str:

			#Check
			if ExecutionDotStr in self.SettingKeyVariable:

				#debug
				'''
				self.debug('we get an attribute of the SettingKeyVariable')
				'''

				#previous
				GetKeyStr,AttributeStr=SYS.previous(
							self.SettingKeyVariable,
							ExecutionDotStr
						)

				#debug
				'''
				self.debug(
						[
							'GetKeyStr is '+GetKeyStr,
							'AttributeStr is '+AttributeStr
						]
					)
				'''
				
				#get
				GetValueVariable=self[GetKeyStr]

				#get the get
				AttributeValueVariable=getattr(
						GetValueVariable,
						AttributeStr	
					)

				#debug
				'''
				self.debug(
						[
							'GetValueVariable is '+SYS._str(GetValueVariable),
							'AttributeValueVariable is '+SYS._str(AttributeValueVariable),
							('self.',self,['SettingValueVariable'])
						]
					)
				'''
				
				#call
				if callable(AttributeValueVariable):

					#debug
					'''
					self.debug(
						[
							'we set call',
							('self.',self,['SettingValueVariable']),
							'AttributeValueVariable is ',
							str(AttributeValueVariable)
						]
					)
					'''

					#Check
					if type(self.SettingValueVariable)==list and len(
						self.SettingValueVariable)>0 and hasattr(self.SettingValueVariable[0],'items'
						) and Setter.SetValueLambdaGrabStr in self.SettingValueVariable[0]:

							#get
							ExecutedMapLambdaList=self.getMapLambdaList(
								self.SettingValueVariable[0]
							)

							#debug
							self.debug(
								[
									'ExecutedMapLambdaList is ',
									SYS._str(ExecutedMapLambdaList)
								]
							)

							#set
							self[AttributeValueVariable]=[ExecutedMapLambdaList]

					else:
					
						#set
						self[AttributeValueVariable]=self.SettingValueVariable

						#get the method and call it
						#AttributeValueVariable(*LiargValueVariable)

				else:

					#alias
					AttributeValueVariable=LiargValueVariable

				#stop the setting
				return {'HookingIsBool':False}

		#Call the parent method
		BaseClass.set(self)

#</DefineClass>

#</DefinePrint>
ExecuterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ExecutingCodeStr',
		'ExecutedLocalsDict'
	]
)
#<DefinePrint>
