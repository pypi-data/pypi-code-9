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
ConnectGetSetPrefixStr="<->"
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
					_ConnectFromVariable=None,	
					_ConnectToVariable=None,
					_ConnectKeyVariablesList=None,
					_ConnectOutAndInTeamKeyStrsListsList=None,
					_ConnectingKeyVariable=None,
					_ConnectingOutSetVariable=None,
					_ConnectingInSetVariable=None,
					_ConnectingOutTeamKeyStr="",
					_ConnectingInTeamKeyStr="",
					_ConnectingGetBool=True,
					_ConnectingValueClass=None,
					_ConnectingOutManagementKeyStr="",
					_ConnectingInManagementKeyStr="",
					_ConnectedParentDeriveConnecterVariable=None,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_connect(self):

		#/####################/#
		# Get the connected variable
		#

		#debug
		self.debug(
			[
				'Adapt the type for getting things to connect',
				'(if we need to get)',
				("self.",self,[
								'ConnectingKeyVariable',
								'ConnectingOutSetVariable',
								'ConnectingGetBool',
							])
			]
		)

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
		# Adapt the type for setting things in the commanded variables
		#

		#debug
		self.debug(
			[
				'Adapt the type for setting things in the outlet managed connected variable',
				("self.",self,[
					'ConnectingOutSetVariable'
					])
			]
		)

		#inits
		ConnectedOutSetVariablesList=SYS.SetList(self.ConnectingOutSetVariable)

		#debug
		'''
		self.debug(
				[
					'in the end, ConnectedOutSetVariablesList is ',
					SYS._str(ConnectingSetVariablesList),
					'Now adapt the type for setting things in the outlet managed connected variable',
					("self.",self,[
						'ConnectingOutSetVariable'
						])
				]
			)
		'''

		#inits
		ConnectingInSetVariablesList=SYS.SetList(self.ConnectingInSetVariable)

		#debug
		'''
		self.debug(
				[
					'in the end, ConnectingInSetVariablesList is ',
					SYS._str(ConnectingSetVariablesList)
				]
			)
		'''

		#/####################/#
		# Now put this getted variable in a 
		# encapsulating managed outlets variable

		#debug
		'''
		self.debug(
				[
					'Now we out team ',
					('self.',self,['ConnectingOutTeamKeyStr']),
					'Check if we have to set a new managed point object or just set the ',
					'ConnectToVariable'
				]
			)
		'''

		#Check
		if self.ConnectingOutTeamKeyStr=="":

			#debug
			self.debug(
				[
					'We just set the ConnectToVariable'
				]
			)

			#set
			self.ConnectToVariable=ConnectedValueVariable

			#update
			if len(ConnectedOutSetVariablesList)>0:

				#mapSet
				self.mapSet(
					ConnectedOutSetVariablesList
				)

		else:

			#debug
			'''
			self.debug(
				[
					'We set in a team'
				]
			)
			'''

			#Check
			if self.ConnectingOutTeamKeyStr not in self.TeamDict:
				ConnectedOutDeriveTeamer=self.team(
					self.ConnectingOutTeamKeyStr
				).TeamedValueVariable
			else:
				ConnectedOutDeriveTeamer=self.TeamDict[
					self.ConnectingOutTeamKeyStr
				]

			#/####################/#
			# Build the OutManagementKeyStr
			#

			#Check
			if self.ConnectingOutManagementKeyStr=="":

				#set
				ConnectedOutManagementKeyStr=ConnectManagementPrefixStr+ConnectedValueVariable.ParentedTotalPathStr.replace(
						'/','_'
					)+'_'+ConnectedValueVariable.ManagementTagStr
			else:

				#alias
				ConnectedOutManagementKeyStr=self.ConnectingOutManagementKeyStr

			#/####################/#
			# Now manage
			#

			#debug
			'''
			self.debug(
				[
					'We manage out',
					('self.',self,[
						'ConnectingValueClass',
					]),
					'ConnectedOutSetVariablesList is ',
					SYS._str(ConnectedOutSetVariablesList)
				]
			)
			'''

			#manage
			if self.ConnectingValueClass!=None:
				ConnectedOutDeriveTeamer.ManagingValueClass=self.ConnectingValueClass

			#manage	
			ConnectedOutDeriveTeamer.manage(
					ConnectedOutManagementKeyStr,
					SYS.update(
						[
							('ConnectToVariable',ConnectedValueVariable),
							('ConnectFromVariable',self)
						],
						ConnectedOutSetVariablesList,
					),
				)

		#/####################/#
		# And put also the inverse in a 
		# encapsulating managed inlets in the getted variable

		#debug
		'''
		self.debug(
				[
					'Now we in team ',
					'IMPORTANT the ConnectingInTeamKeyStr is from the original connecting',
					'not the connected object',
					('self.',self,['ConnectingInTeamKeyStr'])
				]
			)
		'''

		#Check
		if self.ConnectingInTeamKeyStr=="":

			#debug
			'''
			self.debug(
				[
					'We just set the ConnectFromVariable in the ConnectedValueVariable'
				]
			)
			'''

			#set
			ConnectedValueVariable.ConnectFromVariable=self

			#update
			if len(ConnectingInSetVariablesList)>0:

				#mapSet
				ConnectedValueVariable.mapSet(
					ConnectedInSetVariablesList
				)

		else:

			#debug
			self.debug(
				[
					'We set a team in the ConnectFromVariable'
				]
			)

			#Check
			if self.ConnectingInTeamKeyStr not in ConnectedValueVariable.TeamDict:
				ConnectedInDeriveTeamer=ConnectedValueVariable.team(
					self.ConnectingInTeamKeyStr
				).TeamedValueVariable
			else:
				ConnectedInDeriveTeamer=ConnectedValueVariable.TeamDict[
				self.ConnectingInTeamKeyStr
			]

			#/####################/#
			# Build the InManagementKeyStr
			#

			#Check
			if self.ConnectingInManagementKeyStr=="":
				ConnectedInManagementKeyStr=ConnectManagementPrefixStr+self.ParentedTotalPathStr.replace(
						'/','_'
					)+'_'+self.ManagementTagStr
			else:
				ConnectedInManagementKeyStr=self.ConnectingInManagementKeyStr

			#/####################/#
			# Now manage
			#

			#debug
			'''
			self.debug(
					[
						'manage the connect in',
						('self.',self,['ConnectingValueClass'])
					]
				)
			'''

			#Check		
			if self.ConnectingValueClass!=None:

				#set
				ConnectedInDeriveTeamer.ManagingValueClass=self.ConnectingValueClass

			#manage
			ConnectedInDeriveTeamer.manage(
					ConnectedInManagementKeyStr,
					SYS.update(
						[
							('ConnectToVariable',self),
							('ConnectFromVariable',ConnectedValueVariable)
						],
						ConnectingInSetVariablesList,
					),
				)

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
						),
						None
					)

				#return
				return {'HookingIsBool':False}

		#set
		BaseClass.get(self)

	def mimic_set(self):

		#Check
		if type(self.SettingKeyVariable)==str:

			#Check
			if self.SettingKeyVariable.startswith(ConnectGetSetPrefixStr):

				if type(
					self.SettingValueVariable
				)==list and SYS.getIsTuplesListBool(self.SettingValueVariable
				)==False and len(self.SettingValueVariable)==2:

					#debug
					'''
					self.debug(
							[
								'We set connect here',
								('self.',self,['SettingKeyVariable'])
							]
						)
					'''

					#connect
					self.connect(
							SYS.deprefix(
								self.SettingKeyVariable,
								ConnectGetSetPrefixStr
							),
							self.SettingValueVariable[0],
							self.SettingValueVariable[1]
						)

					#return
					return {'HookingIsBool':False}

				else:

					#debug
					'''
					self.debug(
							[
								'We set connect back here',
								('self.',self,['SettingKeyVariable'])
							]
						)
					'''

					#connect
					self.connect(
							SYS.deprefix(
								self.SettingKeyVariable,
								ConnectGetSetPrefixStr
							),
							self.SettingValueVariable
						) 

					#return
					return {'HookingIsBool':False}

		#set
		BaseClass.set(self)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#Check
			if self.PrintingCopyVariable.ConnectToVariable!=None:

				self.PrintingCopyVariable.ConnectToVariable=Printer.getPointerStr(
					self.PrintingCopyVariable.ConnectToVariable
				)
				
			else:

				#append
				self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList.append('ConnectToVariable')

				#debug
				'''
				print('Connecter l 325')
				print('Remove ConnectToVariable')
				print('self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList is ')
				print(self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList)
				print('')
				'''

			#Check
			if self.PrintingCopyVariable.ConnectFromVariable!=None:

				self.PrintingCopyVariable.ConnectFromVariable=Printer.getPointerStr(
					self.PrintingCopyVariable.ConnectFromVariable
				)
				
			else:

				#append
				self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList.append('ConnectFromVariable')

				#debug
				'''
				print('Connecter l 514')
				print('Remove ConnectFromVariable')
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
		# determine the 
		#


		"""
		#/##################/#
		# connect the KeyStrsList
		#

		#debug
		'''
		self.debug(
				[
					'We make connect the ConnectKeyVariablesList',
					('self.',self,['ConnectKeyVariablesList'])
				]
			)
		'''

		#Check
		if self.ConnectKeyVariablesList!=None:

			#map
			map(
					lambda __ConnectKeyStr:
					self.connect(
						__ConnectKeyStr,
						None
					),
					self.ConnectKeyVariablesList
				)
		"""

		"""
		#/##################/#
		# connect for each managed value in the Connections teams
		#

		#Check
		if 'Connections' in self.TeamDict:

			#debug
			'''
			self.debug(
				[
					'We are maybe going to connect the connections',
					'self.ParentDeriveTeamerVariable.TeamTagStr is ',
					self.ParentDeriveTeamerVariable.TeamTagStr
				]
			)
			'''
			
			#Check
			if self.ParentDeriveTeamerVariable==None or self.ParentDeriveTeamerVariable.TeamTagStr!='Connectomes':
			
				#debug
				'''
				self.debug(
					[
						'We make connect in the Connections',
						'self.TeamDict['Connections'].ManagementDict is ',
						SYS._str(self.TeamDict['Connections'].ManagementDict),
						'But first determine the Out and In team strs'
					]
				)
				'''

				#setConnections
				self.setConnections(
					self.TeamDict['Connections']
				)

		#/##################/#
		# connect for each connections for each managed value in the Connectomes teams
		#

		#Check
		if 'Connectomes' in self.TeamDict:

			#setConnectomes
			self.setConnectomes()
		"""

	def mapConnect(self,_TeamTagStr='Connections',_GetterVariable=self):

		#/################/#
		# 
		#

		#debuf
		self.debug(
			[
				'We map a connection here',
				'We get the things to connect from here the top connecter'
			]
		)

		#get
		ConnectionsDeriveConnecter=self.TeamDict[
					_TeamTagStr
				]

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
		
	def setConnections(self,_DeriveManager,_OutTeamKeyStr="",_InTeamKeyStr=""):

		#debug
		'''
		self.debug(
			[
				'We set connections here'
			]
		)
		'''

		#Check
		if _OutTeamKeyStr!="":
			self.ConnectingOutTeamKeyStr=_OutTeamKeyStr
		if _InTeamKeyStr!="":
			self.ConnectingInTeamKeyStr=_InTeamKeyStr

		#map
		map(
			lambda __ItemTuple:
			self.connect(
				#ConnectingKeyVariable
				__ItemTuple[0].replace('_','/'),
				#ConnectingOutSetVariable
				__ItemTuple[1][0],
				#ConnectingInSetVariable
				__ItemTuple[1][1]
			) if type(
				__ItemTuple[1]
			) in [list,tuple] and len(__ItemTuple[1])==2
			else
			self.connect(
				__ItemTuple[0].replace('_','/'),
				__ItemTuple[1]
			),	
			_DeriveManager.ManagementDict.items()
		)

	def setConnectomes(self,_TeamPrefixStr='Connect'):

		#set
		ParentTeamTagStr=_TeamPrefixStr+'omes'

		#map
		ConnectOutAndInTeamKeyStrsListsList=map(
				lambda __TeamKeyStr:
				__TeamKeyStr.split(ConnectGetSetPrefixStr),
				self.TeamDict[ParentTeamTagStr].ManagementDict.keys()
			)

		#debug
		'''
		self.debug(
			[
				'ConnectOutAndInTeamKeyStrsListsList is ',
				str(ConnectOutAndInTeamKeyStrsListsList),
				'Now connect really !'
			]
		)
		'''

		#set
		ChildTeamTagStr=_TeamPrefixStr+'ions'

		#map
		map(
				lambda __ConnectOutAndInTeamKeyStrsList,__TeamValueVariable:
				self.setConnections(
					__TeamValueVariable.TeamDict[ChildTeamTagStr],
					__ConnectOutAndInTeamKeyStrsList[0],
					__ConnectOutAndInTeamKeyStrsList[1]
				),
				ConnectOutAndInTeamKeyStrsListsList,
				self.TeamDict[ParentTeamTagStr].ManagementDict.values()
			)



#</DefineClass>

#<DefineLocals>

#set
Parenter.ParenterClass.ManagingValueClass=ConnecterClass
#ConnecterClass.ConnectingValueClass=ConnecterClass

#</DefineLocals>

#</DefinePrint>
ConnecterClass.PrintingClassSkipKeyStrsList.extend(
	[
		#'ConnectFromVariable',
		#'ConnectToVariable',
		'ConnectVariablesList',
		'ConnectKeyVariablesList',
		'ConnectOutAndInTeamKeyStrsListsList',
		'ConnectingKeyVariable',
		'ConnectingOutSetVariable',
		'ConnectingInSetVariable',
		'ConnectingOutTeamKeyStr',
		'ConnectingInTeamKeyStr',
		'ConnectingGetBool',
		'ConnectingValueClass',
		'ConnectingOutManagementKeyStr',
		'ConnectingInManagementKeyStr',
		'ConnectedParentDeriveConnecterVariable'
	]
)
#<DefinePrint>
