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
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Pointer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
import collections
from ShareYourSystem.Standards.Itemizers import Pather
from ShareYourSystem.Standards.Itemizers import Pointer
#</ImportSpecificModules>

#<DefineLocals>
ManagementChildPrefixStr="$"
ManagementParentTeamerPrefixStr="<"
class ManagementDict(collections.OrderedDict):
	def __init__(self,_Dict=None):

		#Check
		if _Dict==None:
			_Dict={}

		#call the manage init method
		collections.OrderedDict.__init__(self,_Dict)

		#update
		self.update(_Dict)

SYS.ManagementDict=ManagementDict
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ManagerClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
								'ManagingKeyStr',
								'ManagingValueVariable',
								'ManagingValueClass',
								'ManagedValueVariable'
							]

	def default_init(
				self,
				_ManagingKeyStr="",
				_ManagingValueVariable=None,
				_ManagingValueClass=Pointer.PointerClass,
				_ManagedValueVariable=None,
				**_KwargVariablesDict
			):	

		#Call the manage init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#Init the ManagementDict
		self.ManagementDict=ManagementDict()

		##########################
		#init some team attributes
		#

		#Init
		self.TeamTagStr="Top"

		"""
		#point
		self.TeamPointDeriveTeamer=None
		"""
		
	def do_manage(self):

		#debug
		'''
		self.debug(
			('self.',self,[
					'ManagingKeyStr',
					'ManagingValueVariable'
				])
		)
		'''

		#Check
		if self.ManagingValueVariable==None:

			#try to get
			try:

				#get
				self.ManagedValueVariable=self.ManagementDict[
					self.ManagingKeyStr
				]

				#set
				self.ManagedIsBool=True
			
			except KeyError:

				#init
				self.ManagedValueVariable=self.ManagingValueClass()

				#set
				self.ManagedIsBool=False

		else:

			#init
			self.ManagedIsBool=False

			#alias
			self.ManagedValueVariable=self.ManagingValueVariable

		#Check
		if self.ManagedIsBool==False:

			#/####################/#
			# Case where it is a dict or tuples list like
			# we wrap then in a teamer new object

			#Check
			if hasattr(
				self.ManagedValueVariable,
				'items'
			) or SYS.getIsTuplesListBool(self.ManagedValueVariable):

				#init
				self.ManagedValueVariable=SYS.TeamerClass(
					)['#map@set'](
						self.ManagedValueVariable
					)

			#set in the __dict__
			self.__setattr__(
					self.ManagingKeyStr+type(
						self.ManagedValueVariable
					).NameStr,
					self.ManagedValueVariable
				)

			#put in the dict
			self.ManagementDict[
				self.ManagingKeyStr
			]=self.ManagedValueVariable

			##########################
			#give some manage attributes
			#

			#debug
			'''
			self.debug(
				'We make point the managed instance to self'
			)
			'''

			#set
			'''
			self.ManagingValueVariable.point(
					self,
					'ManagementPointDeriveManager'
				)
			'''
			self.ManagedValueVariable.ManagementPointDeriveManager=self

			#debug
			'''
			self.debug(
				'Ok it is pointed'
			)
			'''
			
			#set
			self.ManagedValueVariable.__setattr__(
				'ManagementTagStr',
				self.ManagingKeyStr
			)

			##########################
			#give some team-manage attributes
			#

			#debug
			'''
			self.debug(
				'We make point the managed instance to the parent team'
			)
			'''

			#set
			'''
			self.ManagingValueVariable.point(
					self[TeamParentPrefixStr+'Teamer'],
					'ManagementPointDeriveManager'
				)
			'''
			self.ManagedValueVariable.ManagementPointDeriveTeamer=self.TeamPointDeriveTeamer

			#debug
			'''
			self.debug(
				'Ok it is pointed'
			)
			'''
			
			#set
			self.ManagedValueVariable.__setattr__(
				'ManagementTeamTagStr',
				self.TeamTagStr
			)


	def mimic_get(self):

		#Definition
		OutputDict={'HookingIsBool':True}

		#debug
		'''
		self.debug(('self.',self,['GettingKeyVariable']))
		'''
		
		#Check
		if self.GettingKeyVariable==ManagementParentTeamerPrefixStr+'Teamer':
			
			#alias
			self.GettedValueVariable=self.TeamPointDeriveTeamer

			#Stop the setting
			OutputDict["HookingIsBool"]=False 

		#Check
		elif self.GettingKeyVariable==ManagementChildPrefixStr:

			#debug
			'''
			self.debug('We get all the children teams')
			'''

			#return
			self.GettedValueVariable=self.ManagementDict

			#Stop the getting
			OutputDict["HookingIsBool"]=False 

		elif type(
			self.GettingKeyVariable
		)==str and self.GettingKeyVariable.startswith(
			ManagementChildPrefixStr
		):

			#debug
			'''
			self.debug('We manage here')
			'''

			#team
			self.GettedValueVariable=self.manage(
				SYS.deprefix(
					self.GettingKeyVariable,
					ManagementChildPrefixStr
				)
			).ManagedValueVariable

			#debug
			'''
			self.debug(
				('self.',self,['GettedValueVariable'])
			)
			'''

			#Stop the getting
			OutputDict["HookingIsBool"]=False 

		#Call the parent get method
		if OutputDict['HookingIsBool']:
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
		)==str and self.SettingKeyVariable.startswith(
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
			OutputDict["HookingIsBool"]=False 

		#Call the manage get method
		if OutputDict['HookingIsBool']:
			return BaseClass.set(self)

#</DefineClass>

