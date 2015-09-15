# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Manager completes the list of grand-manage nodes that 
a child node could have. It acts only at one level.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Teamer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
import collections
from ShareYourSystem.Standards.Itemizers import Pather
Teamer=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
ManagementChildPrefixStr="|"
ManagementDirectChildPrefixStr="|#direct:"
sort=SYS.sort
class ManagementDict(SYS.ListDict):
	
	def sort(self):

		#/#################/#
		# Resort the dict
		#

		#sort
		ValueVariablesList=sort(self.values())

		#reset by deleting
		map(
			lambda __KeyStr:
			self.__delitem__(__KeyStr),
			self.keys()
		)

		#update
		self.update(
			zip(
				map(
					lambda __ValueVariable:
					__ValueVariable.ManagementTagStr,
					ValueVariablesList
				),
				map(
					lambda __IndexIntAndValueVariable:
					__IndexIntAndValueVariable[1].setAttr(
						'ManagementIndexInt',
						__IndexIntAndValueVariable[0]
					),
					enumerate(
						ValueVariablesList
					)
				)
			)
		)
		
SYS.ManagementDict=ManagementDict
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ManagerClass(BaseClass):

	def default_init(
				self,
				_ManagementTagStr="",
				_ManagementIndexInt=-1,
				_ManagementDict=None,
				_ManagingKeyStr="",
				_ManagingValueRigidVariable=None,
				_ManagingValueClass=Teamer.TeamerClass,
				_ManagingBeforeSetVariable=None,
				_ManagingAfterSetVariable=None,
				_ManagingClassesDict=None,
				_ManagingWrapBool=True,
				_ManagingIndexInt=-1,
				_ManagedValueVariable=None,
				_ManagedInBool=False,
				_ManagedOnceBool=False,
				**_KwargVariablesDict
			):	

		#Call the manage init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#Init the ManagementDict
		self.ManagementDict=ManagementDict()
		
	def do_manage(self):

		#debug
		'''
		self.debug(
			('self.',self,[
					'ManagingKeyStr',
					'ManagingValueRigidVariable',
					'ManagingWrapBool'
				])
		)
		'''
		
		#/###################/#
		# Force the repr with the ManagementDict
		#

		#Check
		if self.ManagedOnceBool==False:

			#extend
			self.PrintingInstanceForceKeyStrsList.extend(
				[
					'ManagementDict',
					#'TeamTagStr'
				]
			)

			#set
			self.ManagedOnceBool=True

		#reset
		self.TeamingValueClass=self.__class__.TeamingValueClass

		#/###################/#
		# Is it a new managed value
		#

		#in
		self.ManagedInBool=self.ManagingKeyStr in self.ManagementDict

		#debug
		'''
		self.debug(
				[
					'Is it a new managed value ?',
					('self.',self,[
						'ManagingKeyStr',
						'ManagedInBool'
					])
				]
			)
		'''
		
		#Check
		if self.ManagedInBool==False:

			#debug
			'''
			self.debug(
				[
					'This is a new managed value',
					('self.',self,['ManagingKeyStr'])
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
						('self.',self,['ManagingClassesDict','ManagingKeyStr'])
					]
				)
			'''

			#Check
			if self.ManagingKeyStr in self.ManagingClassesDict:

				#get
				self.ManagingValueClass=self.ManagingClassesDict[
					self.ManagingKeyStr
				]

				#debug
				'''
				self.debug(
						[
							'There is a special type for this',
							('self.',self,['ManagingValueClass'])
						]
					)
				'''

			#/####################/#
			# do we have to init 
			#

			#debug
			'''
			self.debug(
				[
					'This is a new managed value',
					('self.',self,[
							'ManagingKeyStr',
							'ManagingValueRigidVariable'
						]
					),
					'Check first if this managingkey str is known'
				]
			)
			'''
			
			#Check
			if self.ManagingValueRigidVariable==None:

				#init
				self.ManagedValueVariable=self.ManagingValueClass()

			else:

				#alias
				self.ManagedValueVariable=self.ManagingValueRigidVariable

			#/####################/#
			# Case where it is a dict or tuples list like
			# we wrap then in a teamer new object and ManagingWrapBool

			#temp
			ManagedTempValueVariable=None

			#Check
			if self.ManagingWrapBool and (
				hasattr(
					self.ManagedValueVariable,
					'items'
				) or SYS.getIsTuplesListBool(self.ManagedValueVariable)
			):

				#debug
				'''
				self.debug(
						[
							'This is a manage with a value dict',
							'We wrap into an instance',
							('self.',self,[
								'ManagingKeyStr',
								'ManagingValueClass',
								'ManagingClassesDict'
								])
						]
					)
				'''

				#Check
				if self.ManagingKeyStr in self.ManagingClassesDict:

					#get
					self.ManagingValueClass=self.ManagingClassesDict[
						self.ManagingKeyStr
					]

					#debug
					'''
					self.debug(
							[
								'There is a special type for this',
								('self.',self,['ManagingValueClass'])
							]
						)
					'''
				
				#temp and init
				ManagedTempValueVariable=self.ManagedValueVariable
				self.ManagedValueVariable=self.ManagingValueClass()
				
				#debug
				'''
				self.debug(
						[
							'Ok the wrapped dict has been setted',
							('self.',self,['ManagedValueVariable']),
							'ManagedTempValueVariable is ',
							SYS._str(ManagedTempValueVariable)
						]
					)
				'''

			#/####################/#
			# Set different way to access it in the object
			# 

			#Check
			if self.ManagingIndexInt>-1:

				#debug
				'''
				self.debug(
					[
						'We manage by inserting',
						('self.',self,[
								'ManagingIndexInt'
							])
					]
				)
				'''

				#insert
				self.ManagementDict.insert(
					self.ManagingIndexInt,
					self.ManagedValueVariable,
					self.ManagingKeyStr,
					"Management"
				)

			else:

				#debug
				'''
				self.debug(
					[
						'We manage by just setting'
					]
				)
				'''

				#put in the dict
				self.ManagementDict[
					self.ManagingKeyStr
				]=self.ManagedValueVariable


			#put in the dict
			self.ManagementDict[
				self.ManagingKeyStr
			]=self.ManagedValueVariable

			#Check
			if self.ManagingWrapBool:

				#debug
				'''
				self.debug(
					[
						'We set also in the __dict__...'
					]
				)
				'''

				#define the keystr to define in the dict
				ManagedKeyStr=self.ManagingKeyStr+type(
							self.ManagedValueVariable
						).NameStr

				#set in the __dict__
				self.__setattr__(
						ManagedKeyStr,
						self.ManagedValueVariable
					)

				#add in the RepresentingSkipKeyStrsList to not be seen in the repr
				self.PrintingInstanceSkipKeyStrsList.append(ManagedKeyStr)

				#/########################/#
				# give some manage attributes
				#

				#set
				self.ManagedValueVariable.ManagementTagStr=self.ManagingKeyStr

				#index
				if self.ManagingIndexInt>-1:
					self.ManagedValueVariable.ManagementIndexInt=self.ManagingIndexInt
				else:
					self.ManagedValueVariable.ManagementIndexInt=len(self.ManagementDict)-1

				#/##########################/
				# If there are shared before set values
				#

				#debug
				'''
				self.debug(
					[
						'The Manager has something before for the managed value ?',
						('self.',self,['ManagingBeforeSetVariable'])
					]
				)
				'''

				#Check
				if self.ManagingBeforeSetVariable!=None:

					#debug
					'''
					self.debug(
							[
								'The Manager has something before for the managed value',
								('self.',self,['ManagingBeforeSetVariable'])
							]
						)
					'''
					
					#map set
					self.ManagedValueVariable['#map@set'](
						self.ManagingBeforeSetVariable	
					)


				#/##########################/
				# If the value itself was a set variable
				#

				#debug
				'''
				self.debug(
						[
							'There was a ManagedTempValueVariable here',
							'ManagedTempValueVariable!=None is',
							str(ManagedTempValueVariable!=None)
						]
					)
				'''

				#Check
				if ManagedTempValueVariable!=None:

					#debug
					'''
					self.debug(
							[
								'We manage with a ManagedValueVariable',
								'ManagedTempValueVariable is ',
								SYS._str(ManagedTempValueVariable)
							]
						)
					'''

					#set with the value
					self.ManagedValueVariable['#map@set'](
							ManagedTempValueVariable
						)

				#/##########################/
				# If there are shared after set values
				#
				

				#Check
				if self.ManagingAfterSetVariable!=None:

					#debug
					'''
					self.debug(
							[
								'The Manager has something after for the managed value',
								('self.',self,['ManagingAfterSetVariable'])
							]
						)
					'''

					#map set
					self.ManagedValueVariable['#map@set'](
						self.ManagingAfterSetVariable	
					)

		else:

			#/########################/#
			# just get and update 
			#

			#debug
			'''
			self.debug(
					[
						'Ok we just get'
					]
				)
			'''

			#get
			self.ManagedValueVariable=self.ManagementDict[
				self.ManagingKeyStr
			]
			
			#debug
			'''
			self.debug(
					[
						'We maybe update',
						('self.',self,['ManagingValueRigidVariable'])
					]
				)
			'''

			#Check
			if hasattr(
				self.ManagingValueRigidVariable,
				'items'
			) or SYS.getIsTuplesListBool(self.ManagingValueRigidVariable):

				#Check
				if self.ManagingWrapBool:

					#set
					self.ManagedValueVariable['#map@set'](
							self.ManagingValueRigidVariable
						)

		#/###################/#
		# reset rigid variable
		#

		#debug
		'''
		self.debug(
			[
				'We reset the ManagingValueRigidVariable',
				('self.',self,['ManagingValueRigidVariable'])
			]
		)
		'''
		
		#set
		self.ManagingValueRigidVariable=None


	def mimic_get(self):

		#Definition
		OutputDict={'HookingIsBool':True}

		#debug
		'''
		self.debug(
			('self.',self,['GettingKeyVariable'])
		)
		'''
		
		#Check
		if self.GettingKeyVariable==ManagementChildPrefixStr:

			#debug
			'''
			self.debug('We get all the children teams')
			'''

			#return
			self.GettedValueVariable=self.ManagementDict

			#Stop the getting
			return {'HookingIsBool':False}

		elif type(
			self.GettingKeyVariable
		)==str:

			#Check
			if self.GettingKeyVariable.startswith(
				ManagementChildPrefixStr
			):

				#deprefix
				GetKeyStr=SYS.deprefix(
						self.GettingKeyVariable,
						ManagementChildPrefixStr
					)

				#Check
				if GetKeyStr[0]!='.':

					#debug
					'''
					self.debug(
						[
							'We manage here',
							"SYS.deprefix(self.GettingKeyVariable,ManagementChildPrefixStr) is",
							SYS.deprefix(self.GettingKeyVariable,ManagementChildPrefixStr)
						]
					)
					'''

					#manage
					self.GettedValueVariable=self.manage(
						SYS.deprefix(self.GettingKeyVariable,ManagementChildPrefixStr)
					).ManagedValueVariable

					#debug
					'''
					self.debug(
						[
							'Ok we have managed',
							('self.',self,['GettedValueVariable'])
						]
					)
					'''

					#Stop the getting
					return {'HookingIsBool':False}

				#Check
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
						self.ManagementDict,
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
				ManagementDirectChildPrefixStr
			):

				#debug
				'''
				self.debug(
					[
						'We manage here without instancing',
						('self.',self,['SettingKeyVariable'])
					]
				)
				'''
		
				#manage
				self.manage(
					SYS.deprefix(
						self.SettingKeyVariable,
						ManagementDirectChildPrefixStr
					),
					self.SettingValueVariable,
					_WrapBool=False
				)
				self.ManagingWrapBool=True

				#Stop the setting
				return {'HookingIsBool':False}

			elif self.SettingKeyVariable.startswith(
				ManagementChildPrefixStr
			):

				#debug
				'''
				self.debug('We manage here')
				'''

				#manage
				self.manage(
					SYS.deprefix(
						self.SettingKeyVariable,
						ManagementChildPrefixStr
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
		
		#return 
		return BaseClass.set(self)

	def __contains__(self,_KeyStr):
		return _KeyStr in self.ManagementDict

	def getManager(self,_KeyStr,_IndexInt=-1):

		#Check
		if _KeyStr in self.ManagementDict:

			#get
			return self.ManagementDict[
				_KeyStr
			]

		else:

			#manage
			return self.manage(
				_KeyStr,
				_IndexInt=_IndexInt
			).ManagedValueVariable


#</DefineClass>

#set
SYS.TeamerClass.TeamingValueClass=ManagerClass

#</DefinePrint>
ManagerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ManagementTagStr',
		'ManagementIndexInt',
		'ManagementDict',
		'ManagingKeyStr',
		'ManagingValueRigidVariable',
		'ManagingValueClass',
		'ManagingClassesDict',
		'ManagingBeforeSetVariable',
		'ManagingAfterSetVariable',
		'ManagingWrapBool',
		'ManagingIndexInt',
		'ManagedValueVariable',
		'ManagedInBool',
		'ManagedOnceBool'
	]
)
#<DefinePrint>
