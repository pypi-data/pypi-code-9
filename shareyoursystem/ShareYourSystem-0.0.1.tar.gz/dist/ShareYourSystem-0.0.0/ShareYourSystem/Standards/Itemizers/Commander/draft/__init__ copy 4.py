# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Commander gather Variables to set them with an UpdateList.
The command process can be AllSetsForEach (ie a map of the update succesively for each)
or a EachSetForAll (ie each set is a map of each).
NOTE : the walk and self attributes are always resetted to False after a call of command.

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
				_CommandTopDeriveCommanderRigidVariable=None,
				_CommandingKeyVariable=None,
				_CommandingSetVariable=None,	
				_CommandingOrderStr="AllSetsForEachGet",
				_CommandingBeforeWalkRigidBool=False,	
				_CommandingAfterWalkRigidBool=False,	
				_CommandingBeforeSelfRigidBool=False,
				_CommandingAfterSelfRigidBool=False,
				_CommandingGetRigidBool=True,	
				_CommandingSetRigidBool=True,
				_CommandingSetAttrOrCallRigidBool=False,
				_CommandingExtraKeyVariable=None,
				_CommandedValueVariablesList=None,
				_CommandedSetVariablesList=None,
				_CommandedExtraValueVariablesList=None,
				**_KwargVariablesDict
			):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_command(self):
		""" """

		#/####################/#
		# Determine the top Commander
		#

		#debug
		'''
		self.debug(
			[
				'First determine the CommandTopDeriveCommanderRigidVariable',
				('self.',self,['CommandTopDeriveCommanderRigidVariable'])
			]
		)
		'''

		#Check
		if self.CommandTopDeriveCommanderRigidVariable==None:
			self.CommandTopDeriveCommanderRigidVariable=self

		#/####################/#
		# Adapt maybe the type for getting things to command
		#

		#Check
		if self.CommandingGetRigidBool:

			#debug
			'''
			self.debug(
				[
					'Adapt the type for getting things to command',
					("self.",self,[
									'CommandingKeyVariable',
									'CommandingSetVariable',
									'CommandingBeforeWalkRigidBool',
									'CommandingBeforeSelfRigidBool'
								])
				]
			)
			'''

			#init
			self.CommandedValueVariablesList=SYS.GetList(
				self.CommandingKeyVariable,
				self
			)

			#init
			self.CommandedExtraValueVariablesList=SYS.GetList(
				self.CommandingExtraKeyVariable,
				self
			)

		else:

			#init
			self.CommandedValueVariablesList=self.CommandingKeyVariable

			#init
			self.CommandedExtraValueVariablesList=self.CommandingExtraKeyVariable
	
		#debug
		'''
		self.debug(
				[
					('self.',self,['CommandingKeyVariable']),
					'in the end, self.CommandedValueVariablesList is ',
					SYS._str(self.CommandedValueVariablesList)
				]
			)
		'''


		#/###################/#
		# Inform the getted values who is the top
		#

		#debug
		'''
		self.debug(
			[
				'We inform the commanded values who is the top commander'
			]
		)	
		'''

		#map
		map(
			lambda __CommandedValueVariable:
			setattr(
				__CommandedValueVariable,
				'CommandTopDeriveCommanderRigidVariable',
				self.CommandTopDeriveCommanderRigidVariable
			),
			self.CommandedValueVariablesList
		)

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
					'before we setCommand'
				]
			)
			'''

			#set
			self.setCommand()

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

			#debug
			'''
			self.debug(
				[
					'Ok we can setAttr now'
				]
			)
			'''

			#map the recursion but pay watch to not set new things to walk in...it is an infinite walk either !
			map(
					lambda __CommandedValueVariable:
					__CommandedValueVariable.setAttr(
							'GettingNewBool',False
						).command(
						).setAttr(
							'GettingNewBool',True
						),
					self.CommandedValueVariablesList+self.CommandedExtraValueVariablesList
				)

		#/####################/#
		# Adapt maybe the type for setting things in the commanded variables
		#

		#Check
		if self.CommandingSetRigidBool:

			#debug
			'''
			self.debug(
				[
					'Adapt the type for setting things in the commanded variables',
					("self.",self,['CommandingSetVariable'])
				]
			)
			'''

			#inits
			self.CommandedSetVariablesList=SYS.SetList(self.CommandingSetVariable)

		else:

			#alias direct
			self.CommandedSetVariablesList=self.CommandingSetVariable

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
				[
					'We command before self here',
					('self.',self,[
							'CommandingSetRigidBool',
							'CommandingSetAttrOrCallRigidBool'
						])
				]
			)
			'''

			#Check
			if self.CommandingSetAttrOrCallRigidBool==False:

				#add
				self.mapSet(
					self.CommandedSetVariablesList
				)

			else:

				#add
				map(
					lambda __ElementVariable:
					self.setAttrOrCall(
						__ElementVariable
					),
					self.CommandedSetVariablesList
				)
				

		#Check for the order
		if self.CommandingOrderStr=="AllSetsForEachGet":

			#debug
			'''
			self.debug(
					[
						'Ok now we do a AllSetsForEachGet'
					]
				)
			'''
			
			#Debug
			"""
			for __CommandedValueVariable in CommandedValueVariablesList:

				#debug
				self.debug(
						[
							'__CommandedValueVariable is ',
							SYS._str(__CommandedValueVariable),
							'CommandedSetVariablesList is ',
							SYS._str(CommandedSetVariablesList)
						]
					)

				#map
				map(
						lambda __CommandedSetVariable:
						__CommandedValueVariable.set(
							*__CommandedSetVariable
						),
						CommandedSetVariablesList
					)
			"""

			#Check
			if self.CommandingSetAttrOrCallRigidBool:

				#debug
				'''
				self.debug(
					[
						'map a SetAttrOrCallBool',
						('self.',self,[
							'CommandedValueVariablesList',
							'CommandedSetVariablesList'
						])
					]
				)
				'''

				#map
				map(
						lambda __CommandedValueVariable:
						map(
							lambda __CommandedSetVariable:
							__CommandedValueVariable.setAttrOrCall(
								__CommandedSetVariable
							),
							self.CommandedSetVariablesList
						),
						self.CommandedValueVariablesList
					)

				#debug
				'''
				self.debug(
					[
						'Ok end of SetAttrOrCallBool'
					]
				)
				'''

			else:

				#debug
				'''
				self.debug(
					[
						'We call a map set',
						('self.',self,[
								'CommandedValueVariablesList',
								'CommandedSetVariablesList'
							])
					]
				)
				'''
				
				#map
				map(
						lambda __CommandedValueVariable:
						map(
							lambda __CommandedSetVariable:
							__CommandedValueVariable.set(
								*__CommandedSetVariable
							)
							if hasattr(__CommandedValueVariable,'set')
							else None,
							self.CommandedSetVariablesList
						),
						self.CommandedValueVariablesList
					)


		elif self.CommandingOrderStr=="EachSetForAllGets":

			#Check
			if self.CommandingSetAttrOrCallRigidBool:

				#map
				map(
						lambda __CommandedSetVariable:
						map(
							lambda __CommandedValueVariable:
							__CommandedValueVariable.setAttrOrCall(
								__CommandedSetVariable
							),
							self.CommandedValueVariablesList
						),
						self.CommandedSetVariablesList
					)

			else:

				#map
				map(
						lambda __CommandedSetVariable:
						map(
							lambda __CommandedValueVariable:
							__CommandedValueVariable.set(
								*__CommandedSetVariable
							),
							self.CommandedValueVariablesList
						),
						self.CommandedSetVariablesList
					)

		#Check
		if self.CommandingAfterSelfRigidBool:

			#debug
			self.debug(
					[
						'We command after self here'
					]
				)

			#Check
			if self.CommandingSetAttrOrCallRigidBool==False:

				#add
				self.mapSet(
					self.CommandedSetVariablesList
				)

			else:

				#add
				map(
					lambda __ElementVariable:
					self.setAttrOrCall(
						__ElementVariable
					),
					self.CommandedSetVariablesList
				)

		#/###################/#
		# And we check for a walk after
		#

		#Check
		if self.CommandingAfterWalkRigidBool:

			#debug
			'''
			self.debug(
				[
					'we are going to walk after the command',
					#'self.CommandedValueVariablesList is '+SYS._str(
					#	self.CommandedValueVariablesList),
					#('self.',self,['CommandingKeyVariable']),
					'We have to determine the things to propagate',
					'CommandingKeyVariable and CommandingSetVariable notably ',
					'if it is None in the commanded value"
				]
			)
			'''

			#set
			self.setCommand()

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

			#debug
			self.debug(
				[
					'Ok we can command now',
					('self.',self,[
							'CommandedValueVariablesList',
							'CommandedExtraValueVariablesList'
						])
				]
			)

			#map the recursion but pay watch to not set new things to walk in...it is an infinite walk either !
			map(
					lambda __CommandedValueVariable:
					__CommandedValueVariable.setAttr(
							'GettingNewBool',False
						).command(
						).setAttr(
							'GettingNewBool',True
						)
					if hasattr(
						__CommandedValueVariable,
						'command'
					)
					else None,
					self.CommandedValueVariablesList+self.CommandedExtraValueVariablesList
				)

		#/#######################/#
		# Reset always these values to False
		#

		#set
		self.CommandingBeforeWalkRigidBool=False	
		self.CommandingAfterWalkRigidBool=False
		self.CommandingBeforeSelfRigidBool=False
		self.CommandingAfterSelfRigidBool=False
		self.CommandingSetAttrOrCallRigidBool=False
		self.CommandingGetRigidBool=True	
		self.CommandingSetRigidBool=True
		self.CommandTopDeriveCommanderRigidVariable=None

		#debug
		'''
		self.debug(
			[
				'End of the command'
			]
		)
		'''

	def setCommand(self):

		#/##############/#
		# Get all the commanding attributes
		#

		#set
		CommandedOrderedDict=self.getDoing(
			SYS.CommanderClass
		)
		CommandedOrderedDict['CommandingBeforeSelfRigidBool']=False
		CommandedLiargVariablesList=CommandedOrderedDict.values()
		
		#/##############/#
		# Special get for KeyVariable and SetVariable
		#

		#get
		CommandedNewKeyVariable=CommandedLiargVariablesList[0]

		#get
		CommandedNewSetVariable=CommandedLiargVariablesList[1]

		#get
		CommandedNewTuplesList=zip(
			CommandedOrderedDict.keys()[2:],
			CommandedLiargVariablesList[2:]
		)

		#/##############/#
		# Map a setAttr
		#

		#map
		map(
			lambda __CommandedValueVariable:
			__CommandedValueVariable.setAttr(
				'CommandingKeyVariable',
				CommandedNewKeyVariable
			)
			if __CommandedValueVariable.CommandingKeyVariable==None
			else None,
			self.CommandedValueVariablesList
		)

		#map
		map(
			lambda __CommandedValueVariable:
			__CommandedValueVariable.setAttr(
				'CommandingSetVariable',
				CommandedNewSetVariable
			)
			if __CommandedValueVariable.CommandingSetVariable==None
			else None,
			self.CommandedValueVariablesList
		)

		#map
		map(
			lambda __CommandedValueVariable:
			__CommandedValueVariable.mapSetAttr(
				CommandedNewTuplesList
			),
			self.CommandedValueVariablesList
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
		'CommandTopDeriveCommanderRigidVariable',
		'CommandingKeyVariable',
		'CommandingSetVariable',
		'CommandingOrderStr',
		'CommandingBeforeWalkRigidBool',
		'CommandingAfterWalkRigidBool',
		'CommandingBeforeSelfRigidBool',
		'CommandingAfterSelfRigidBool',
		'CommandingGetRigidBool',	
		'CommandingSetRigidBool',
		'CommandingSetAttrOrCallRigidBool',
		'CommandingExtraKeyVariable',
		'CommandedValueVariablesList',
		'CommandedSetVariablesList',
		'CommandedLiargVariablesList',
		'CommandedExtraValueVariablesList'
	]
)
#<DefinePrint>