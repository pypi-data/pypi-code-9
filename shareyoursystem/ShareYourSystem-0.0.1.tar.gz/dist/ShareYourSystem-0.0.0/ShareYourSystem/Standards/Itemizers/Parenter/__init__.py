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
SYS.addDo('Parenter','Parent','Parenting','Parented')
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
from ShareYourSystem.Standards.Itemizers import Setter,Pather,Teamer
from ShareYourSystem.Standards.Interfacers import Printer
Manager=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
ParentPreviousStr="^"
ParentGrandPreviousStr="^^"
ParentTopStr="Top"
ParentUpStr="?^"
ParentDownStr="?v"
ParentMutePrefixStr='!'
SYS.addSingPlural('Child','Children')
SYS.addSingPlural('GrandChild','GrandChildren')
ListDict=SYS.ListDict
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
				_ParentTagStr="",
				_ParentTeamTagStr="",
				_ParentManagementTagStr="",
				_ParentGrandTeamTagStr="",
				_ParentGrandManagementTagStr="",
				_ParentDeriveTeamerVariable=None,
				_ParentGrandDeriveTeamerVariable=None,
				_ParentTopDeriveTeamerVariable=None,
				_ParentingTriggerVariable=None,
				_ParentedTotalDeriveParentersList=None,
				_ParentedTotalDeriveTeamersList=None,
				_ParentedTotalDeriveManagersList=None,
				_ParentedTotalListDict=None,
				_ParentedTotalSingularListDict=None,
				_ParentedTotalPathStr="",
				_ParentedTeamPathStr="",
				_ParentedManagementPathStr="",
				_ParentedTriggerVariablesList=None,
				**_KwargVariablesDict
			):	

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#init
		self.ParentedTotalDeriveParentersList=[]
		self.ParentedTotalDeriveTeamersList=[]
		self.ParentedTotalDeriveManagersList=[]
		
		#set top
		self.ParentTopDeriveTeamerVariable=self

		#update
		#self.TeamingBeforeSetVariable=SYS.update(self.TeamingBeforeSetVariable,[('ParentDeriveTeamerVariable',self)])
		#self.ManagingBeforeSetVariable=SYS.update(self.ManagingBeforeSetVariable,[('ParentDeriveTeamerVariable',self)])

	def do_parent(self):

		#get 
		ParentedDeriveTeamerVariable=self.ParentDeriveTeamerVariable

		#debug
		'''
		self.debug(
			[
				'We parent here',
				('self.',self,[
					#'ManagementPointDeriveTeamer',
					'NameStr'
				]),
				'ParentedDeriveTeamerVariable!=None is',
				str(ParentedDeriveTeamerVariable!=None)
			]
		)
		'''

		#Check
		if ParentedDeriveTeamerVariable!=None:

			#/####################/#
			# Set shortly the grand parent
			#

			if hasattr(self.ParentDeriveTeamerVariable,'ParentGrandDeriveTeamerVariable'):
				
				#get
				self.ParentGrandDeriveTeamerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

				#Check
				if self.ParentGrandDeriveTeamerVariable!=None:
						
					#Check		
					if self.ParentGrandDeriveTeamerVariable.TeamTagStr!="":

						#set
						self.ParentGrandTeamTagStr=self.ParentGrandDeriveTeamerVariable.TeamTagStr

					#Check		
					if self.ParentGrandDeriveTeamerVariable.ManagementTagStr!="":

						#set
						self.ParentGrandManagementTagStr=self.ParentGrandDeriveTeamerVariable.ManagementTagStr


			#/####################/#
			# Now build the list chain of Teamers and Managers
			#

			#add
			self.ParentedTotalDeriveParentersList=[
				ParentedDeriveTeamerVariable
			]+ParentedDeriveTeamerVariable.ParentedTotalDeriveParentersList

			#add
			if self.TeamTagStr!="":

				#add
				self.ParentedTotalDeriveTeamersList=[
					ParentedDeriveTeamerVariable
				]+ParentedDeriveTeamerVariable.ParentedTotalDeriveTeamersList

				#set
				self.ParentedTotalDeriveManagersList=ParentedDeriveTeamerVariable.ParentedTotalDeriveManagersList

			else:

				#add
				self.ParentedTotalDeriveManagersList=[
					ParentedDeriveTeamerVariable
				]+ParentedDeriveTeamerVariable.ParentedTotalDeriveManagersList

				#set
				self.ParentedTotalDeriveTeamersList=ParentedDeriveTeamerVariable.ParentedTotalDeriveTeamersList


			#/####################/#
			# Now build the ordered dict chain of Teamers and Managers
			#

			#dict
			self.ParentedTotalListDict=ListDict(
				map(
					lambda __ParentedTotalDeriveParenter:
					(
						__ParentedTotalDeriveParenter.TeamTagStr
						if __ParentedTotalDeriveParenter.TeamTagStr!=""
						else __ParentedTotalDeriveParenter.ManagementTagStr,
						__ParentedTotalDeriveParenter
					),
					self.ParentedTotalDeriveParentersList
				)
			)

			#debug
			'''
			self.debug(
				[
					'The ParentedTotalListDict is setted',
					'self.ParentedTotalListDict.keys() is ',
					str(self.ParentedTotalListDict.keys())
				]
			)
			'''

			#Check
			if self.ParentDeriveTeamerVariable.TeamTagStr!='':

				#init with
				self.ParentedTotalSingularListDict=ListDict(
					[(
						SYS.getSingularStrWithPluralStr(
							self.ParentDeriveTeamerVariable.TeamTagStr
						),
						self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
					)]
				)
			else:

				#init
				self.ParentedTotalSingularListDict=ListDict()

			#dict
			self.ParentedTotalSingularListDict.update(
				SYS.filterNone(
					map(
						lambda __ParentedTotalDeriveTeamer:
						(
							SYS.getSingularStrWithPluralStr(
								__ParentedTotalDeriveTeamer.ParentDeriveTeamerVariable.TeamTagStr
							),
							__ParentedTotalDeriveTeamer
						)
						if __ParentedTotalDeriveTeamer.ParentDeriveTeamerVariable!=None
						else None,
						self.ParentedTotalDeriveTeamersList
					)
				)
			)



			#/####################/#
			# Now build the paths
			#

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
						'ParentedTotalDeriveParentersList',
						'ParentedTotalDeriveTeamersList',
						'ParentedTotalDeriveManagersList',
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
			if len(self.ParentedTotalDeriveParentersList)>0:

				#last one
				self.ParentTopDeriveTeamerVariable=self.ParentedTotalDeriveParentersList[-1]
							
			#debug
			'''
			self.debug(
					('self.',self,['ParentTopDeriveTeamerVariable'])
				)
			'''

		else:

			#set
			self.ParentTopDeriveTeamerVariable=self

		#debug
		'''
		self.debug(
			[
				'Finally',
				('self.',self,['ParentTopDeriveTeamerVariable'])
			]
		)
		'''

		#/####################/#
		# link to the ParentTagStr
		# 

		#set
		self.ParentTagStr=self.ParentedTotalPathStr.replace('/','_')+'_'+self.ParentKeyStr

		#/####################/#
		# Adapt the shape of the ParentedTriggerVariablesList
		# for the trigger

		#init
		self.ParentedTriggerVariablesList=SYS.SetList(
				self.ParentingTriggerVariable
			)

	def mimic_team(self):

		#/#################/#
		# Call the base method
		#

		#debug
		'''
		self.debug(
				[
					'We team here',
					'call the parent method firsts',
					('self.',self,[
						'TeamingKeyStr',
						'ParentChildSetVariable'
					])
				]
			)
		'''

		#call the base method
		BaseClass.team(self)

		#/#################/#
		# Set the parent in the child
		#

		#debug
		'''
		self.debug(
				('self.',self,['TeamingKeyStr'])
			)
		'''
		
		#set
		if hasattr(self.TeamedValueVariable,'ParentDeriveTeamerVariable'):

			#Check
			if self.TeamedValueVariable.ParentDeriveTeamerVariable!=self:
				self.TeamedValueVariable.ParentDeriveTeamerVariable=self
				self.TeamedValueVariable.ParentKeyStr=self.TeamingKeyStr
				self.TeamedValueVariable.ParentManagementTagStr=self.TeamedValueVariable.ParentDeriveTeamerVariable.ManagementTagStr

			#/###################/#
			# Look maybe for a grandparent
			#

			#debug
			'''
			self.debug(
					[
						'We look for a grand parent here',
						('self.',self,['ParentDeriveTeamerVariable'])
					]
				)
			'''
			
			#set
			self.TeamedValueVariable.ParentGrandDeriveTeamerVariable=self.ParentDeriveTeamerVariable

			#Check
			if self.TeamedValueVariable.ParentGrandDeriveTeamerVariable!=None:
							
				#set
				self.TeamedValueVariable.ParentGrandTeamTagStr=self.TeamedValueVariable.ParentGrandDeriveTeamerVariable.TeamTagStr

	def mimic_manage(self):

		#/#################/#
		# Call the base method
		#

		#debug
		'''
		self.debug(
				[
					'We manage here',
					'call the base method first'
				]
			)
		'''

		#call the base method
		BaseClass.manage(self)

		#/#################/#
		# Set the parent in the child
		#

		#debug
		'''
		self.debug(
				('self.',self,['ManagingKeyStr'])
			)
		'''

		#Check
		if hasattr(self.ManagedValueVariable,'ParentDeriveTeamerVariable'):

			#Check
			if self.ManagedValueVariable.ParentDeriveTeamerVariable!=self:

				#set
				self.ManagedValueVariable.ParentDeriveTeamerVariable=self
				self.ManagedValueVariable.ParentKeyStr=self.ManagingKeyStr
				self.ManagedValueVariable.ParentTeamTagStr=self.ManagedValueVariable.ParentDeriveTeamerVariable.TeamTagStr

			#/###################/#
			# Look maybe for a grandparent
			#

			#set
			self.ManagedValueVariable.ParentGrandDeriveTeamerVariable=self.ParentDeriveTeamerVariable

			#Check
			if self.ManagedValueVariable.ParentGrandDeriveTeamerVariable!=None:
	
				#set
				self.ManagedValueVariable.ParentGrandManagementTagStr=self.ManagedValueVariable.ParentGrandDeriveTeamerVariable.ManagementTagStr

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

		elif self.GettingKeyVariable==ParentGrandPreviousStr:
			
			#debug
			'''
			self.debug('We get the previous grand parent')
			'''

			#alias
			self.GettedValueVariable=self.ParentGrandDeriveTeamerVariable

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
			self.debug(
					[
						'We command a up parent'
					]
				)

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
		if type(self.SettingKeyVariable)==str: 

			#/##################/#
			# Special DeriveParentTeamerVariable case
			# just setattr to make the set shorter

			#Check
			if self.SettingKeyVariable=='ParentDeriveTeamerVariable':

				#set
				self.ParentDeriveTeamerVariable=self.SettingValueVariable

				#return
				return {'HookingIsBool':False}

			#/##################/#
			# Special Mute case
			#

			#Check
			elif self.SettingKeyVariable.startswith(
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

	"""
	def mimic_array(self):

		#call the parent method
		BaseClass.array(self)

		#parent down
		if self.ArrayingTopBool:
			self.get('?v')
	"""
	
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
					('self.',self,[
							'ParentedTotalPathStr',
							'ParentedTriggerVariablesList'
						]),
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
					'self is '+SYS._str(self)
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

	def mimic__print(self,**_KwargVariablesDict):

		#debug
		'''
		print('Parenter 525')
		print('self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList is ')
		print(self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList)
		print('')
		'''
		
		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#map
			map(
					lambda __ItemTuple:
					self.PrintingCopyVariable.TeamDict.__setitem__(
						__ItemTuple[0],
						Printer.getPointerStr(__ItemTuple[1])+" (Empty)"
					) 
					if hasattr(
						__ItemTuple[1],'ManagementDict'
					) and len(__ItemTuple[1].ManagementDict)==0
					else None,
					self.PrintingCopyVariable.TeamDict.items()
				)

		#Check
		if self.ParentedTotalPathStr!="":

			#Check
			if hasattr(self.PrintingCopyVariable,'PrintingInfoStr'):

				#add
				self.PrintingCopyVariable.PrintingInfoStr+=' ^'

			
		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

	def parentUp(self,**_KwargVariablesDict):

		#debug
		'''
		self.debug(
			[
				'we parent up here',
				'self.ParentDeriveTeamerVariable!=None is ',
				str(self.ParentDeriveTeamerVariable!=None)
			]
		)
		'''

		#/###############/#
		# First make parent the parent
		#

		#Check
		if self.ParentDeriveTeamerVariable!=None:

			#make the parent first
			self.ParentDeriveTeamerVariable.parentUp(**_KwargVariablesDict)

		#/###############/#
		# Set here the kwargs
		#

		#Check
		if len(_KwargVariablesDict)>0:

			#map
			map(
					lambda __ItemTuple:
					setattr(
						self,
						*__ItemTuple
					),
					_KwargVariablesDict.items()
				)

		#/###############/#
		# parent here
		#

		#parent
		self.parent()

		#return self
		return self


	def parentDown(self,
			_TeamVariable=None,
			_ManagementVariable=None,
			_HookMethodStr="",
			**_KwargVariablesDict
		):

		#debug
		'''
		self.debug(
			[
				'We parent down here',
				('self.',self,[
					'TeamedOnceBool'
				]),
				'_TeamVariable is ',
				str(_TeamVariable),
				'_ManagementVariable is ',
				str(_ManagementVariable)
			]
		)
		'''

		#/###############/#
		# Set here the kwargs
		#

		#Check
		if len(_KwargVariablesDict)>0:
			
			#map
			map(
					lambda __ItemTuple:
					setattr(
						self,
						*__ItemTuple
					),
					_KwargVariablesDict.items()
				)

		#/###############/#
		# First parent here
		#

		#debug
		'''
		self.debug(
			[
				'Check if we have to parent',
				('self.',self,['WatchAfterParentWithParenterBool'])
			]
		)
		'''

		#parent
		self.parent()

		#Check
		if _HookMethodStr!="" and hasattr(self,_HookMethodStr):

			#call
			getattr(self,_HookMethodStr)()

		#/###############/#
		# Command the children to parent down also
		#

		#debug
		self.debug(
			[
				'Look how to parentDown the children',
				('self.',self,['TeamedOnceBool'])
			]
		)

		#Check
		if self.TeamedOnceBool:

			#/###############/#
			# Determine the TeamStrsList
			#

			if _TeamVariable==None:
				TeamStrsList=self.TeamDict.keys()
			elif len(_TeamVariable)>0 and type(_TeamVariable[0])==str:
				TeamStrsList=self.TeamDict
			else:
				TeamStrsList=self.mapCondition(
					_TeamVariable,
					self.TeamDict.keys(),
					_DirectBool=True
				)

			#debug
			'''
			self.debug(
				[
					'_TeamVariable is ',
					str(_TeamVariable),
					'TeamStrsList is ',
					str(TeamStrsList)
				]
			)
			'''

			#/#################/#
			# Get the teams and parent switching the key strs
			#

			#map
			map(
					lambda __ElementVariable:
					__ElementVariable.parentDown(
						_TeamVariable,
						_ManagementVariable,
						_HookMethodStr,
						**_KwargVariablesDict
					)
					if hasattr(__ElementVariable,'parentDown')
					else None,
					map(
						lambda __TeamStr:
						self.TeamDict[
							__TeamStr
						],
						TeamStrsList
					)
				)

		else:

			#/###############/#
			# Determine the ManagementStrsList
			#

			if _ManagementVariable==None:
				ManagementStrsList=self.ManagementDict.keys()
			elif len(_ManagementVariable)>0 and type(_ManagementVariable)==str:
				ManagementStrsList=self.ManagementDict
			else:
				ManagementStrsList=self.mapCondition(
					_ManagementVariable,
					self.ManagementDict.keys(),
					_DirectBool=True
				)

			#debug
			'''
			self.debug(
				[
					'_ManagementVariable is ',
					str(_ManagementVariable),
					'ManagementStrsList is ',
					str(ManagementStrsList)
				]
			)
			'''

			#/#################/#
			# Get the managements and parent switching the key strs
			#

			#map
			map(
					lambda __ElementVariable:
					__ElementVariable.parentDown(
						_TeamVariable,
						_ManagementVariable,
						_HookMethodStr,
						**_KwargVariablesDict
					)
					if hasattr(__ElementVariable,'parentDown')
					else None,
					map(
						lambda __ManagementStr:
						self.ManagementDict[
							__ManagementStr
						],
						ManagementStrsList
					)
					
				)

		#return self
		return self

	def getParenterStr(self):

		#get
		ParenterStr=Printer.getPointerStr(
						self
					)

		#Check
		if self.TeamedOnceBool:
			ParenterStr+=' with : '+str(self.TeamDict.keys())
		elif self.ManagedOnceBool:
			ParenterStr+=' with : '+str(self.ManagementDict.keys())

		#return
		return ParenterStr

	def __contains__(self,_KeyStr):

		#Check
		if self.TeamedOnceBool:
			return _KeyStr in self.TeamDict
		elif self.TeamedOnceBool:
			return _KeyStr in self.ManagementDict
		else:
			return (_KeyStr in self.TeamDict) or (_KeyStr in self.ManagementDict)

	def __len__(self):

		#Check
		if self.TeamedOnceBool:
			return len(self.TeamDict)
		elif self.TeamedOnceBool:
			return len(self.ManagementDict)
		else:
			return 0
#</DefineClass>

#Set
SYS.ManagerClass.ManagingValueClass=ParenterClass
SYS.TeamerClass.TeamingValueClass=ParenterClass

#</DefinePrint>
ParenterClass.PrintingClassSkipKeyStrsList.extend(
	[
			'ParentKeyStr',
			'ParentTagStr',
			'ParentTeamTagStr',
			'ParentManagementTagStr',
			'ParentGrandTeamTagStr',
			'ParentGrandManagementTagStr',
			'ParentDeriveTeamerVariable',
			'ParentGrandDeriveTeamerVariable',
			'ParentTopDeriveTeamerVariable',
			'ParentingTriggerVariable',
			'ParentedTotalDeriveParentersList',
			'ParentedTotalDeriveTeamersList',
			'ParentedTotalDeriveManagersList',
			'ParentedTotalSingularListDict',
			'ParentedTotalListDict',
			'ParentedTotalPathStr',
			'ParentedTeamPathStr',
			'ParentedManagementPathStr',
			'ParentedTriggerVariablesList'
	]
)
#<DefinePrint>
