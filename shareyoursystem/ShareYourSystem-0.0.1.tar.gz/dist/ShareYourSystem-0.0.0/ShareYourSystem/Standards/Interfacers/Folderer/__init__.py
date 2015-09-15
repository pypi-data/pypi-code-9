# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Folderer is a quick object helping for getting the FolderedDirKeyStrsList
at a specified directory or in the current one by default

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Explorer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import json
import os
import sys
#</ImportSpecificModules>

#<DefineLocals>
class ModuleDict(dict):
	
	def __init__(self,_DictVariable=None,_ModuleVariable=None,**_KwargVariablesDict):

		#Call the parent init method
		if _DictVariable!=None:
			dict.__init__(self,_DictVariable,**_KwargVariablesDict)
		else:
			dict.__init__(self,**_KwargVariablesDict)

		#Debug
		'''
		print('PackageDict l 39')
		print('_ModuleVariable is ')
		print(_ModuleVariable)
		print('')
		'''

		#import
		self._import(_ModuleVariable)

	def _import(self,_ModuleVariable):

		#Check
		if type(_ModuleVariable) in SYS.StrTypesList:
			self['ModuleVariable']=None
			self['ModuleStr']=_ModuleVariable
		else:
			self['ModuleVariable']=_ModuleVariable
			self['ModuleStr']=_ModuleVariable.__name__

		#Check for a module
		if self['ModuleVariable']==None or self['ModuleStr']!=self['ModuleVariable'].__name__:

			#Check
			if self['ModuleStr']!="":

				#Import the module if not already
				if self['ModuleStr'] not in sys.modules:
					importlib.import_module(self['ModuleStr'])

				#set with sys
				self['ModuleVariable']=sys.modules[
					self['ModuleStr']
				]

		#set
		if self['ModuleVariable']!=None:

			#set
			self['InstallFolderPathStr']='/'.join(
				self['ModuleVariable'].__file__.split('/')[:-1]
			)+'/'

			#set
			self['LocalFolderPathStr']=SYS.PythonlogyLocalFolderPathStr+self['ModuleVariable'].__name__.replace(
				'.','/')+'/'
			

#</DefineLocals>

#<DefineClass>
@DecorationClass()
class FoldererClass(BaseClass):
	"""
		FoldererClass ...

	"""

	def default_init(self,
						_FolderingPathVariable=None,
						_FolderingMkdirBool=False,
						_FolderingImportBool=True,
						_FolderedPathStr="",
						_FolderedModuleDict=None,
						_FolderedDirKeyStrsList=None,	
						_FolderedModuleStr="",
						_FolderedParentModuleStr="",
						_FolderedNameStr="",
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)
	
	def do_folder(self,**_KwargVariablesDict):

		#/################/#
		# Adapt the current path str
		#

		#debug
		'''
		self.debug(
			[
				'We folder here',
				('self.',self,[
						'FolderingPathVariable'
					])
			]
		)
		'''

		#set
		if self.FolderingPathVariable==None:

			#/################/#
			# Get the current
			#

			#Get the current
			FolderedCurrentPathStr=os.getcwd()

			#add
			self.FolderedPathStr=FolderedCurrentPathStr+'/'

		elif type(self.FolderingPathVariable)==str:

			#/################/#
			# This is a path str query
			#

			#set
			self.FolderedPathStr=self.FolderingPathVariable

		else:

			#/################/#
			# Get info on the already imported module
			#

			#module
			self.FolderedModuleDict=ModuleDict(
						_ModuleVariable=self.FolderingPathVariable
					)

			#set
			self.FolderedPathStr=self.FolderedModuleDict['LocalFolderPathStr']


		#/################/#
		# Now do things with that
		#

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'FolderedPathStr'
					])
			]
		)
		'''
			
		#Check
		if self.FolderedPathStr!="":

			#Add the '/' if not in the end
			if self.FolderedPathStr[-1]!="/":
				self.FolderedPathStr+="/"

			#/################/#
			# Maybe build the dir
			#

			#Build intermediar pathes
			if os.path.isdir(self.FolderedPathStr)==False:

				#Check
				if self.FolderingMkdirBool:

					#debug
					'''
					print('We are going to build the intermediar folder')
					print('self.FolderingPathVariable is ',self.FolderingPathVariable)
					print('')
					'''

					#Definition
					FolderedPathStrsList=self.FolderedPathStr.split('/')
					FolderedRootPathStr=FolderedPathStrsList[0]
					for _PathStr in FolderedPathStrsList[1:]:

						#debug
						'''
						print('FolderedRootPathStr is ',FolderedRootPathStr)
						print('')
						'''

						#Mkdir if it doesn't exist
						if FolderedRootPathStr!="" and os.path.isdir(FolderedRootPathStr)==False:
							os.popen('mkdir '+FolderedRootPathStr)

						#Add the following
						FolderedRootPathStr+='/'+_PathStr

					#Mkdir if it doesn't exist
					if os.path.isdir(FolderedRootPathStr)==False:
						os.popen('mkdir '+FolderedRootPathStr)

		#/################/#
		# Find the Module str maybe that is associated
		#

		#Recheck
		if os.path.isdir(self.FolderedPathStr):

			#set
			self.FolderedDirKeyStrsList=os.listdir(
				self.FolderedPathStr
			)

			#Check
			if '__init__.py' in self.FolderedDirKeyStrsList:

				#set maybe FolderedModuleStr and FolderedParentModuleStr if we are located in the SYS path
				if 'ShareYourSystem' in self.FolderedPathStr:

					#Check
					if self.FolderedModuleDict==None:

						#module
						self.FolderedModuleDict=ModuleDict(
									_ModuleVariable=self.FolderingPathVariable
								)

					#set
					self.FolderedModuleStr='ShareYourSystem'+self.FolderedPathStr.split(
						'ShareYourSystem')[-1].replace('/','.')

					#Remove the ossibly last dot
					if self.FolderedModuleStr[-1]=='.':
						self.FolderedModuleStr=self.FolderedModuleStr[:-1]

					#set
					if '.' in self.FolderedModuleStr:

						#set
						self.FolderedNameStr=self.FolderedModuleStr.split('.')[-1]

						#debug
						'''
						self.debug(('self.',self,['FolderingPathVariable','FolderedNameStr']))
						'''
						
						#set the parent
						self.FolderedParentModuleStr=self.FolderedNameStr.join(
							self.FolderedModuleStr.split(self.FolderedNameStr)[:-1]
						)
						if len(self.FolderedParentModuleStr
							)>0 and self.FolderedParentModuleStr[-1]=='.':
							self.FolderedParentModuleStr=self.FolderedParentModuleStr[:-1]
					else:
						self.FolderedModuleStr=self.FolderedModuleStr

			else:

				#set
				self.FolderedModuleStr=""
				self.FolderedParentModuleStr=""







#</DefineClass>

#</DefinePrint>
FoldererClass.PrintingClassSkipKeyStrsList.extend(
	[
		'FolderingPathVariable',
		'FolderingMkdirBool',
		'FolderingImportBool',
		'FolderedPathStr',
		'FolderedDirKeyStrsList',	
		'FolderedModuleDict',
		'FolderedModuleStr',
		'FolderedParentModuleStr',
		'FolderedNameStr',
		#'FolderedModuleDict'
	]
)
#<DefinePrint>