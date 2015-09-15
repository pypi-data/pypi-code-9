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
					_StructureTopDeriveStructurerRigidVariable=None,
					_StructureTeamerCommandKeyRigidVariable=None,
					_StructureManagerCommandKeyRigidVariable=None,
					_StructureTeamerCommandSetRigidList=None,
					_StructureManagerCommandSetRigidList=None,
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
					_StructuredTeamKeyStrsList=None,
					_StructuredOnceBool=False,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#init
		self.StructureTopDeriveStructurerRigidVariable=self

	def do_structure(self):

		#/###################/#
		# Check the level
		#

		#debug
		'''
		self.debug(
			[
				'We structure here',
				'self.StructureTopDeriveStructurerRigidVariable==self is ',
				str(self.StructureTopDeriveStructurerRigidVariable==self)
			]
		)
		'''

		#set
		self.StructureTopDeriveStructurerRigidVariable=self

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
		self.StructureTopDeriveStructurerRigidVariable=self
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

		#link for setCommandingKeyVariable
		self.StructureTeamerCommandKeyRigidVariable=self.StructuringTeamerCommandKeyVariable
		self.StructureManagerCommandKeyRigidVariable=self.StructuringManagerCommandKeyVariable
		self.setCommandingKeyVariable()

		#link for setCommandingSetVariable
		self.CommandTopDeriveCommanderRigidVariable=self
		self.StructureTeamerCommandSetRigidList=self.StructuringTeamerCommandSetList
		self.StructureManagerCommandSetRigidList=self.StructuringManagerCommandSetList
		self.setCommandingSetVariable()

		#Other
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

	def setCommandingKeyVariable(self):

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
					'StructureTeamerCommandKeyRigidVariable',
					'StructureManagerCommandKeyRigidVariable'
				]),
				'We get the good team or management keys'
			]
		)
		'''
		
		#Check
		if self.TeamedOnceBool:

			#/##################/#
			#  get
			#

			#get
			StructureTeamerCommandKeyRigidVariable=getattr(
				self,
				'StructureTeamerCommandKeyRigidVariable'
			)

			#debug
			'''
			self.debug(
				[
					'StructureTeamerCommandKeyRigidVariable is ',
					SYS._str(StructureTeamerCommandKeyRigidVariable)
				]
			)
			'''

			#/###############/#
			# Determine the CommandedLiargVariablesList
			#

			#Check
			if StructureTeamerCommandKeyRigidVariable==None:

				#all the key
				StructureKeyStrsList=[]

			#Check
			elif type(StructureTeamerCommandKeyRigidVariable)==list and len(
				StructureTeamerCommandKeyRigidVariable
			)>0 and type(
				StructureTeamerCommandKeyRigidVariable[0]
			)==str:

				#alias
				StructureKeyStrsList=StructureTeamerCommandKeyRigidVariable
			
			#Check
			elif StructureTeamerCommandKeyRigidVariable=="#all":

				#all the key
				StructureKeyStrsList=self.TeamDict.keys()
	
			else:

				#mapCondition
				StructureKeyStrsList=self.mapCondition(
					StructureTeamerCommandKeyRigidVariable,
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
				'CommandingKeyVariable',
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

			#get
			StructureManagerCommandKeyRigidVariable=getattr(
				self,
				'StructureManagerCommandKeyRigidVariable'
			)

			#/##################/#
			# Sort the dict
			#

			#debug
			'''
			self.debug(
				[
					'before sort',
					'self.ManagementDict.keys() is ',
					SYS._str(self.ManagementDict.keys())
				]
			)
			'''

			#sort
			self.ManagementDict.sort()

			#debug
			'''
			self.debug(
				[
					'after sort',
					'self.ManagementDict.keys() is ',
					SYS._str(self.ManagementDict.keys())
				]
			)
			'''
			
			#/##################/#
			# determine the StructureKeyStrsList
			#

			#Check
			if StructureManagerCommandKeyRigidVariable==None:

				#all the key 
				StructureKeyStrsList=[]

			#Check
			elif type(StructureManagerCommandKeyRigidVariable
			)==list and len(StructureManagerCommandKeyRigidVariable
				)>0 and type(StructureManagerCommandKeyRigidVariable[0])==str:

				#alias
				StructureKeyStrsList=StructureManagerCommandKeyRigidVariable
			
			#Check
			elif StructureManagerCommandKeyRigidVariable=="#all":

				#all the key 
				StructureKeyStrsList=self.ManagementDict.keys()

			else:

				#mapCondition
				StructureKeyStrsList=self.mapCondition(
					StructureManagerCommandKeyRigidVariable,
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
			
			#filterNone
			CommandingKeyVariable=SYS.filterNone(
						map(
							lambda __KeyStr:
							self.ManagementDict[__KeyStr]
							if __KeyStr in self.ManagementDict
							else None,
							StructureKeyStrsList
						)
					)

			#/##################/#
			# Maybe sort
			#

			"""
			#debug
			self.debug(
				[
					'before sort',
					'CommandingKeyVariable is ',
					SYS._str(CommandingKeyVariable)
				]
			)

			#sort
			CommandingKeyVariable=SYS.sort(
					CommandingKeyVariable
				)

			#debug
			self.debug(
				[
					'after sort',
					'CommandingKeyVariable is ',
					SYS._str(CommandingKeyVariable)
				]
			)
			"""

			#set
			setattr(
				self,
				'CommandingKeyVariable',
				CommandingKeyVariable
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
			self.CommandingSetVariable=self.StructureTeamerCommandSetRigidList

		else:

			#alias
			self.CommandingSetVariable=self.StructureManagerCommandSetRigidList

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
					('StructureTopDeriveStructurerRigidVariable',self.CommandTopDeriveCommanderRigidVariable),
					('StructureTeamerCommandKeyRigidVariable',self.StructureTeamerCommandKeyRigidVariable),
					('StructureManagerCommandKeyRigidVariable',self.StructureManagerCommandKeyRigidVariable),
					('StructureTeamerCommandSetRigidList',self.StructureTeamerCommandSetRigidList),
					('StructureManagerCommandSetRigidList',self.StructureManagerCommandSetRigidList),
					('parent')
		]

		#add
		self.CommandingSetVariable=CommandingSetVariable+self.CommandingSetVariable+[
			('setCommandingKeyVariable'),
			('setCommandingSetVariable'),
			('StructureTopDeriveStructurerRigidVariable',None),
			('StructureTeamerCommandKeyRigidVariable',None),
			('StructureManagerCommandKeyRigidVariable',None),
			('StructureTeamerCommandSetRigidList',None),
			('StructureManagerCommandSetRigidList',None),
		]

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
StructurerClass.ManagingValueClass=StructurerClass
StructurerClass.TeamingValueClass=StructurerClass

#</DefineLocals>

#</DefinePrint>
StructurerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'StructureTagStr',
		'StructureTopDeriveStructurerRigidVariable',
		'StructureTeamerCommandKeyRigidVariable',
		'StructureManagerCommandKeyRigidVariable',
		'StructureTeamerCommandSetRigidList',
		'StructureManagerCommandSetRigidList',
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
		'StructuredTeamKeyStrsList',
		'StructuredOnceBool'
	]
)
#<DefinePrint>
