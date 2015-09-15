# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Parenter completes the list of grand-parent nodes that 
a child node could have. It acts only at one level.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Manager"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
from ShareYourSystem.Standards.Itemizers import Setter,Pather,Teamer
Manager=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
ParentPreviousStr="^"
ParentTopStr="Top"
ParentUpStr="?^"
ParentDownStr="?v"
ParentMutePrefixStr='!'
#</DefineLocals>

#<DefineClass>
@DecorationClass(
	**{
	'ClassingSwitchMethodStrsList':[
		'parent'
	]
}
)
class ParenterClass(BaseClass):

	def default_init(self,
				_ParentKeyStr={
					'DefaultValueType':property,
					'PropertyInitVariable':"Top",
					'PropertyDocStr':'I am reactive when I know my parent !'
				},
				_ParentDeriveTeamerVariable=None,
				_ParentTopDeriveTeamerVariable=None,
				_ParentingTriggerVariable=None,
				_ParentingClassesDict=None,
				_ParentedTotalDeriveTeamersList=None,
				_ParentedDeriveTeamersList=None,
				_ParentedDeriveManagersList=None,
				_ParentedTotalPathStr="",
				_ParentedTeamPathStr="",
				_ParentedManagementPathStr="",
				_ParentedTriggerVariablesList=None,
				**_KwargVariablesDict
			):	

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#init
		self.ParentedTotalDeriveTeamersList=[]
		self.ParentedDeriveTeamersList=[]
		self.ParentedDeriveManagersList=[]
		
		#set top
		self.ParentTopDeriveTeamerVariable=self

	def do_parent(self):

		#debug
		'''
		self.debug(('self.',self,[
					#'ManagementPointDeriveTeamer',
					'NameStr'
				]))
		'''

		#get 
		ParentedDeriveTeamerVariable=self.ParentDeriveTeamerVariable

		#Check
		if ParentedDeriveTeamerVariable!=None:

			#/####################/#
			# Now build the chain of Teamers and Managers
			#

			#add
			self.ParentedTotalDeriveTeamersList=[
				ParentedDeriveTeamerVariable
			]+ParentedDeriveTeamerVariable.ParentedTotalDeriveTeamersList

			#add
			if self.TeamTagStr!="":

				#add
				self.ParentedDeriveTeamersList=[
					ParentedDeriveTeamerVariable
				]+ParentedDeriveTeamerVariable.ParentedDeriveTeamersList

				#set
				self.ParentedDeriveManagersList=ParentedDeriveTeamerVariable.ParentedDeriveManagersList

			else:

				#add
				self.ParentedDeriveManagersList=[
					ParentedDeriveTeamerVariable
				]+ParentedDeriveTeamerVariable.ParentedDeriveManagersList

				#set
				self.ParentedDeriveTeamersList=ParentedDeriveTeamerVariable.ParentedDeriveTeamersList

			#map 
			[
				self.ParentedTotalPathStr,
				self.ParentedTeamPathStr,
				self.ParentedManagementPathStr,
			]=map(
				lambda __ParentedList:
				Pather.PathPrefixStr+Pather.PathPrefixStr.join(
					SYS.reverse(
						map(
							lambda __ParentedDeriveTeamer:
							__ParentedDeriveTeamer.ParentKeyStr,
							__ParentedList
						)
					)
				),
				map(
					lambda __KeyStr:
					getattr(self,__KeyStr),
					[
						'ParentedTotalDeriveTeamersList',
						'ParentedDeriveTeamersList',
						'ParentedDeriveManagersList',
					]
				)
			)

			#debug
			'''
			self.debug(
					("self.",self,[
							'ParentedTotalPathStr',
							'ParentedTeamPathStr',
							'ParentedManagementPathStr'
						]
					)
				)
			'''
			
			#/####################/#
			# Set the top teamer variable
			#

			#Check
			if len(self.ParentedTotalDeriveTeamersList)>0:

				#last one
				self.ParentTopDeriveTeamerVariable=self.ParentedTotalDeriveTeamersList[-1]
							
			#debug
			'''
			self.debug(
					('self.',self,['ParentTopDeriveTeamerVariable'])
				)
			'''

		else:

			#set
			self.ParentTopDeriveTeamerVariable=self

		#/####################/#
		# Adapt the shape of the ParentedTriggerVariablesList
		# for the trigger

		#init
		self.ParentedTriggerVariablesList=SYS.SetList(
				self.ParentingTriggerVariable
			)

	def mimic_team(self):

		#call the base method
		BaseClass.team(self)

		#debug
		'''
		self.debug(
				('self.',self,['TeamingKeyStr'])
			)
		'''
		
		#set
		try:

			#Check
			if self.TeamedValueVariable.ParentDeriveTeamerVariable!=self:
				self.TeamedValueVariable.ParentDeriveTeamerVariable=self
				self.TeamedValueVariable.ParentKeyStr=self.TeamingKeyStr
		except:

			#pass
			pass

		#Check
		'''
		if self.ParentKeyStr=='Top':

			#debug
			self.debug('We are the top so we command a parent')

			#command
			self.command(
				['TeamDict.values','ManagementDict.values'],
				('parent',[]),
				_AfterWalkRigidBool=True
			)
		'''

		"""
		#hook a parent method
		if self.ParentTopDeriveTeamerVariable==self and hasattr(
			self.TeamedValueVariable,'parent'
		):

			#debug
			self.debug(
					[
						'We down parent in the TeamedValueVariable',
						('self.',self,['TeamedValueVariable'])
					]
				)

			#parent
			self.TeamedValueVariable.parent(_DownBool=True)
		"""

		"""
		#hook a parent method
		if len(self.TeamedValueVariable.ManagementDict)==0 and hasattr(
			self.TeamedValueVariable,'parent'
		):

			#debug
			self.debug(
					[
						'We up parent in the TeamedValueVariable',
						('self.',self,['TeamedValueVariable'])
					]
				)

			#parent
			self.TeamedValueVariable.parent(_UpBool=True)
		"""

	def mimic_manage(self):

		#call the base method
		BaseClass.manage(self)

		#debug
		'''
		self.debug(
				('self.',self,['ManagingKeyStr'])
			)
		'''

		try:

			#Check
			if self.ManagedValueVariable.ParentDeriveTeamerVariable!=self:

				#set
				self.ManagedValueVariable.ParentDeriveTeamerVariable=self
				self.ManagedValueVariable.ParentKeyStr=self.ManagingKeyStr

		except:

			#pass
			pass

		"""
		#hook a parent method
		if self.ParentTopDeriveTeamerVariable==self and hasattr(
			self.ManagedValueVariable,
			'parent'
		):

			#debug
			self.debug(
					[
						'We down parent in the ManagedValueVariable',
						('self.',self,['ManagedValueVariable'])
					]
				)

			#parent
			self.ManagedValueVariable.parent(_DownBool=True)
		"""

		"""
		#hook a parent method
		if len(self.ManagedValueVariable.TeamDict)==0 and hasattr(
			self.ManagedValueVariable,'parent'
		):

			#debug
			self.debug(
					[
						'We up parent in the TeamedValueVariable',
						('self.',self,['TeamedValueVariable'])
					]
				)

			#parent
			self.ManagedValueVariable.parent(_UpBool=True)
		"""

	def mimic_get(self):
		
		#debug
		'''
		self.debug(
				[
					('self.',self,[
							'GettingKeyVariable',
						])
				]
			)
		'''

		#Check
		if self.GettingKeyVariable==ParentPreviousStr:
			
			#debug
			'''
			self.debug('We get the previous parent')
			'''

			#alias
			self.GettedValueVariable=self.ParentDeriveTeamerVariable

			#Stop the setting
			return {"HookingIsBool":False}

		#Check
		elif self.GettingKeyVariable==ParentTopStr:
			
			#debug
			'''
			self.debug(
				[
					'We get the top parent',
					('self.',self,['ParentTopDeriveTeamerVariable'])
				]
			)
			'''

			#alias
			self.GettedValueVariable=self.ParentTopDeriveTeamerVariable

			#Stop the setting
			return {"HookingIsBool":False}
			
		elif self.GettingKeyVariable==ParentUpStr:
			
			#debug
			'''
			self.debug(
					'We command a up parent'
				)
			'''

			#command
			self.command(
					'^',
					'#call:parent',
					_BeforeWalkRigidBool=True,
					_AfterSelfRigidBool=True
				)

			#return
			return 

		elif self.GettingKeyVariable==ParentDownStr:
			
			#debug
			'''
			self.debug(
					'We command a down parent'
				)
			'''

			#command
			self.command(
					'+'+Teamer.TeamChildPrefixStr+'.values+'+Manager.ManagementChildPrefixStr+'.values',
					'#call:parent',
					_AfterWalkRigidBool=True,
					_BeforeSelfRigidBool=True
				)

			#return
			return

		#debug
		'''
		self.debug(
			[
				'get with the base method',
				'BaseClass is '+str(BaseClass)
			]
		)
		'''

		#Call the base method
		return BaseClass.get(self)

	def mimic_set(self):

		#Check
		if type(self.SettingKeyVariable)==str and self.SettingKeyVariable.startswith(
				ParentMutePrefixStr
			): 

			#deprefix
			MuteGetKeyStr=SYS.deprefix(
				self.SettingKeyVariable,
				ParentMutePrefixStr
			)

			#get
			MuteGetValueVariable=self[MuteGetKeyStr]

			#init
			#MuteSetValueVariable=self.SettingValueVariable()['#map@set'](
			#	MuteGetValueVariable.__dict__
			#)
			MuteSetValueVariable=self.SettingValueVariable()
			MuteSetValueVariable.__dict__=MuteGetValueVariable.__dict__

			#debug
			'''
			self.debug(
				[
					'We are going to mute...',
					'MuteGetKeyStr is '+str(MuteGetKeyStr),
					'MuteGetValueVariable.TeamTagStr is '+str(MuteGetValueVariable.TeamTagStr),
					'MuteGetValueVariable.ManagementTagStr is '+str(MuteGetValueVariable.ManagementTagStr),
					('self.',self,['SettingValueVariable']),
					'MuteSetValueVariable is ',
					SYS._str(MuteSetValueVariable)
				]
			)
			'''

			#Check
			if MuteGetValueVariable.ParentDeriveTeamerVariable.TeamedOnceBool:

				#debug
				'''
				self.debug(
						'We team again'
					)
				'''

				#del
				del MuteGetValueVariable.ParentDeriveTeamerVariable.TeamDict[
					MuteGetValueVariable.TeamTagStr
				]

				#team again
				MuteGetValueVariable.ParentDeriveTeamerVariable.team(
						MuteGetValueVariable.TeamTagStr,
						MuteSetValueVariable
					)

				#return
				return {'HookingIsBool':False}

			else:

				#debug
				'''
				self.debug(
						'We manage again'
					)
				'''

				#del
				del MuteGetValueVariable.ParentDeriveTeamerVariable.ManagementDict[
					MuteGetValueVariable.ManagementTagStr
				]

				#manage again
				MuteGetValueVariable.ParentDeriveTeamerVariable.manage(
						MuteGetValueVariable.ManagementTagStr,
						MuteSetValueVariable
					)

				#return
				return {'HookingIsBool':False}

		#Call the base method
		BaseClass.set(self)

	def mimic_array(self):

		#call the parent method
		BaseClass.array(self)

		#parent down
		if self.ArrayingTopBool:
			self.get('?v')

	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#set the value of the "hidden" property variable
		self._WatchAfterParentWithParenterBool=_SettingValueVariable

		#debug
		'''
		self.debug(
			[
				'We have parented here',
				'_SettingValueVariable is '+str(_SettingValueVariable)
			]
		)
		'''

		#Check
		if _SettingValueVariable:

			#debug
			'''
			self.debug(
				[
					'We have parented here !',
					('self.',self,['ParentedTotalPathStr']),
					'we launch the trigger'
				]
			)
			'''

			#trigger map@set
			self[Setter.SetMapStr](self.ParentedTriggerVariablesList)

			#debug
			'''
			self.debug(
				[
					'We have trigerred',
				]
			)
			'''

		else:

			#debug
			'''
			self.debug(
				'We have switched the parent here !'
			)
			'''

#</DefineClass>

#Set
SYS.ManagerClass.ManagingValueClass=ParenterClass
SYS.TeamerClass.TeamingValueClass=ParenterClass

#</DefinePrint>
ParenterClass.PrintingClassSkipKeyStrsList.extend(
	[
			'ParentKeyStr',
			'ParentDeriveTeamerVariable',
			'ParentTopDeriveTeamerVariable',
			#'ParentingTriggerVariable',
			'ParentingClassesDict',
			'ParentedTotalDeriveTeamersList',
			'ParentedDeriveTeamersList',
			'ParentedDeriveManagersList',
			#'ParentedTotalPathStr',
			'ParentedTeamPathStr',
			'ParentedManagementPathStr',
			'ParentedTriggerVariablesList'
	]
)
#<DefinePrint>
