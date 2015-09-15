# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Structurer 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Connecter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Structurer','Structure','Structuring','Structured')
#</DefineAugmentation>

#<ImportSpecificModules>
Connecter=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
StructureOutPrefixStr='_Struc_'
StructureInTeamKeyStr='Structures'
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class StructurerClass(BaseClass):

	def default_init(
					self,
					_StructureTagStr='Top',
					_StructureTopDeriveStructurerVariable=None,
					_StructureTargetStr='Top',
					_StructureConnectPrefixStrsList=None,
					_StructureFilterTeamTagStrsList=None,
					_StructuringTeamerCommandKeyVariable=None,
					_StructuringManagerCommandKeyVariable=None,
					_StructuringBeforeCommandSetList=None,
					_StructuringTeamerCommandSetList=None,
					_StructuringManagerCommandSetList=None,
					_StructuringSingPluralVariable=None,
					_StructuringTagStr="",
					_StructuringClassBool=True,
					_StructuringFlatBool=False,
					_StructuringTeamerCommandExtraKeyVariable=None,
					_StructuringManagerCommandExtraKeyVariable=None,
					_StructuredTeamKeyStrsList=None,
					_StructuredOnceBool=False,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#init
		self.StructureTopDeriveStructurerVariable=self

	def do_structure(self):

		#/###################/#
		# Check the level
		#

		#debug
		'''
		self.debug(
			[
				'We structure here',
				'self.StructureTopDeriveStructurerVariable==self is ',
				str(self.StructureTopDeriveStructurerVariable==self)
			]
		)
		'''

		#Check
		if self.StructureTopDeriveStructurerVariable==self:

			#debug
			'''
			self.debug(
				[
					'We are in the top structurer',
				]
			)
			'''
			
			#debug
			'''
			self.debug(
					[
						'We structure top here',
						('self.',self,[
								'StructuringTeamerCommandKeyVariable',
								'StructuringManagerCommandKeyVariable'
							])
					]
				)
			'''
			
			#/###################/#
			# Set the structure of singular team if not already
			#

			#Check
			if self.StructuredOnceBool==False:

				#Check
				if self.StructuringSingPluralVariable!=None:

					#debug
					'''
					self.debug(
						[
							'we structure for the first time here',
							('self.',self,['StructuringSingPluralVariable'])
						]
					)
					'''

					#map add the sing plurals
					map(
						lambda __ItemTuple:
						SYS.addSingPlural(
							*__ItemTuple
						),
						SYS.SetList(self.StructuringSingPluralVariable)
					)

					#Define a class
					class StructureClass(StructurerClass):pass
					StructureClass.__name__=self.NameStr+'s'
					StructureClass.ManagingValueClass=self.__class__

					#set
					setattr(
						self.Module,
						StructureClass.__name__,
						StructureClass
					)

					#dict
					ClassesDict=dict(
							map(
								lambda __ItemTuple:
								(__ItemTuple[1],StructureClass),
								_SingPluralVariable
							)
						)

					#Check
					if self.StructuringClassBool:

						#map
						if _Class.TeamingClassesDict==None:
							_Class.TeamingClassesDict=ClassesDict
						else:
							_Class.TeamingClassesDict.update(
								ClassesDict
							)

						#set 
						self.__class__.StructuringOnceBool=True

					else:

						#map
						if self.TeamingClassesDict==None:
							self.TeamingClassesDict=ClassesDict
						else:
							self.TeamingClassesDict.update(
								ClassesDict
							)


					#set
					self.StructuredOnceBool=True


			#Check
			if self.StructuringFlatBool:

				#/##################/#
				# prepare the struc teams
				#

				#map
				self.StructuredTeamKeyStrsList=map(
						lambda __StructuringTeamOrManagementStr:
						StructureOutPrefixStr+self.StructuringTagStr+'_'+__StructuringTeamOrManagementStr,
						(self.StructuringTeamerCommandKeyVariable if self.StructuringTeamerCommandKeyVariable!=None else [])+
						(self.StructuringManagerCommandKeyVariable if self.StructuringManagerCommandKeyVariable!=None else [])
					)

				#debug
				'''
				self.debug(
						[
							'We are going to make team the StructuredTeamKeyStrsList',
							('self.',self,['StructuredTeamKeyStrsList'])
						]
					)
				'''

				#map
				map(
						lambda __StructuredTeamKeyStr:
						self.team(__StructuredTeamKeyStr),
						self.StructuredTeamKeyStrsList
					)

			#/##################/#
			# we make the top parent and structure
			#

			#set
			self.StructureTopDeriveStructurerVariable=self
			self.parent()

			#/##################/#
			# command
			#

			#debug
			'''
			self.debug(
				[
					'Before command we set the arg'
				]
			)
			'''

			#set
			self.setCommandingKeyVariable()
			self.CommandTopDeriveCommanderRigidVariable=self
			self.setCommandingSetVariable()
			self.CommandingAfterWalkRigidBool=True
			self.CommandingGetRigidBool=False
			self.CommandingSetRigidBool=False
			self.CommandingSetAttrOrCallRigidBool=True


			#debug
			'''
			self.debug(
				[
					'we are going to command',
					('self.',self,[
						'CommandingKeyVariable',
						'CommandingSetVariable'
					])
				]
			)
			'''

			#command
			self.command()

			#debug
			'''
			self.debug(
				[
					'Ok we have commanded'
				]
			)
			'''

		else:

			#debug
			'''
			self.debug(
				[
					'We structure in a level here'
				]
			)
			'''

			pass

	def setCommandingKeyVariable(self):

		#/##################/#
		# Set the teams and managements that are going to be setted
		# but also the ones that are just going to be passed through

		#debug
		'''
		self.debug(
			[
				'we set commanding key variable',
				('self.',self,[
					'StructuringTeamerCommandKeyVariable',
					'StructuringTeamerCommandExtraKeyVariable',
					'StructuringManagerCommandKeyVariable',
					'StructuringManagerCommandExtraKeyVariable'
				])
			]
		)
		'''

		#set
		self.setCommandingExtraKeyVariable()
		self.setCommandingExtraKeyVariable('Extra')

		#debug
		'''
		self.debug(
			[
				'in the end',
				('self.',self,[
					'CommandingKeyVariable',
					'CommandingExtraKeyVariable'
				])
			]
		)
		'''

	def setCommandingExtraKeyVariable(self,_ExtraStr=""):

		#/##################/#
		# Switch case depending on the team or manage level
		#

		#debug
		'''
		self.debug(
			[
				'We setCommandingKeyVariable here',
				('self.',self,[
					'TeamedOnceBool',
					'StructuringTeamerCommandKeyVariable',
					'StructuringManagerCommandKeyVariable'
				]),
				'We get the good team or management keys'
			]
		)
		'''
		
		#set
		CommandingKeyVariableKeyStr='Commanding'+_ExtraStr+'KeyVariable'

		#Check
		if self.TeamedOnceBool:

			#/##################/#
			#  get
			#

			#set
			StructuringCommandKeyVariableKeyStr='StructuringTeamerCommand'+_ExtraStr+'KeyVariable'
	
			#get
			StructuringTeamerCommandKeyVariable=getattr(
				self,
				StructuringCommandKeyVariableKeyStr
			)

			#debug
			'''
			self.debug(
				[
					'StructuringTeamerCommandKeyVariable is ',
					SYS._str(StructuringTeamerCommandKeyVariable)
				]
			)
			'''

			#/###############/#
			# Determine the CommandedLiargVariablesList
			#

			#Check
			if StructuringTeamerCommandKeyVariable==None:

				#all the key
				StructureKeyStrsList=[]

			#Check
			elif type(StructuringTeamerCommandKeyVariable)==list and len(
				StructuringTeamerCommandKeyVariable
			)>0 and type(
				StructuringTeamerCommandKeyVariable[0]
			)==str:

				#alias
				StructureKeyStrsList=StructuringTeamerCommandKeyVariable
			
			#Check
			elif StructuringTeamerCommandKeyVariable=="#all":

				#all the key
				StructureKeyStrsList=self.TeamDict.keys()
	
			else:

				#mapCondition
				StructureKeyStrsList=self.mapCondition(
					StructuringTeamerCommandKeyVariable,
					self.TeamDict.keys(),
					_SetAttrOrCallBool=True
				)

			#/###############/#
			# Now get and filter in the team
			#

			#debug
			'''
			self.debug(
				[
					'We get the managed values in the Teamer',
					'StructureKeyStrsList is ',
					SYS._str(StructureKeyStrsList)
				]
			)
			'''

			#set
			setattr(
				self,
				CommandingKeyVariableKeyStr,
				SYS.filterNone(
				map(
					lambda __KeyStr:
					self.TeamDict[__KeyStr]
					if __KeyStr in self.TeamDict
					else None,
					StructureKeyStrsList
					)
				)
			)

		else:

			#/###############/#
			# Determine the CommandedLiargVariablesList
			#

			#debug 
			'''
			self.debug(
				[
					'We setCommandingKeyVariable in a manager',
					('self.',self,['StructuringManagerCommandKeyVariable'])
				]
			)
			'''

			#/##################/#
			#  get
			#

			#set
			StructuringCommandKeyVariableKeyStr='StructuringManagerCommand'+_ExtraStr+'KeyVariable'

			#get
			StructuringManagerCommandKeyVariable=getattr(
				self,
				StructuringCommandKeyVariableKeyStr
			)

			#Check
			if StructuringManagerCommandKeyVariable==None:

				#all the key 
				StructureKeyStrsList=[]

			#Check
			elif type(StructuringManagerCommandKeyVariable
			)==list and len(StructuringManagerCommandKeyVariable
				)>0 and type(StructuringManagerCommandKeyVariable[0])==str:

				#alias
				StructureKeyStrsList=StructuringManagerCommandKeyVariable
			
			#Check
			elif StructuringManagerCommandKeyVariable=="#all":

				#all the key 
				StructureKeyStrsList=self.ManagementDict.keys()

			else:

				#mapCondition
				StructureKeyStrsList=self.mapCondition(
					StructuringManagerCommandKeyVariable,
					self.ManagementDict.keys(),
					_SetAttrOrCallBool=True
				)

			#/###############/#
			# Now get and filter in the management
			#

			#debug
			'''
			self.debug(
				[
					'We get the teamed values in the Manager',
					'StructureKeyStrsList is ',
					str(StructureKeyStrsList)
				]
			)
			'''
			
			#set
			setattr(
				self,
				CommandingKeyVariableKeyStr,
				SYS.filterNone(
					map(
						lambda __KeyStr:
						self.ManagementDict[__KeyStr]
						if __KeyStr in self.ManagementDict
						else None,
						StructureKeyStrsList
					)
				)
			)

	def setCommandingSetVariable(self):

		#/##################/#
		# Switch case depending on the team or manage level
		#

		#debug
		'''
		self.debug(
			[
				'We setCommandingSetVariable here',
				('self.',self,[
					'TeamedOnceBool',
					'StructuringTeamerCommandSetList',
					'StructuringManagerCommandSetList'
				])
			]
		)
		'''

		#Check
		if self.TeamedOnceBool:

			#alias
			self.CommandingSetVariable=self.StructuringTeamerCommandSetList

		else:

			#alias
			self.CommandingSetVariable=self.StructuringManagerCommandSetList

		#debug
		'''
		self.debug(
			[
				'Now we add the before with the special',
				'self.CommandTopDeriveCommanderRigidVariable==self is ',
				str(self.CommandTopDeriveCommanderRigidVariable==self)
			]
		)
		'''

		#init
		CommandingSetVariable=[
					('StructureTopDeriveStructurerVariable',self.CommandTopDeriveCommanderRigidVariable),
					('StructuringTeamerCommandKeyVariable',self.StructuringTeamerCommandKeyVariable),
					('StructuringManagerCommandKeyVariable',self.StructuringManagerCommandKeyVariable),
					('StructuringTeamerCommandSetList',self.StructuringTeamerCommandSetList),
					('StructuringManagerCommandSetList',self.StructuringManagerCommandSetList),
					('parent'),
					('setCommandingKeyVariable'),
					('setCommandingSetVariable')
		]

		#add
		self.CommandingSetVariable=CommandingSetVariable+self.CommandingSetVariable

		#debug
		'''
		self.debug(
			[
				'In the end',
				('self.',self,['CommandingSetVariable'])
			]
		)
		'''


	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#/##################/#
		# Call the base method
		#

		#debug
		'''
		self.debug(
			[
				'First we call the base method',
				('self.',self,[
							'StructuringTeamerCommandKeyVariable',
							'StructuringManagerCommandKeyVariable'
						])
			]
		)
		'''

		#call the base method
		BaseClass.propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable)

		#debug
		'''
		self.debug(
			[
				'We have called the base method',
				('self.',self,[
							'StructuringTeamerCommandKeyVariable',
							'StructuringManagerCommandKeyVariable'
						])
			]
		)
		'''

		#/##################/#
		# Set the StructureTagStr
		#

		#debug
		'''
		self.debug(
				[
					'We have parented',
					'we set the control path str',
					('self.',self,[
							'ParentedTotalPathStr',
							'ManagementTagStr'
						])
				]
			)
		'''
		
		#Check
		if self.ManagementTagStr!='':

			#get
			self.StructureTagStr=(
					self.ParentedTotalPathStr+'/'+self.ManagementTagStr
				).replace('/','_')

		#remove
		if self.StructureTagStr[0]=='_':
			self.StructureTagStr=self.StructureTagStr[1:]

		"""
		#/##################/#
		# Find the StructureTopDeriveStructurerVariable in the grand parents
		#

		#find
		'''
		self.debug(
			[
				'We have parented',
				('self.',self,[
						#'ParentedTotalDeriveTeamersList',
						'StructureTargetStr'
					]),
				'Now find the StructureTopDeriveStructurerVariable that has the StructureTagStr',
				'equal to the self.StructureTargetStr'
			]
		)
		'''

		#Check
		if len(self.ParentedTotalDeriveTeamersList)>0:

			#index
			try:

				#index
				IndexInt=map(
						lambda __ParentedDeriveTeamer:
						hasattr(
							__ParentedDeriveTeamer,
							'StructureTargetStr'
						) and __ParentedDeriveTeamer.StructureTagStr==self.StructureTargetStr,
						self.ParentedTotalDeriveTeamersList
					).index(True)

				#set
				self.StructureTopDeriveStructurerVariable=self.ParentedTotalDeriveTeamersList[IndexInt]

			except:

				IndexInt=len(self.ParentedTotalDeriveTeamersList)
			
		#debug
		'''
		self.debug(
				[
					'Finally StructureTopDeriveStructurerVariable is ',
					SYS._str(self.StructureTopDeriveStructurerVariable)
				]
			)
		'''

		#/##################/#
		# Add to the StructureTopDeriveStructurerVariable
		#

		#debug
		'''
		self.debug(
			[
				('self.',self,[
					'TeamTagStr',
					'ManagementTagStr'
				])
			]
		)
		'''

		#Check
		if self.TeamTagStr!="":
			
			#debug
			'''
			self.debug(
					[
						'Check if we have to make manage the '+str(
							StructureOutPrefixStr+self.ParentDeriveTeamerVariable.ManagementTagStr
						),
						'self.StructureTopDeriveStructurerVariable.StructuringManagerCommandKeyVariable is ',
						str(self.StructureTopDeriveStructurerVariable.StructuringManagerCommandKeyVariable)
					]
				)
			'''

			#Check
			if self.StructureTopDeriveStructurerVariable.StructuringManagerCommandKeyVariable!=None:

				#Check
				if self.ParentDeriveTeamerVariable.ManagementTagStr in self.StructureTopDeriveStructurerVariable.StructuringManagerCommandKeyVariable:

					#debug
					self.debug(
						[
							'Yes we make team connect here',
							('self.',self,['PointingInManagementKeyStr']),
							'self.ParentDeriveTeamerVariable.ManagementTagStr is ',
							str(self.ParentDeriveTeamerVariable.ManagementTagStr),

						]
					)

					#connect
					#self.StructureTopDeriveStructurerVariable.connect(
					#		self,
					#		_OutTeamKeyStr=StructureOutPrefixStr+self.StructuringTagStr+'_'+self.ParentDeriveTeamerVariable.ManagementTagStr,
					#		_InTeamKeyStr=StructureInTeamKeyStr
					#)

					#connect out like in the StructureTopDeriveStructurerVariable
					self.StructureTopDeriveStructurerVariable.TeamDict[
						StructureOutPrefixStr+self.StructuringTagStr+'_'+self.ParentDeriveTeamerVariable.ManagementTagStr
					].manage(
						self.StructureTagStr,
						{
							'ConnectedToVariable':self
						}
					)

					#connect in like in the self
					#self.TeamDict[
					#	StructureInTeamKeyStr
					#].manage(
					#	{
					#		'ConnectedToVariable':self.StructureTopDeriveStructurerVariable
					#	}
					#)

		if self.ManagementTagStr!="":
			
			#debug
			'''
			self.debug(
					[
						'we make connect the top structureer on the team'+str(
							StructureOutPrefixStr+self.ParentDeriveTeamerVariable.TeamTagStr
						),
						('self.',self,[
								'StructureTagStr'
							])
					]
				)
			'''

			#Check
			if self.StructureTopDeriveStructurerVariable.StructuringTeamerCommandKeyVariable!=None:

				#Check
				if self.ParentDeriveTeamerVariable.TeamTagStr in self.StructureTopDeriveStructurerVariable.StructuringTeamerCommandKeyVariable:

					#debug
					'''
					self.debug(
						[
							'Yes we make team connect here',
							#'self.StructureTopDeriveStructurerVariable.TeamDict.keys() is',
							#str(self.StructureTopDeriveStructurerVariable.TeamDict.keys()),
							#('self.',self,['StructureTopDeriveStructurerVariable']),
							'self.StructureTopDeriveStructurerVariable.StructuredTeamKeyStrsList is',
							str(self.StructureTopDeriveStructurerVariable.StructuredTeamKeyStrsList),
							('self.',self,['StructuringTagStr'])
						]
					)
					'''
					
					#connect out like in the StructureTopDeriveStructurerVariable
					self.StructureTopDeriveStructurerVariable.TeamDict[
						StructureOutPrefixStr+self.StructureTopDeriveStructurerVariable.StructuringTagStr+'_'+self.ParentDeriveTeamerVariable.TeamTagStr
					].manage(
						self.StructureTagStr,
						{
							'ConnectedToVariable':self
						}
					)

		#debug
		'''
		self.debug(
			[
				'In the end',
				('self.',self,[
							'StructuringTeamerCommandKeyVariable',
							'StructuringManagerCommandKeyVariable'
						])
			]
		)
		'''
		"""

		#/##################/#
		# Maybe do some connections
		#

		#debug
		'''
		self.debug(
			[
				'We do here maybe some connections',
				('self.',self,['StructureConnectPrefixStrsList'])
			]
		)
		'''

		#Check
		if self.StructureConnectPrefixStrsList!=None:

			#debug
			'''
			self.debug(
				[
					'We do here some connections',
					('self.',self,['StructureConnectPrefixStrsList'])
				]
			)
			'''

			#map
			map(
				lambda __StructureConnectPrefixStr:
				self.mapConnect(__StructureConnectPrefixStr),
				self.StructureConnectPrefixStrsList
			)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Simplify the repr of the flatted teams
			#

			#Check
			if type(self.StructuredTeamKeyStrsList)==list:

				#map
				map(
					lambda __StructuredTeamKeyStr:
					self.PrintingCopyVariable.TeamDict.__setitem__(
						__StructuredTeamKeyStr,
						"Pointer with "+str(
							len(
								self.PrintingCopyVariable.TeamDict[
									__StructuredTeamKeyStr
								].ManagementDict
							)
						)+" managed encapsulations"
					),
					self.StructuredTeamKeyStrsList
				)
			
			#/##################/#
			# Simplify also the repr of the structures team
			#

			#Check
			if StructureInTeamKeyStr in self.TeamDict:

				#set
				self.PrintingCopyVariable.TeamDict[
					StructureInTeamKeyStr
				]="Pointer with "+str(
							len(
								self.PrintingCopyVariable.TeamDict[
									StructureInTeamKeyStr
								].ManagementDict
							)
						)+" managed encapsulations"


		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

#</DefineClass>

#<DefineLocals>

#set
#Connecter.ConnecterClass.ManagingValueClass=StructurerClass
#SYS.ParenterClass.ManagingValueClass=StructurerClass

StructurerClass.ManagingValueClass=StructurerClass
StructurerClass.TeamingValueClass=StructurerClass

#</DefineLocals>

#</DefinePrint>
StructurerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'StructureTagStr',
		'StructureTopDeriveStructurerVariable',
		'StructureTargetStr',
		'StructureConnectPrefixStrsList',
		'StructureFilterTeamTagStrsList',
		'StructuringTeamerCommandKeyVariable',
		'StructuringManagerCommandKeyVariable',
		'StructuringBeforeCommandSetList',
		'StructuringTeamerCommandSetList',
		'StructuringManagerCommandSetList',
		'StructuringSingPluralVariable',
		'StructuringTagStr',
		'StructuringClassBool',
		'StructuringFlatBool',
		'StructuringTeamerCommandExtraKeyVariable',
		'StructuringManagerCommandExtraKeyVariable',
		'StructuredTeamKeyStrsList',
		'StructuredOnceBool'
	]
)
#<DefinePrint>
