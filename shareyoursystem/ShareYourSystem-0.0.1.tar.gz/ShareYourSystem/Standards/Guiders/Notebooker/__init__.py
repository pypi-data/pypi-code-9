# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Notebooker takes piece of .md,.py,.tex files for putting them in a IPython Notebook

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Guiders.Celler"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
import os
import sys
from ShareYourSystem.Standards.Interfacers import Filer
from ShareYourSystem.Standards.Guiders import Guider
import importlib
Celler=BaseModule
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class NotebookerClass(BaseClass):
	
	def default_init(self,
						_NotebookingFileKeyStr="",
						_NotebookingWriteBool=True,
						_NotebookedTextStrsList=None,
						_NotebookedCodeDict=None,
						_NotebookedPageStrsList=None,
						_NotebookedSubslideStrsList=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_notebook(self):
		
		#debug
		'''
		self.debug(('self.',self,['NotebookingFileKeyStr']))
		'''

		#Check
		if self.NotebookingFileKeyStr!="":
			
			#debug
			'''
			self.debug(
				[
					('self.',self,[
						'ScriptbookedSortDict',
						'ScriptbookedFileKeyStrsList'
					])
				]
			)
			'''

			#map
			self.NotebookedTextStrsList=map(
					lambda __ScriptbookedFileKeyStr:
					self.file(
								_KeyStr=__ScriptbookedFileKeyStr,
								_ModeStr='r'
								
					).FiledReadVariable,
					sorted(
						self.ScriptbookedFileKeyStrsList
					)
				)

			#map
			self.NotebookedScriptStrsList=map(
				lambda __ScriptbookedFileKeyStr:
				SYS.flip(
					dict(
							Guider.GuideFormatTuplesList
						)
				)[
					'.'+__ScriptbookedFileKeyStr.split('.')[-1]
				],
				sorted(
					self.ScriptbookedFileKeyStrsList
				)
			)

			#debug
			'''
			self.debug(
				[
					('self.',self,[
						'NotebookedTextStrsList',
						'NotebookedScriptStrsList'
					])
				]
			)
			'''

			#file first
			self.file(
						self.NotebookingFileKeyStr,
						_ModeStr='w',
						_FormatStr='json'
					)

			#Copy
			self.NotebookedCodeDict=copy.copy(Celler.CellInitDict)

			#Fill the cells
			self.NotebookedCodeDict['worksheets']=[
				{
					'cells':map(
						lambda __NotebookedTextStr,__NotebookedScriptStr,__IndexInt:
							dict(
								self.cell(
									__NotebookedTextStr,
									__NotebookedScriptStr
								).CelledNoteDict,
								**{
									'prompt_number':__IndexInt,
								}
							),
							self.NotebookedTextStrsList,
							self.NotebookedScriptStrsList,
							xrange(len(self.NotebookedTextStrsList))
						)
				}
			]

			#map
			self.NotebookedPageStrsList=map(
					lambda __FileKeyStr:
					Guider.GuidingSortStr.join(
						__FileKeyStr.split('.')[0].split(
							Guider.GuidingSortStr
						)[1:]
					),
					sorted(self.ScriptbookedSortDict.values())
				)

			#debug
			'''
			self.debug(
				[
					'We have determined all the pages',
					('self.',self,[
						'NotebookedPageStrsList'
					])
				]
			)
			'''
			
			#map
			self.NotebookedSubslideStrsList=map(
					lambda __NotebookedPageStr,__PageIndexInt:
					'slide'
					if  __PageIndexInt==0
					else
					'subslide' 
					if self.NotebookedPageStrsList[__PageIndexInt-1]!=__NotebookedPageStr
					else '-',
					self.NotebookedPageStrsList,
					xrange(len(self.NotebookedPageStrsList))
				)

			#debug
			'''
			self.debug(
				[
					('self.',self,['NotebookedSubslideStrsList']),
					"self.NotebookedCodeDict['worksheets'][0]['cells'] is "+SYS._str(
						self.NotebookedCodeDict['worksheets'][0]['cells'])
				]
			)
			'''

			#Specify the page/slide
			map(
				lambda __CellDict,__NotebookedSubslideStr:
				__CellDict['metadata']['slideshow'].__setitem__(
						"slide_type",
						__NotebookedSubslideStr
					)
				,
				self.NotebookedCodeDict['worksheets'][0]['cells'],
				self.NotebookedSubslideStrsList
			)

			#debug
			'''
			self.debug(
				[
					"self.NotebookedCodeDict['worksheets'][0]['cells'] is "+SYS._str(
						self.NotebookedCodeDict['worksheets'][0]['cells'])
				]
			)
			'''

			#debug
			'''
			self.debug(
						('self.',self,[
											'NotebookingWriteBool',
											'NotebookedCodeDict',
										])
					)
			'''

			#Check
			if self.NotebookingWriteBool:

				#debug
				'''
				self.debug(
						[
							'We are going to write the notebook',
							('self.',self,[
												'FolderingPathVariable',
												'FilingKeyStr',
												'NotebookedCodeDict'
											])
						]
					)
				'''

				#Write
				self.file(
					_WriteVariable=self.NotebookedCodeDict,
					_ModeStr='w',
				)

				#Close
				self.FiledHardVariable.close(
					)
	
#</DefineClass>


#</DefinePrint>
NotebookerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'NotebookingFileKeyStr',
		'NotebookingWriteBool',
		'NotebookedTextStrsList',
		'NotebookedCodeDict',
		'NotebookedPageStrsList',
		'NotebookedSubslideStrsList'
	]
)
#<DefinePrint>
