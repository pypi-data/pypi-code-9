# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Commander gather Variables to set them with an UpdateList.
The command process can be AllSetsForEach (ie a map of the update succesively for each)
or a EachSetForAll (ie each set is a map of each).

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Pather"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Itemizers import Getter,Setter
#</ImportSpecificModules>

#<DefineLocals>
CommandPrefixStr="--"
CommandWalkStr="..."
CommandSelfStr="/"
CommandAddStr="+"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class CommanderClass(BaseClass):

	def default_init(
				self,
				_CommandingGetVariable=None,
				_CommandingSetVariable=None,	
				_CommandingOrderStr="AllSetsForEachGet",
				_CommandingBeforeWalkRigidBool=False,	
				_CommandingAfterWalkRigidBool=False,	
				_CommandingBeforeSelfRigidBool=False,
				_CommandingAfterSelfRigidBool=False,		
				**_KwargVariablesDict
			):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_command(self):
		""" """

		#/####################/#
		# Adapt the type for getting things to command
		#

		#debug
		'''
		self.debug(
			[
				'Adapt the type for getting things to command',
				("self.",self,[
								'CommandingGetVariable',
								'CommandingSetVariable'
							])
			]
		)
		'''

		#Check
		if type(self.CommandingGetVariable)!=list:
			
			#debug
			'''
			self.debug(
				[
					'We get nicely',
					('self.',self,['CommandingGetVariable'])
				]
			)
			'''

			#get
			CommandedValueVariablesList=self[
				self.CommandingGetVariable
			]

			#Check
			if type(CommandedValueVariablesList)!=list:
				CommandedValueVariablesList=[CommandedValueVariablesList]

		else:

			#map a get
			CommandedValueVariablesList=map(
					lambda __CommandingGetVariable:
					self[__CommandingGetVariable],
					self.CommandingGetVariable
				)

		#flat maybe
		CommandedValueVariablesList=SYS.flat(CommandedValueVariablesList)

		#filter
		CommandedValueVariablesList=SYS.filterNone(CommandedValueVariablesList)

		#debug
		'''
		self.debug(
				[
					'in the end, CommandedValueVariablesList is ',
					SYS._str(CommandedValueVariablesList)
				]
			)
		'''
		
		#/###################/#
		# Check if we have to walk before
		#

		#Check
		if self.CommandingBeforeWalkRigidBool:

			#debug
			'''
			self.debug(
				[
					'we are going to walk before the command',
					'CommandedValueVariablesList is '+SYS._str(CommandedValueVariablesList),
					'self.getDoing(SYS.CommanderClass).values() is '+SYS._str
					(self.getDoing(
						SYS.CommanderClass).values())
				]
			)
			'''

			#Debug
			'''
			for __CommandedValueVariable in CommandedValueVariablesList:

				#debug
				self.debug(
					'__CommandedValueVariable is '+SYS._str( __CommandedValueVariable)
				)

				#set
				__CommandedValueVariable.set(
							'GettingNewBool',False
						).command(
							*self.getDoing().values()	
						).set(
							'GettingNewBool',True
						)
			'''

			#set
			CommandedOrderedDict=self.getDoing(
									SYS.CommanderClass
								)
			CommandedOrderedDict['CommandingBeforeSelfRigidBool']=False
			CommandedLiargVariablesList=CommandedOrderedDict.values()

			#map the recursion but pay watch to not set new things to walk in...it is an infinite walk either !
			map(
					lambda __CommandedValueVariable:
					__CommandedValueVariable.set(
							'GettingNewBool',False
						).command(
							*CommandedLiargVariablesList	
						).set(
							'GettingNewBool',True
						),
					CommandedValueVariablesList
				)

		#/####################/#
		# Adapt the type for setting things in the commanded variables
		#

		#debug
		'''
		self.debug(
			[
				'Adapt the type for setting things in the commanded variables',
				("self.",self,['CommandingSetVariable'])
			]
		)
		'''

		#Check
		if type(self.CommandingSetVariable)!=list:
			
			#Check
			if hasattr(self.CommandingSetVariable,'items'):

				#items
				CommandedSetVariablesList=self.CommandingSetVariable.items()

			elif type(self.CommandingSetVariable
				)==str and self.CommandingSetVariable.startswith(
					Getter.GetCallPrefixStr
				):

				#list
				CommandedSetVariablesList=[
					('get',self.CommandingSetVariable)
				]

			else:

				#list
				CommandedSetVariablesList=[
					self.CommandingSetVariable
				]

		else:

			#alias
			CommandedSetVariablesList=self.CommandingSetVariable

		#debug
		'''
		self.debug(
				[
					'in the end, CommandedSetVariablesList is ',
					SYS._str(CommandedSetVariablesList)
				]
			)
		'''

		#/###################/#
		# Ok now we command locally
		#

		#Check
		if self.CommandingBeforeSelfRigidBool:

			#debug
			'''
			self.debug(
					'We command before self here'
				)
			'''

			#add
			self[Setter.SetMapStr](CommandedSetVariablesList)

		#Check for the order
		if self.CommandingOrderStr=="AllSetsForEachGet":

			#map
			map(
					lambda __CommandedValueVariable:
					map(
						lambda __CommandedSetVariable:
						__CommandedValueVariable.set(
							*__CommandedSetVariable
						),
						CommandedSetVariablesList
					),
					CommandedValueVariablesList
				)

		elif self.CommandingOrderStr=="EachSetForAllGets":

			#map
			map(
					lambda __CommandedSetVariable:
					map(
						lambda __CommandedValueVariables:
						__CommandedValueVariables.set(
							*__CommandedSetVariable
						),
						CommandedValueVariablesList
					),
					CommandedSetVariablesList
				)

		#Check
		if self.CommandingAfterSelfRigidBool:

			#debug
			'''
			self.debug(
					'We command after self here'
				)
			'''

			#add
			self[Setter.SetMapStr](CommandedSetVariablesList)

		#/###################/#
		# And we check for a walk after
		#

		#Check
		if self.CommandingAfterWalkRigidBool:

			#debug
			'''
			self.debug(
				[
					'we are going to walk the command',
					'CommandedValueVariablesList is '+SYS._str(CommandedValueVariablesList)
				]
			)
			'''
			
			#Debug
			'''
			for __CommandedValueVariable in CommandedValueVariablesList:

				#debug
				self.debug(
					'__CommandedValueVariable is '+SYS._str( __CommandedValueVariable)
				)

				#set
				__CommandedValueVariable.set(
							'GettingNewBool',False
						).command(
							*self.getDoing().values()	
						).set(
							'GettingNewBool',True
						)
			'''

			#set
			CommandedOrderedDict=self.getDoing(
									SYS.CommanderClass
								)
			CommandedOrderedDict['CommandingBeforeSelfRigidBool']=False
			CommandedLiargVariablesList=CommandedOrderedDict.values()

			#map the recursion but pay watch to not set new things to walk in...it is an infinite walk either !
			map(
					lambda __CommandedValueVariable:
					__CommandedValueVariable.set(
							'GettingNewBool',False
						).command(
							*CommandedLiargVariablesList	
						).set(
							'GettingNewBool',True
						),
					CommandedValueVariablesList
				)

	def mimic_get(self):

		#debug
		'''
		self.debug(
				('self.',self,[
						'GettingKeyVariable',
					])
			)
		'''

		#Check
		if type(self.GettingKeyVariable)==str:

			#Check
			if self.GettingKeyVariable.startswith(CommandAddStr):

				#split
				AddGetKeyStrsList=self.GettingKeyVariable.split(CommandAddStr)[1:]

				#debug
				'''
				self.debug(
					[
						'We map get',
						'AddGetKeyStrsList is '+str(AddGetKeyStrsList) 
					]
				)
				'''
				
				#map get
				AddVariablesList=self[
						Getter.GetMapStr
					](*AddGetKeyStrsList).ItemizedMapValueVariablesList

				#debug
				'''
				self.debug(
					[
						'We sum now',
						'AddVariablesList is '+SYS._str(AddVariablesList) 
					]
				)	
				'''

				#map get
				self.GettedValueVariable=SYS.sum(AddVariablesList)

				#return
				return {'HookingIsBool':False}

		#return
		return BaseClass.get(self)


	def mimic_set(self):

		#debug
		'''
		self.debug(
				('self.',self,[
						'SettingKeyVariable',
						'SettingValueVariable'
					])
			)
		'''

		#Check
		if type(self.SettingKeyVariable)==str:

			#Check
			if self.SettingKeyVariable.startswith(
				CommandPrefixStr
			):

				#debug
				'''
				self.debug(
						'We command here'
					)
				'''

				#deprefix
				CommandGetKeyStr=SYS.deprefix(
					self.SettingKeyVariable,
					CommandPrefixStr
				)
				
				#Check
				if CommandGetKeyStr.startswith(CommandWalkStr):

					#debug
					'''
					self.debug(
							'We command-walk here'
						)
					'''

					#command
					self.command(
						SYS.deprefix(
							CommandGetKeyStr,
							CommandWalkStr
						),
						self.SettingValueVariable,
						_AfterWalkRigidBool=True
					)

					#stop the setting
					return {'HookingIsBool':False}

				elif CommandGetKeyStr.startswith(CommandSelfStr+CommandWalkStr):

					#debug
					'''
					self.debug(
							'We command-self-walk here'
						)
					'''

					#command
					self.command(
						SYS.deprefix(
							CommandGetKeyStr,
							CommandSelfStr+CommandWalkStr
						),
						self.SettingValueVariable,
						_AfterWalkRigidBool=True,
						_SelfBool=True
					)

					#stop the setting
					return {'HookingIsBool':False}

				else:

					#command
					self.command(
						CommandGetKeyStr,
						self.SettingValueVariable
					)

					#stop the setting
					return {'HookingIsBool':False}

			#Check
			elif self.SettingKeyVariable.startswith(
				CommandWalkStr
			):

				#debug
				'''
				self.debug(
						'We walk-command here'
					)
				'''

				CommandGetKeyStr=SYS.deprefix(
						self.SettingKeyVariable,
						CommandWalkStr
					)

				#Check
				if CommandGetKeyStr.startswith(CommandPrefixStr):

					#command
					self.command(
						SYS.deprefix(
							CommandGetKeyStr,
							CommandPrefixStr
						),
						self.SettingValueVariable,
						_BeforeWalkRigidBool=True
					)

					#stop the setting
					return {'HookingIsBool':False}

				elif CommandGetKeyStr.startswith(CommandSelfStr):

					#command
					self.command(
						SYS.deprefix(
							CommandGetKeyStr,
							CommandSelfStr+CommandPrefixStr
						),
						self.SettingValueVariable,
						_BeforeWalkRigidBool=True,
						_AfterSelfRigidBool=True
					)

					#stop the setting
					return {'HookingIsBool':False}

			#Check
			elif self.SettingKeyVariable.startswith(
				CommandSelfStr+CommandWalkStr+CommandPrefixStr
			):

				#command
				self.command(
					SYS.deprefix(
						self.SettingKeyVariable,
						CommandSelfStr+CommandWalkStr+CommandPrefixStr
					),
					self.SettingValueVariable,
					_BeforeWalkRigidBool=True,
					_BeforeSelfRigidBool=True
				)

				#stop the setting
				return {'HookingIsBool':False}

		#debug
		'''
		self.debug(
				[
					'Call the base set method',
					'BaseClass is '+str(BaseClass),
					('self.',self,['SettingKeyVariable'])
				]
			)
		'''
		
		#Call the base method
		BaseClass.set(self)

#</DefineClass>


#</DefinePrint>
CommanderClass.PrintingClassSkipKeyStrsList.extend(
	[
		'CommandingGetVariable',
		'CommandingSetVariable',
		'CommandingOrderStr',
		'CommandingBeforeWalkRigidBool',
		'CommandingAfterWalkRigidBool',
		'CommandingBeforeSelfRigidBool',
		'CommandingAfterSelfRigidBool'
	]
)
#<DefinePrint>