# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Filer is a quick object for opening a FiledHardVariable and safely using (read,write) 
it depending on the FiledModeStr.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Folderer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
#</ImportSpecificModules>

#<DefineLocals>
FilingOrderStr='_'
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class FilerClass(BaseClass):

	def default_init(self,
						_FilingKeyStr="",
						_FilingModeStr='r',
						_FilingFormatStr='txt',
						_FilingWriteVariable=None,
						_FiledPathStr="",
						_FiledHardVariable=None,
						_FiledReadVariable=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_file(self,**_KwargVariablesDict):

		#Check
		if self.FilingModeStr!='c':

			#/###################/#
			# First open the file
			#

			#Call the folder method before
			self.folder()

			#debug
			'''
			self.debug(('self.',self,['FolderedPathStr']))
			'''

			#set the FiledPathStr
			if self.FolderedPathStr[-1]!='/':
				self.FolderedPathStr=self.FolderedPathStr+'/'
			self.FiledPathStr=self.FolderedPathStr+self.FilingKeyStr

			#Check
			if '.' in self.FilingKeyStr:
				self.FilingFormatStr=self.FilingKeyStr.split('.')[-1]

			#debug
			'''
			self.debug(
				('self.',self,[
						'FilingKeyStr',
						'FiledPathStr',
						'FilingModeStr',
						'FilingFormatStr',
						'FiledHardVariable'
					])
			)
			'''

			#Close before if we chaneg the mode
			if self.FiledHardVariable!=None:

				#Check
				if self.FiledHardVariable==self.FiledPathStr:

					#Return if it is the same mode already
					if self.FiledHardVariable.mode==self.FilingModeStr:
						return self

					#Check
					if self.FiledHardVariable.mode!='c':
						if ('w' in self.FilingModeStr and self.FiledHardVariable.mode=='r'
							) or ('r'==self.FilingModeStr and 'w' in self.FiledHardVariable.mode):
							self.FiledHardVariable.close()

				else:

					#Close
					self.FiledHardVariable.close()


			#Open the self.FilePointer
			if self.FilingModeStr=='r' and os.path.isfile(self.FiledPathStr):

				#debug
				'''
				self.debug('Open the file for reading !')
				'''

				#Open
				self.FiledHardVariable=open(self.FiledPathStr,self.FilingModeStr)

			else:

				#debug
				'''
				self.debug('Open the file for writing !')
				'''

				#Open
				self.FiledHardVariable=open(
					self.FiledPathStr,
					self.FilingModeStr
				)

		#Check
		else:

			#/###################/#
			# Case where we have to close
			#

			#close
			if self.FiledHardVariable!=None:
				self.FiledHardVariable.close()

		#/###################/#
		# Case where we have to write
		#

		if self.FilingModeStr=='w':	
			
			#debug
			self.debug(
					[
						'We write here',
						('self.',self,[
							'FilingFormatStr',
							#'FilingWriteVariable',
							'FiledPathStr'
						])
					]
				)

			#Check
			if self.FilingFormatStr in [
						'md',
						'txt',
						'sh',
					]:

				#Check
				if self.FilingWriteVariable==None:
					self.FilingWriteVariable=""

				#Read the FiledHardVariable
				self.FiledHardVariable.write(
					self.FilingWriteVariable
				)

			elif self.FilingFormatStr in [
				'json',
				'ipynb'
			]:

				#import
				import json
				
				#debug
				'''
				self.debug(
							[
								'we write in json...',
								'json.dumps(self.FilingWriteVariable,indent=2) is '+str(json.dumps(self.FilingWriteVariable,indent=2))
							]
					)
				'''
				
				#Use the json decoder
				self.FiledHardVariable.write(
					json.dumps(self.FilingWriteVariable,indent=2)
				)

			elif self.FilingFormatStr=='yaml':

				#import
				import yaml

				#debug
				'''
				print('We yamelized !')
				print('self.FiledHardVariable is ',self.FiledHardVariable)
				print('self.FilingWriteVariable is ',self.FilingWriteVariable)
				print('')
				'''

				#Use the json decoder
				self.FiledHardVariable.write(
					yaml.dump(self.FilingWriteVariable,indent=2)
				)

		#/###################/#
		# Case where we have to read
		#

		elif self.FilingModeStr=='r':
			
			#debug
			'''
			self.debug(
				[
					'We are going to read',
					('self.',self,[
						'FilingFormatStr'
						])
				]
			)
			'''
			
			#Check
			if self.FilingFormatStr in [
									'txt',
									'md',
									'py'
								]:

				#Read the FiledHardVariable
				self.FiledReadVariable=self.FiledHardVariable.read()

			elif self.FilingFormatStr in [
				'json',
				'ipynb'
			]:

				#import json
				import json

				#Use the json decoder
				self.FiledReadVariable=json.load(self.FiledHardVariable)

			elif self.FilingFormatStr=='yaml':

				#Use the json decoders
				self.FiledReadVariable=yaml.load(self.FiledHardVariable)




#</DefineClass>

#</DefinePrint>
FilerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'FilingKeyStr',
		'FilingModeStr',
		'FilingActionStr',
		'FilingFormatStr',
		'FilingWriteVariable',
		'FiledPathStr',
		'FiledHardVariable',
		'FiledReadVariable'
	]
)
#<DefinePrint>

