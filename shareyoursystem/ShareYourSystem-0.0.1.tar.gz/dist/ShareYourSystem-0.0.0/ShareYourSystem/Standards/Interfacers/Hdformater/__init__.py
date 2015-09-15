# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


An Hdformater instance maps an apply and so "grinds" a MappingArgDictsList 
to a method.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Pymongoer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import importlib
import os
import sys
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['hdformat']
})
class HdformaterClass(BaseClass):
	
	def default_init(self,
			_HdformatGroupPathStr={
				'DefaultValueType':property,
				'PropertyInitVariable':'/',
				'PropertyDocStr':'I set a path of groups'
			},
			_HdformatingFileKeyStr="", 
			_HdformatingModuleStr="tables",			
			_HdformatedFileVariable=None, 
			_HdformatedFilePathStr="",		
			_HdformatedConsoleStr="", 			
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_hdformat(self):

		#debug
		'''
		self.debug(('self.',self,[
									'HdformatingFileKeyStr'
								]))
		'''
		
		#Check
		if self.HdformatedFileVariable==None:

			#folder first
			self.folder()

			#set
			self.HdformatedFilePathStr=self.FolderingPathVariable+self.HdformatingFileKeyStr
			
			#Maybe we have to import
			if self.HdformatingModuleStr not in sys.modules:

				#debug
				'''
				self.debug('We import first the hdf module')
				'''

				#Import
				importlib.import_module(self.HdformatingModuleStr)

			#Check
			if self.HdformatingFileKeyStr!="":

				#Check for first write
				if os.path.isfile(self.HdformatedFilePathStr)==False:

					#debug
					'''
					self.debug('We create the file first')
					'''

					#Create the file 
					self.HdformatedFileVariable=sys.modules[self.HdformatingModuleStr].File(
										self.HdformatedFilePathStr,'w')
						
					#Close it
					self.HdformatedFileVariable.close()

				if self.HdformatedFileVariable==None or ( 
					(self.HdformatingModuleStr=='tables' and self.HdformatedFileVariable.isopen==0
						) or (self.HdformatingModuleStr=='h5py' and self.HdformatedFileVariable.mode=='c') ):

					#debug
					'''
					self.debug('We open the file')
					'''

					#Open the HdformatedFileVariable
					self.HdformatedFileVariable=sys.modules[self.HdformatingModuleStr].File(
						self.HdformatedFilePathStr,'r+')

			#link
			self.FiledHardVariable=self.HdformatedFileVariable

	def hdfview(self):

		#debug
		'''
		self.debug(('self.',self,['HdformatingFilePathStr']))
		'''

		if self.HdformatedFilePathStr!="":
		
			#set the HdformatedConsoleStr
			self.HdformatedConsoleStr=os.popen(
				SYS.h5lsPathStr+' -dlr '+self.HdformatedFilePathStr
			).read()
		
		#Return self
		return self.HdformatedConsoleStr

	def mimic_file(self):

		#Call the base method
		BaseClass.file(self)

		#Check
		if self.FilingModeStr=='c': 

			#Close the HdformatedFileVariable
			if self.HdformatedFileVariable!=None:
				self.HdformatedFileVariable.close()

	def propertize_setHdformatGroupPathStr(self,_SettingValueVariable):

		#Check
		if _SettingValueVariable[0]!='/':
			_SettingValueVariable='/'+_SettingValueVariable

		#set
		self._HdformatGroupPathStr=_SettingValueVariable

		#Debug
		'''
		self.debug(
				[
					'We have setted a HdformatGroupPathStr',
					('self.',self,[
						'HdformatedFileVariable',
						'_HdformatGroupPathStr'
					])
				]
			)
		'''
		
		#/##################/#
		# Check that we have the File of the Top parent
		# 

		#Check
		if self.HdformatedFileVariable==None:

			#Check
			if self.ParentTopDeriveTeamerVariable.HdformatedFileVariable==None:
				self.ParentTopDeriveTeamerVariable.hdformat()

			#alias
			self.HdformatedFileVariable=self.ParentTopDeriveTeamerVariable.HdformatedFileVariable

		#/##################/#
		# Set a path inside
		#

		#Check if the Path exists
		if self._HdformatGroupPathStr not in self.HdformatedFileVariable:

			#set all the intermediate Paths before
			PathStrsList=self._HdformatGroupPathStr.split('/')[1:]
			ParsingChildPathStr="/"

			#set the PathStr from the top to the down (integrativ loop)
			for __ChildPathStr in PathStrsList:

				#Go deeper
				NewParsingChildPathStr=ParsingChildPathStr+__ChildPathStr

				#Create the group if not already
				if NewParsingChildPathStr not in self.HdformatedFileVariable:
					if self.HdformatingModuleStr=="tables":
						self.HdformatedFileVariable.create_group(
							ParsingChildPathStr,__ChildPathStr
						)
					elif self.HdformatingModuleStr=="h5py":
						Group=self.HdformatedFileVariable[ParsingChildPathStr]
						Group.create_group(__ChildPathStr)
				
				#Prepare the next group	
				ParsingChildPathStr=NewParsingChildPathStr+'/'

#</DefineClass>


#</DefinePrint>
HdformaterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'HdformatGroupPathStr',
		'HdformatingFileKeyStr',
		'HdformatingModuleStr',
		'HdformatedFileVariable',
		'HdformatedConsoleStr',
		'HdformatedFilePathStr'
	]
)
#<DefinePrint>
