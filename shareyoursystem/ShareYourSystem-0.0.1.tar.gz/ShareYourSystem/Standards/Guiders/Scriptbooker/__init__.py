# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Scriptbooker defines template of Mardown and Code Scriptbooks for readming a Module.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Guiders.Guider"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
Guider=BaseModule
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ScriptbookerClass(BaseClass):

	def default_init(self,
						_ScriptbookingGuideTuplesList=[
							('001','Document','Markdown'),
							#('003','Ouvaton','Markdown')
							('1','Github','Markdown'),
						],
						_ScriptbookedFileKeyStrsList=None,
						_ScriptbookedNewGuideTuplesList=None,
						_ScriptbookedOldGuideTuplesList=None,
						_ScriptbookedSortDict=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_scriptbook(self):

		#debug
		self.debug(
			[
				'We scriptbook here',
				('self.',self,[
					'FolderedDirKeyStrsList'
				])
			]
		)

		#Definition
		self.ScriptbookedFileKeyStrsList=SYS._filter(
				lambda __DirKeyStr:
				any(
					map(
						lambda __ExtensionStr:
						__DirKeyStr.endswith(
							self.GuidingBookStr+__ExtensionStr
						),
						['.py','.md','.tex']
				)),
				self.FolderedDirKeyStrsList
		)

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'ScriptbookedFileKeyStrsList'
					])
			]
		)
		'''
		
		#Definition
		ScriptbookedPageStrsList=map(
			lambda __ScriptbookerScriptbookFileKeyStr:
			Guider.GuidingSortStr.join(
				__ScriptbookerScriptbookFileKeyStr.split(
					Guider.GuidingSortStr)[1:]
				),
			self.ScriptbookedFileKeyStrsList
		)

		#set
		self.ScriptbookedSortDict=dict(
				zip(
						ScriptbookedPageStrsList,
						self.ScriptbookedFileKeyStrsList
					)
			)

		#debug
		'''
		self.debug(('self.',self,['ScriptbookedSortDict']))
		'''
		
		#Check
		if len(self.ScriptbookingGuideTuplesList)>0:

			#map
			ScriptbookedGuideTuplesList=map(
					lambda __ScriptbookingGuideTuple:
					list(__ScriptbookingGuideTuple)+[
						__ScriptbookingGuideTuple[1]+self.GuidingBookStr+dict(
						Guider.GuideFormatTuplesList
						)[
							__ScriptbookingGuideTuple[2]
						]
					],
					self.ScriptbookingGuideTuplesList
				)

			#groupby
			[
				self.ScriptbookedNewGuideTuplesList,
				self.ScriptbookedOldGuideTuplesList
			]=SYS.groupby(
				lambda __ScriptbookedGuideTuple:
				__ScriptbookedGuideTuple[3] not in self.ScriptbookedSortDict,
				ScriptbookedGuideTuplesList
			)

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'ScriptbookedNewGuideTuplesList'
						])
				]
			)
			'''
			
			#map a guide for the news
			map(
				lambda __ScriptbookedNewGuideTuple:
				self.guide(
					__ScriptbookedNewGuideTuple[0],
					__ScriptbookedNewGuideTuple[1],
					self.GuidingBookStr,
					__ScriptbookedNewGuideTuple[2]
				),
				self.ScriptbookedNewGuideTuplesList
			)

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'ScriptbookedOldGuideTuplesList',
							'ScriptbookedSortDict'
						])
				]
			)
			'''

			#check if we rewrite for the olds
			map(
				lambda __ScriptbookedOldGuideTuple:
				self.file(
					_ModeStr='c'
				) 
				if "#FrozenIsBool True" in self.file(
						self.ScriptbookedSortDict[
								__ScriptbookedOldGuideTuple[3]
							],
						_ModeStr='r',
						_FormatStr='txt'
					).FiledReadVariable
				else self.file(
						_ModeStr='c'
					).guide(
						__ScriptbookedOldGuideTuple[0],
						__ScriptbookedOldGuideTuple[1],
						self.GuidingBookStr,
						__ScriptbookedOldGuideTuple[2]
					),
				self.ScriptbookedOldGuideTuplesList
			)
		

	
#</DefineClass>

#</DefinePrint>
ScriptbookerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ScriptbookingGuideTuplesList',
		'ScriptbookedFileKeyStrsList',
		'ScriptbookedNewGuideTuplesList',
		'ScriptbookedOldGuideTuplesList',
		'ScriptbookedSortDict'
	]
)
#<DefinePrint>

