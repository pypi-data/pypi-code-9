# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Teamer defines Child ordered dicts with <DoStr> as KeyStr. 
The items inside are automatically setted with Teamed<DoStr><TypeStr> and have 
a parent InstanceVariable. This is the beginning for buiding high
arborescent and (possibly circular) structures of objects.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Commander"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
from ShareYourSystem.Standards.Itemizers import Pather
#</ImportSpecificModules>

#<DefineLocals>
TeamChildPrefixStr='-'
TeamDirectChildPrefixStr='-#direct:'
class TeamDict(SYS.ListDict):pass
SYS.TeamDict=TeamDict
#</DefineLocals>


#<DefineClass>
@DecorationClass()
class TeamerClass(BaseClass):

	def default_init(self,
				_TeamTagStr="",
				_TeamIndexInt=-1,
				_TeamDict=None,
				_TeamingKeyStr="",	
				_TeamingValueRigidVariable=None,	
				_TeamingManageVariable=None,					
				_TeamingValueClass=BaseClass, 	
				_TeamingClassesDict=None,
				_TeamingBeforeSetVariable=None,
				_TeamingAfterSetVariable=None,
				_TeamingWrapBool=True,
				_TeamingIndexInt=-1,
				_TeamedValueVariable=None,	
				_TeamedInBool=False,
				_TeamedOnceBool=False,																
				**_KwargVariablesDict
			):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#init
		self.TeamDict=TeamDict()

	def do_team(self):

		#debug
		'''
		self.debug(
			[
				'We team here',
				('self.',self,[
						'TeamingKeyStr',
						'TeamingValueRigidVariable'
					])
			]
		)
		'''

		#/###################/#
		# Force the repr with the ManagementDict
		#

		#Check
		if self.TeamedOnceBool==False:

			#Extend
			self.PrintingInstanceForceKeyStrsList.extend(
				[
					'TeamDict',
					#'ManagementTagStr'
				]
			)

			#set
			self.TeamedOnceBool=True


		#reset
		self.TeamingValueClass=self.__class__.TeamingValueClass
		
		#/###################/#
		# Is it a new teamed value
		#

		#in
		self.TeamedInBool=self.TeamingKeyStr in self.TeamDict

		#debug
		'''
		self.debug(
				[
					'Is it a new teamed value ?',
					('self.',self,[
						'TeamingKeyStr',
						'TeamedInBool'
					])
				]
			)
		'''
		
		#Check
		if self.TeamedInBool==False:

			#debug
			'''
			self.debug(
				[
					'This is a new teamed value',
					('self.',self,['TeamingKeyStr'])
				]
			)
			'''

			#/####################/#
			# Check if there is a special type for this
			# 

			#debug
			'''
			self.debug(
					[
						'Is there a special type for this',
						('self.',self,['TeamingClassesDict','TeamingKeyStr'])
					]
				)
			'''

			#Check
			if self.TeamingKeyStr in self.TeamingClassesDict:

				#get
				self.TeamingValueClass=self.TeamingClassesDict[
					self.TeamingKeyStr
				]

				#debug
				'''
				self.debug(
						[
							'There is a special type for this',
							('self.',self,['TeamingValueClass'])
						]
					)
				'''

			#/####################/#
			# do we have to init 
			#

			#Check
			if self.TeamingValueRigidVariable==None:

				#init
				self.TeamedValueVariable=self.TeamingValueClass()

			else:

				#alias
				self.TeamedValueVariable=self.TeamingValueRigidVariable

			#/####################/#
			# Case where it is a dict or tuples list like
			# we wrap then in a manager new object if TeamingWrapBool

			#temp
			TeamedTempValueVariable=None

			#Check
			if self.TeamingWrapBool and (
				hasattr(
					self.TeamedValueVariable,
					'items'
				) or SYS.getIsTuplesListBool(self.TeamedValueVariable)
			):

				#debug
				'''
				self.debug(
						[
							'This is a team with a value dict',
							'We wrap into an instance',
							('self.',self,[
								'TeamingKeyStr',
								'TeamingValueClass',
								'TeamingClassesDict'
								])
						]
					)
				'''
					
				#temp and init
				TeamedTempValueVariable=self.TeamedValueVariable
				self.TeamedValueVariable=self.TeamingValueClass()

				#debug
				'''
				self.debug(
						[
							'Ok the wrapped dict has been setted'
						]
					)
				'''
				
			#/####################/#
			# Set different way to access it in the object
			# 

			#Check
			if self.TeamingIndexInt>-1:

				#debug
				'''
				self.debug(
					[
						'We team by inserting',
						('self.',self,[
								'TeamingIndexInt'
							])
					]
				)
				'''

				#insert
				self.TeamDict.insert(
					self.TeamingIndexInt,
					self.TeamedValueVariable,
					self.TeamingKeyStr,
					"Team"
				)

			else:

				#debug
				'''
				self.debug(
					[
						'We team by just setting'
					]
				)
				'''
				
				#put in the dict
				self.TeamDict[
					self.TeamingKeyStr
				]=self.TeamedValueVariable

			#Check
			if self.TeamingWrapBool:

				#define the keystr to define in the dict
				TeamedKeyStr=self.TeamingKeyStr+type(
						self.TeamedValueVariable
					).NameStr

				#set in the __dict__
				self.__setattr__(
						TeamedKeyStr,
						self.TeamedValueVariable
					)

				#add in the RepresentingSkipKeyStrsList to not be seen in the repr
				self.PrintingInstanceSkipKeyStrsList.append(TeamedKeyStr)

				#/##########################/
				# Give some team attributes
				#

				#set
				self.TeamedValueVariable.TeamTagStr=self.TeamingKeyStr

				#index
				if self.TeamingIndexInt>-1:
					self.TeamedValueVariable.TeamIndexInt=self.TeamingIndexInt
				else:
					self.TeamedValueVariable.TeamIndexInt=len(self.TeamDict)-1

				#/##########################/
				# If there are shared before set values
				#

				#debug
				'''
				self.debug(
					[
						'The Teamer has something before for the teamed value ?',
						('self.',self,['TeamingBeforeSetVariable'])
					]
				)
				'''

				#Check
				if self.TeamingBeforeSetVariable!=None:

					#debug
					'''
					self.debug(
						[
							'The Teamer has something before for the teamed value',
							('self.',self,['TeamingBeforeSetVariable'])
						]
					)
					'''

					#map set
					self.TeamedValueVariable['#map@set'](
						self.TeamingBeforeSetVariable	
					)

					#self.TeamedValueVariable.mapSet(
					#	self.TeamingBeforeSetVariable	
					#)

				#/##########################/
				# If the value itself was a set variable
				#

				#Check
				if TeamedTempValueVariable!=None:

					#debug
					'''
					self.debug(
							[
								'We team with a TeamedValueVariable',
								'TeamedTempValueVariable is ',
								SYS._str(TeamedTempValueVariable)
							]
						)
					'''
					
					#set with the value
					self.TeamedValueVariable['#map@set'](
							TeamedTempValueVariable
						)

				#/##########################/
				# If there are shared after set values
				#
				
				#Check
				if self.TeamingAfterSetVariable!=None:

					#debug
					'''
					self.debug(
							[
								'The Teamed has something after for the teamed value',
								('self.',self,['TeamingAfterSetVariable'])
							]
						)
					'''

					#map set
					self.TeamedValueVariable['#map@set'](
						self.TeamingAfterSetVariable	
					)

		else:

			##########################
			# just get and update 
			#

			#debug
			'''
			self.debug(
					[
						'We just get the teamed value'
					]
				)
			'''
			
			#get
			self.TeamedValueVariable=self.TeamDict[self.TeamingKeyStr]
			
			#debug
			'''
			self.debug(
					[
						'We update the teamed value',
						('self.',self,['TeamingValueRigidVariable'])
					]
				)
			'''

			#Check
			if hasattr(
				self.TeamingValueRigidVariable,
				'items'
			) or SYS.getIsTuplesListBool(self.TeamingValueRigidVariable):

				#Check
				if self.TeamingWrapBool:

					#set
					self.TeamedValueVariable['#map@set'](
							self.TeamingValueRigidVariable
						)

		#/###################/#
		# reset rigid variable
		#

		#set
		self.TeamingValueRigidVariable=None

	def mimic_get(self):

		#Definition
		OutputDict={'HookingIsBool':True}

		#debug
		'''
		self.debug(
			[
				('self.',self,['GettingKeyVariable'])
			]
		)
		'''

		#Check
		if type(
			self.GettingKeyVariable
		)==str:

			#Check
			if self.GettingKeyVariable==TeamChildPrefixStr:

				#return 
				self.GettedValueVariable=self.TeamDict

				#Stop the setting
				return {'HookingIsBool':False}

			elif self.GettingKeyVariable.startswith(TeamChildPrefixStr):

				#deprefix
				GetKeyStr=SYS.deprefix(
						self.GettingKeyVariable,
						TeamChildPrefixStr
					)

				#Check
				if GetKeyStr[0]!='.':

					#debug
					'''
					self.debug(
						[
							'We team here',
							('self.',self,['GettingKeyVariable'])
						]
					)
					'''

					#team
					self.GettedValueVariable=self.team(
						GetKeyStr
					).TeamedValueVariable

					#Stop the setting
					return {'HookingIsBool':False}

				else:

					#debug
					'''
					self.debug(
						[
							'We team here',
							('self.',self,['GettingKeyVariable'])
						]
					)
					'''

					#team
					self.GettedValueVariable=getattr(
						self.TeamDict,
						GetKeyStr[1:]
					)()

					#Stop the setting
					return {'HookingIsBool':False}

		#Call the parent get method
		return BaseClass.get(self)

	def mimic_set(self):

		#Definition
		OutputDict={'HookingIsBool':True}

		#debug
		'''
		self.debug(('self.',self,['SettingKeyVariable']))
		'''

		#Check
		if type(
			self.SettingKeyVariable
		)==str:

			#Check
			if self.SettingKeyVariable.startswith(
				TeamDirectChildPrefixStr
			):

				#debug
				'''
				self.debug(
					[
						'We team here without instancing',
						('self.',self,['SettingKeyVariable'])
					]
				)
				'''
		
				#team
				self.team(
					SYS.deprefix(
						self.SettingKeyVariable,
						TeamDirectChildPrefixStr
					),
					self.SettingValueVariable,
					_WrapBool=False
				)
				self.TeamingWrapBool=True

				#Stop the setting
				return {'HookingIsBool':False}

			#Check
			elif self.SettingKeyVariable.startswith(
				TeamChildPrefixStr
			):

				#debug
				'''
				self.debug(
					[
						'We team here',
						('self.',self,['SettingKeyVariable'])
					]
				)
				'''

				#team
				self.team(
					SYS.deprefix(
						self.SettingKeyVariable,
						TeamChildPrefixStr
					),
					self.SettingValueVariable
				)

				#Stop the setting
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
		
		#Call the parent get method
		return BaseClass.set(self)

	def __contains__(self,_KeyStr):
		return _KeyStr in self.ManagementDict

	def getTeamer(self,_KeyStr,_IndexInt=-1):

		#Check
		if _KeyStr in self.TeamDict:

			#get
			return self.TeamDict[
				_KeyStr
			]

		else:

			#team
			return self.team(
				_KeyStr,
				_IndexInt=_IndexInt
			).TeamedValueVariable
		
#</DefineClass>


#</DefinePrint>
TeamerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'TeamTagStr',
		'TeamIndexInt',
		'TeamDict',
		'TeamingKeyStr',
		'TeamingValueRigidVariable',
		'TeamingClassesDict',
		'TeamingManageVariable',
		'TeamingClassesDict',
		'TeamingValueClass',
		'TeamingBeforeSetVariable',
		'TeamingAfterSetVariable',
		'TeamingWrapBool',
		'TeamingIndexInt',
		'TeamedValueVariable',
		'TeamedInBool',
		'TeamedOnceBool'
	]
)
#<DefinePrint>
