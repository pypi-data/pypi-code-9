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
from ShareYourSystem.Standards.Itemizers import Setter,Pather
#</ImportSpecificModules>

#<DefineLocals>
ParentPreviousStr="^"
ParentTopStr="Top"
#</DefineLocals>

#<DefineClass>
@DecorationClass(
	**{'ClassingSwitchMethodStrsList':['parent']}
)
class ParenterClass(BaseClass):

	def default_init(self,
				_ParentKeyStr="Top",
				_ParentDeriveTeamerVariable=None,
				_ParentTopDeriveTeamerVariable=None,
				_ParentingTopGetVariable=None,
				_ParentingClimbBool=True,
				_ParentingTriggerVariable=None,
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
			# Check if we have to climb to parent the parent
			#

			#debug
			'''
			self.debug('We are going to parent the parent')
			'''
			
			"""
			#Parent the parent maybe
			if self.ParentingClimbBool:

				#debug
				'''
				self.debug('First we make parent the parent')
				'''
				
				#parent the parent
				ParentedDeriveTeamerVariable.parent(
						self.ParentingTopGetVariable,
						self.ParentingClimbBool
					)

				#debug
				'''
				self.debug(
						[
							'Ok parent has parented',
							'ParentedDeriveTeamerVariable is '+SYS._str(
								ParentedDeriveTeamerVariable
							)
						]
					)
				'''
			"""

			#/####################/#
			# Now build the chain of Teamers and Managers
			#

			#add
			self.ParentedTotalDeriveTeamersList=[
				ParentedDeriveTeamerVariable
			]+ParentedDeriveTeamerVariable.ParentedTotalDeriveTeamersList

			#add
			if self.TeamTagStr=="":

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

			#/####################/#
			# Command things
			#

			#debug
			'''
			self.debug(('self.',self,['ParentingTopGetVariable']))
			'''

			"""
			#Check
			if self.ParentingTopGetVariable!=None:

				#Check
				if type(self.ParentingTopGetVariable)==list:

					#debug
					'''
					self.debug(
							'This is a list'
						)
					'''
					
					#get
					ParentedValueVariablesList=self.ParentTopDeriveTeamerVariable[
							'#map@get'](
											*self.ParentingTopGetVariable
									).ItemizedMapValueVariablesList
									
					
					#debug
					'''
					self.debug('ParentedValueVariablesList is '+str(ParentedValueVariablesList))
					'''

					#Link
					self['#map@set'](
								zip(
									self.ParentingTopGetVariable,
									ParentedValueVariablesList
								)
						)

				else:

					#Link
					self.set(
							self.ParentingTopGetVariable,
							self.ParentTopDeriveTeamerVariable[
								self.ParentingTopGetVariable
							]
						)
			"""
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
		self.TeamedValueVariable.ParentDeriveTeamerVariable=self
		self.TeamedValueVariable.ParentKeyStr=self.TeamingKeyStr

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
		
	def mimic_manage(self):

		#call the base method
		BaseClass.manage(self)

		#debug
		'''
		self.debug(
				('self.',self,['ManagingKeyStr'])
			)
		'''

		#set
		self.ManagedValueVariable.ParentDeriveTeamerVariable=self
		self.ManagedValueVariable.ParentKeyStr=self.ManagingKeyStr

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

		#Check
		elif self.GettingKeyVariable==ParentAllStr:

			#add
			self.GettedValueVariable=self.ManagementDict.values()+self.TeamDict.values()

			#Stop the setting
			return {"HookingIsBool":False}

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

	def getWatchAfterParentWithParenterBool(self):

		#try
		try:
			return getattr(self,'_WatchAfterParentWithParenterBool')
		except:
			return False

	def setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#set the value of the "hidden" property variable
		self._WatchAfterParentWithParenterBool=_SettingValueVariable

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
			
		else:

			#debug
			'''
			self.debug('We have switched the parent here !')
			'''

	def delWatchAfterParentWithParenterBool(self):
		self.__delattr__('_WatchAfterParentWithParenterBool')

	WatchAfterParentWithParenterBool=property(
			getWatchAfterParentWithParenterBool,
			setWatchAfterParentWithParenterBool,
			delWatchAfterParentWithParenterBool,
			'WatchAfterParentWithParenterBool is now reactive !'
		)


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
			'ParentingClimbBool',
			'ParentedTotalDeriveTeamersList',
			'ParentedDeriveTeamersList',
			'ParentedDeriveManagersList',
			#'ParentedTotalPathStr',
			'ParentedTeamPathStr',
			'ParentedManagementPathStr',
	]
)
#<DefinePrint>
