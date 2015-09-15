# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Connecter 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Parenter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Connecter','Connect','Connecting','Connected')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Interfacers import Printer
from ShareYourSystem.Standards.Itemizers import Pather,Teamer,Manager,Parenter
#</ImportSpecificModules>

#<DefineLocals>
ConnectKeyPrefixStr="*"
ConnectGetSetPrefixStr="->"
ConnectInTeamKeyStr="Inlets"
ConnectOutTeamKeyStr="Outlets"
ConnectConnectKeyStr='?>'
ConnectManagementPrefixStr='_p_'
def getLiargVariablesList(_ValueVariable):
	return _ValueVariable
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ConnecterClass(BaseClass):

	def default_init(
					self,
					_ConnectingKeyVariable=None,
					_ConnectingGetBool=True,
					_ConnectedToVariable=None,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_connect(self):

		#/####################/#
		# Get the connected variable
		#

		#debug
		'''
		self.debug(
			[
				'Adapt the type for getting things to connect',
				'(if we need to get)',
				("self.",self,[
								'ConnectingKeyVariable',
								'ConnectingGetBool',
							])
			]
		)
		'''
		
		#Check
		if self.ConnectingKeyVariable!=None:

			#Check
			if self.ConnectingGetBool:
			
				#init
				ConnectedValueVariable=self[self.ConnectingKeyVariable]

			else:

				#alias
				ConnectedValueVariable=self.ConnectingKeyVariable


			#debug
			'''
			self.debug(
					[
						'in the end, ConnectedValueVariable is ',
						SYS._str(ConnectedValueVariable)
					]
				)
			'''

			#/####################/#
			# Make it parent if it was not yet the case
			#

			#debug
			'''
			self.debug(
				[
					'We make the ConnectedValueVariable parentUp',
					'ConnectedValueVariable is ',
					SYS._str(ConnectedValueVariable),
					('ConnectedValueVariable.',ConnectedValueVariable,[
							'ParentedTotalPathStr'
						])
				]
			)
			'''

			#parentUp
			ConnectedValueVariable.parentUp()

			#debug
			'''
			self.debug(
				[
					'Ok it has connected',
					('ConnectedValueVariable.',ConnectedValueVariable,[
							'ParentedTotalPathStr'
						])
				]
			)
			'''

			#/####################/#
			# Now set the ConnectedToVariable
			# 

			#debug
			'''
			self.debug(
				[
					'We just set the ConnectedToVariable'
				]
			)
			'''

			#set
			self.ConnectedToVariable=ConnectedValueVariable

	def mimic_get(self):

		#Check
		if type(self.GettingKeyVariable)==str:

			#Check
			if self.GettingKeyVariable.startswith(ConnectGetSetPrefixStr):

				#debug
				'''
				self.debug(
						[
							'We get connect here',
							('self.',self,['GettingKeyVariable'])
						]
					)
				'''

				#connect
				self.connect(
						SYS.deprefix(
							self.GettingKeyVariable,
							ConnectGetSetPrefixStr
						)
					)

				#return
				return {'HookingIsBool':False}

		#set
		BaseClass.get(self)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify to see maybe ConnectedToVariable
		#

		#Check
		if self.PrintingSelfBool:

			#Check
			if self.ConnectedToVariable!=None:

				#/##################/#
				# Add in the pointer descrp
				#	

				#add
				self.PrintingCopyVariable.PrintingInfoStr+=' ->'+str(
					id(self.ConnectedToVariable)
				)

				#/##################/#
				# Stringify
				#

				self.PrintingCopyVariable.ConnectedToVariable=Printer.getPointerStr(
					self.PrintingCopyVariable.ConnectedToVariable
				)
				
			else:

				#append
				self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList.append('ConnectedToVariable')

				#debug
				'''
				print('Connecter l 325')
				print('Remove ConnectedToVariable')
				print('self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList is ')
				print(self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList)
				print('')
				'''
			
		
		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#/##################/#
		# Call the base method
		#

		BaseClass.propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable)

		#/##################/#
		# connect for each managed value in the Connections teams
		#

		#mapConnect
		self.mapConnect()

	def mapConnect(self,_TeamPrefixStr='Connect',_GetterVariable=None):

		#/################/#
		#  Check the level
		#

		#debug
		'''
		self.debug(
			[
				'We map connect here',
				'_TeamPrefixStr is '+_TeamPrefixStr
			]
		)
		'''

		#filter
		TeamTagStrsList=SYS._filter(
			lambda __KeyStr:
			__KeyStr.startswith(_TeamPrefixStr),
			self.TeamDict.keys()
		)

		#Check
		if len(TeamTagStrsList)==1:

			#get
			TeamTagStr=TeamTagStrsList[0]

			#debug
			'''
			self.debug(
				[
					'TeamTagStr is '+TeamTagStr,
				]
			)
			'''

			#/#################/#
			#  omes level
			#

			#Check
			if TeamTagStr.endswith('omes'):

				#map
				map(
					lambda __DeriveConnecter:
					__DeriveConnecter.mapConnect(
						_TeamPrefixStr,
						self
					),
					self.TeamDict[
						TeamTagStr
					].ManagementDict.values()
				)
					
			else:

				#/#################/#
				#  ions level
				#

				#setConnections
				self.setConnections(TeamTagStr,_GetterVariable)

	def setConnections(self,_TeamTagStr,_GetterVariable):

		#/#################/#
		#  ions level
		#

		#debug
		'''
		self.debug(
			[
				'We set connections here',
				'_TeamTagStr is '+_TeamTagStr
			]
		)
		'''

		#Check
		if _GetterVariable==None:
			_GetterVariable=self

		#debug
		'''
		self.debug(
			[
				'We map a connect here',
				'TeamTagStr is '+TeamTagStr,
				'We get the things to connect from here the top connecter'
			]
		)
		'''

		#get
		ConnectionsDeriveConnecter=self.TeamDict[
					_TeamTagStr
				]

		"""
		#map
		ConnectionsKeyVariablesList=map(
			lambda __ItemTuple:
			__ItemTuple[0]
			if __ItemTuple[1].ConnectingKeyVariable==None
			else __ItemTuple[1].ConnectingKeyVariable,
			ConnectionsDeriveConnecter.ManagementDict.items()
		)

		#map
		map(
				lambda __ConnectionsKeyVariable,__DeriveConnecter:
				__DeriveConnecter.connect(
					_GetterVariable[
						__ConnectionsKeyVariable
					],
					_GetBool=False
				)
				if type(__ConnectionsKeyVariable)==str
				else __DeriveConnecter.connect(
					__ConnectionsKeyVariable,
					_GetBool=False
				),
				ConnectionsKeyVariablesList,
				ConnectionsDeriveConnecter.ManagementDict.values()
			)
		"""

		#map
		map(
			lambda __ItemTuple:
			self.setConnection(
				__ItemTuple[0],
				__ItemTuple[1],
				_GetterVariable
			),
			ConnectionsDeriveConnecter.ManagementDict.items()
		)

	def setConnection(self,_KeyVariable,_ValueDeriveConnecter,_GetterVariable):

		#debug
		'''
		self.debug(
			[
				'We setConnection here',
				'_KeyVariable is '+SYS._str(_KeyVariable)
			]
		)
		'''

		#/#################/#
		# Determine the key from the management key or inside
		#

		if _ValueDeriveConnecter.ConnectingKeyVariable==None:
			KeyVariable=_KeyVariable
		else:
			KeyVariable=_ValueDeriveConnecter.ConnectingKeyVariable

		#debug
		'''
		self.debug(
			[
				'Ok now',
				'KeyVariable is '+SYS._str(KeyVariable)
			]
		)
		'''

		#/##################/#
		# Connect with or without getting before
		#

		#connect
		if type(KeyVariable)==str:

			#debug
			'''
			self.debug(
				[
					'We get and connect'
				]
			)
			'''

			#connect
			_ValueDeriveConnecter.connect(
				_GetterVariable[
					KeyVariable
				],
				_GetBool=False
			)

		else:

			#debug
			'''
			self.debug(
				[
					'We directly connect'
				]
			)
			'''

			#connect
			_ValueDeriveConnecter.connect(
				KeyVariable,
				_GetBool=False
			)

		#debug
		'''
		self.debug(
			[
				'In the end',
				#'_ValueDeriveConnecter.ConnectedToVariable is ',
				#SYS._str(_ValueDeriveConnecter.ConnectedToVariable),
				'_ValueDeriveConnecter.ConnectedToVariable.ManagementTagStr is '+ _ValueDeriveConnecter.ConnectedToVariable.ManagementTagStr
			]
		)
		'''
		
#</DefineClass>

#<DefineLocals>

#set
Parenter.ParenterClass.ManagingValueClass=ConnecterClass

#</DefineLocals>

#</DefinePrint>
ConnecterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ConnectingKeyVariable',
		'ConnectingGetBool',
		#'ConnectedToVariable',
	]
)
#<DefinePrint>
