# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Celler defines template of Mardown and Code Cells for readming a Module.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Guiders.Capturer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
import six
import copy
#</ImportSpecificModules>

#<DefineLocals>
CellInitDict={
				'metadata': {
								'name': "",
								'signature': ""
							},
				'nbformat': 3,
				'nbformat_minor': 0,
				'worksheets': []
			}

CellCodeCellDict={
						'cell_type':'code',
						'collapsed': False,
						'input':[],
						'language': "python",
						'metadata': {'slideshow':{'slide_type':"slide"}},
						'prompt_number':0
					}

CellOutputDict={
						'output_type': "stream",
						'stream': "stdout",
						'text': [														
								]
					}

CellMarkdownCellDict={
							'source': "", 
							'cell_type': 'markdown', 
							'metadata': {'slideshow':{'slide_type':"slide"}}
						} 
#</DefineLocals>


#<DefineClass>
@DecorationClass()
class CellerClass(BaseClass):
						
	def default_init(self,
						_CellingTextStr="",
						_CellingScriptStr="",
						_CelledOutputStr="",
						_CelledNoteDict=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_cell(self):

		#Check
		if self.CellingTextStr=="":
			self.CellingTextStr=self.FiledReadVariable

		#Debug
		'''
		self.debug(
			[
				'We cell here',
				('self.',self,[
						'FolderingPathVariable',
						'CellingTextStr'
					]
				)
			]
		)
		'''
		
		#Check Code case
		if self.CellingScriptStr=='Python':
			
			#folder first
			self.folder()

			#Definition the self.CelledOutputStr
			if self.FolderingPathVariable!=os.getcwd()+'/':		
		
				#capture and six method
				self.CapturedPrintStrsList=[]
				self.capture()
				six.exec_(self.CellingTextStr,vars())
				self.CapturingStopBool=True
				self.CelledOutputStr='\n'.join(self.CapturedPrintStrsList)

			else:

				#Avoid the output of the corresponding NameStr because it will do a circular effect...
				self.CelledOutputStr=""


			#Debug
			'''
			self.debug(('self.',self,['CelledOutputStr']))
			'''

			#Return 
			self.CelledNoteDict=dict(
				copy.deepcopy(CellCodeCellDict),
				**{
					'input':map(	
								lambda __LineStr:
								__LineStr+'\n',
								self.CellingTextStr.replace(
									"#FrozenIsBool True",""
							).replace(
								"#FrozenIsBool False",""
							).replace(
								'\t',
								'    '
							).replace('    \n','\n').split('\n')
						),
						"outputs":[
						dict(
							copy.copy(CellOutputDict),
								**
								{
									"text":map(	
											lambda __LineStr:
											__LineStr+'\n',
											self.CelledOutputStr.split('\n')
										)
								}
							)
						]
				}
			)

		#Check Markdown case
		elif self.CellingScriptStr=='Markdown':

			self.CelledNoteDict=dict(
				copy.deepcopy(CellMarkdownCellDict),
				**{
						'source':self.CellingTextStr
				}
			)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Display or not several things
			#

			#map
			map(
					lambda __KeyStr:
					self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList.append(
						__KeyStr
					) if getattr(self.PrintingCopyVariable,__KeyStr)==None
					else 
						self.forcePrint(
							[__KeyStr],
							'CellerClass'
						),
					[
						'CelledNoteDict'
					]
				)


		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)
	
#</DefineClass>

#</DefinePrint>
CellerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'CellingTextStr',
		'CellingScriptStr',
		'CelledOutputStr',
		'CelledNoteDict'
	]
)
#<DefinePrint>
