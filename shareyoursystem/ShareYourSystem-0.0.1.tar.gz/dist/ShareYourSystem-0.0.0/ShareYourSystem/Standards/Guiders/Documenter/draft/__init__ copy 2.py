# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Documenter

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Guiders.Nbconverter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import os
import copy
import sys
from ShareYourSystem.Standards.Classors import Doer
from ShareYourSystem.Standards.Guiders import Celler
#</ImportSpecificModules>

#<DefineLocals>
DocumentOntologyLocalFolderPathStr=SYS.ShareYourSystemLocalFolderPathStr+'Ouvaton/'
DocumentNbviewerLocalFolderPathStr=SYS.ShareYourSystemLocalFolderPathStr+'Ouvaton/'
DocumentDocumentLocalFolderPathStr=SYS.ShareYourSystemLocalFolderPathStr+'docs/LibraryReference/'
DocumentOntologyOuvatonFolderPathStr='/httpdocs/slides/'
DocumentNbviewerOuvatonFolderPathStr='/httpdocs/ipython/'
DocumentModuleStrsList=SYS.lib()
DocumentModulePathStrsList=map(
	lambda __DocumentModuleStr:
	__DocumentModuleStr.replace('.','/'),
	DocumentModuleStrsList
)
DocumentNameStrsList=map(
	lambda __DocumentModulePathStr:
	__DocumentModulePathStr.split('/')[-1],
	DocumentModulePathStrsList
)
#</DefineLocals>

#<DefineFunctions>
def getDocumentedReadmeInstanceVariableWithFolderPathStr(
		_InstanceVariable,_FolderPathStr
	):

	#file first
	return _InstanceVariable.notebook(
			**{
				'FolderingPathVariable':_FolderPathStr,
				'GuidingBookStr':"Doc",
				'NotebookingFileKeyStr':"Presentation.ipynb"
			}
	).nbconvert("Readme.md")
#</DefineFunctions>


#<DefineClass>
@DecorationClass()
class DocumenterClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
							
							]

	def default_init(self,
						_DocumentingConceptFolderPathStr="",
						_DocumentingSubReadmeIsBool=True,
						_DocumentingConceptReadmeIsBool=True,
						_DocumentingConceptDocumentIsBool=True,
						_DocumentingConceptSlideIsBool=True,
						_DocumentingSiteDocumentIsBool=True,
						_DocumentedConceptModule=None,
						_DocumentedConceptModuleStr="",
						_DocumentedConceptModuleFolderPathStr="",
						_DocumentedSubNameStrsList=None,
						_DocumentedSubModulesList=None,
						_DocumentedSubModuleStrsList=None,
						_DocumentedSubModuleLocalFolderPathStrsList=None,
						_DocumentedPresentationsDictsList=None,
						_DocumentedConceptNotebookDict=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_document(self):
		
		#debug
		'''
		self.debug(
				[
					('self.',self,[
						'DocumentingSubReadmeIsBool',
						'DocumentingConceptDocumentIsBool'
					])
				]
			)
		'''

		#Check
		if self.DocumentingConceptFolderPathStr=="":
			self.DocumentingConceptFolderPathStr='ShareYourSystem'.join(
				os.getcwd().split('ShareYourSystem')[:-1]
			)+'ShareYourSystem/'

		#debug
		'''
		self.debug(('self.',self,['DocumentingConceptFolderPathStr']))
		'''

		#debug
		self.folder(
			self.DocumentingConceptFolderPathStr
		)
		self.DocumentedConceptModuleStr=self.FolderedModuleStr

		#debug
		'''
		self.debug(('self.',self,[
									'FolderedModuleStr',
									'FolderedDirKeyStrsList'
								]))
		'''

		#filter
		self.DocumentedSubNameStrsList=SYS._filter(
			lambda __FolderedDirKeyStr:
			os.path.isdir(
				self.FolderingPathVariable+__FolderedDirKeyStr
			) and __FolderedDirKeyStr in Doer.DoerStrToDoStrOrderedDict.keys(),
			self.FolderedDirKeyStrsList
		)	

		#debug
		'''
		self.debug(('self.',self,['DocumentedSubNameStrsList','DocumentNameStrsList']))
		'''
		
		#sort
		self.DocumentedSubNameStrsList=SYS._filter(
				lambda __DocumentNameStr:
				__DocumentNameStr in self.DocumentedSubNameStrsList,
				DocumentNameStrsList
			)
		#map
		self.DocumentedSubModuleStrsList=map(
			lambda __DocumentedSubNameStr:
			self.DocumentedConceptModuleStr+'.'+__DocumentedSubNameStr,
			self.DocumentedSubNameStrsList
		)	

		#Check
		self.DocumentedConceptNameStr=self.FolderingPathVariable.split(
					'/'
			)[-1] if self.FolderingPathVariable[-1]!='/' else self.FolderingPathVariable.split('/'
			)[-2]

		#debug
		'''
		self.debug(('self.',self,[
									'DocumentedSubNameStrsList',
									'DocumentedSubModuleStrsList',
									'DocumentedConceptNameStr'
								]))
		'''

		#check
		if self.DocumentedConceptNameStr in SYS.PluralStrToSingularStrOrderedDict.keys():
			
			#debug
			self.debug(
				[
					'We get the concept module',
					('self.',self,[
							'DocumentedConceptNameStr'
						])
				]
			)

			#folder
			self.DocumentedConceptModule=self.folder(
					getattr(SYS,self.DocumentedConceptNameStr)
				).FolderedModuleDict['ModuleVariable']

		#join
		self.DocumentedConceptModuleFolderPathStr='/'.join(
			self.DocumentedConceptModule.__file__.split(
			'/'
			)[:-1]
		)+'/'

		#debug
		'''
		self.debug(('self.',self,['DocumentedConceptModule']))
		'''

		#filter
		self.DocumentedSubModulesList=SYS._filter(
				lambda __AttributeValueVariable:
				type(__AttributeValueVariable).__name__=='module',
				self.DocumentedConceptModule.__dict__.values()
			)

		#debug
		'''
		self.debug((
					'self.',self,[
							'DocumentedSubModulesList'
						]
					))
		'''

		#Check
		if self.DocumentingSubReadmeIsBool:

			#debug
			'''
			self.debug(
						[
							'we build sub modules readmes here',
							('self.',self,['DocumentedSubModuleStrsList'])
						]
					)
			'''

			#map
			map(
					lambda __DocumentedSubModuleStr:
					self.folder(
							__DocumentedSubModuleStr
						).scriptbook(
						_GuideTuplesList=[
								('001','Document','Markdown'),
							],
							**{
								'GuidingBookStr':"Doc",
							}
						).notebook(
							"PreReadme.ipynb"
						).nbconvert(
							"Readme.md"
						),
					self.DocumentedSubModuleStrsList
				)
			
		#Check
		if self.DocumentingConceptSlideIsBool:
			
			#debug
			'''
			self.debug(
						[
							'we slide here',
							('self.',self,['DocumentedSubModuleStrsList'])
						]
						)
			'''

			#map
			map(
					lambda __DocumentedSubModuleStr:
					self.folder(
							__DocumentedSubModuleStr
						).scriptbook(
						_GuideTuplesList=[
								('001','Document','Markdown'),
								('002','Github','Markdown'),
							],
							**{
								'GuidingBookStr':"Doc",
							}
						).notebook(
							"Presentation.ipynb",
							**{'WritingLoadBool':False}
						).nbconvert(
							"Presentation.html",
							'Slide'
						),
					self.DocumentedSubModuleStrsList
				)
			
			#mv for Nbviewer ipython notebooks
			map(
					lambda __DocumentedSubModuleStr:
					os.popen(
						'cp '+sys.modules[
							__DocumentedSubModuleStr
						].LocalFolderPathStr+'Presentation.ipynb '+DocumentNbviewerLocalFolderPathStr+__DocumentedSubModuleStr.split(
								'.'
							)[-1]+'.ipynb'
					),
					self.DocumentedSubModuleStrsList
				)

			#mv for Ouvaton slide in html
			map(
					lambda __DocumentedSubModuleStr:
					os.popen(
						'cp '+sys.modules[
							__DocumentedSubModuleStr
						].LocalFolderPathStr+'Presentation.html '+DocumentOntologyLocalFolderPathStr+__DocumentedSubModuleStr.split(
								'.'
							)[-1]+'.html'
					),
					self.DocumentedSubModuleStrsList
				)

			#mv for Ouvaton slide in php
			map(
					lambda __DocumentedSubModuleStr:
					os.popen(
						'cp '+sys.modules[
							__DocumentedSubModuleStr
						].LocalFolderPathStr+'Presentation.html '+DocumentOntologyLocalFolderPathStr+__DocumentedSubModuleStr.split(
								'.'
							)[-1]+'.php'
					),
					self.DocumentedSubModuleStrsList
				)

			#map
			self.DocumentedSubModuleLocalFolderPathStrsList=map(
					lambda __DocumentedSubModuleStr:
					SYS.PythonlogyLocalFolderPathStr+__DocumentedSubModuleStr.replace(
						'.','/'
					),
					self.DocumentedSubModuleStrsList
				)

			#map
			self.DocumentedPresentationsDictsList=map(
					lambda __DocumentedSubModuleFolderPathStr:
					self.folder(
							__DocumentedSubModuleFolderPathStr
						).file(
							'Presentation.ipynb',
							_ModeStr='r',
							_FormatStr='json'
						).file(
							_ModeStr='c'
						).FiledReadVariable,
					self.DocumentedSubModuleLocalFolderPathStrsList
				)					

			#debug
			'''
			self.debug(
						'self.DocumentedPresentationsDictsList is '+SYS._str(self.DocumentedPresentationsDictsList)
					)
			'''

			#copy
			self.DocumentedConceptNotebookDict=copy.copy(Celler.CellInitDict)

			#flat
			DocumentedFlatPresentationsDictsList=SYS.flat(
					map(
							lambda __DocumentedPresentationsDict:
							copy.deepcopy(
								__DocumentedPresentationsDict['worksheets'][0]['cells']
								),
							self.DocumentedPresentationsDictsList
						)
					)

			#Flat all the presentations
			self.DocumentedConceptNotebookDict['worksheets']=[
				{
					'cells':map(
						lambda __DocumentedFlatPresentationsDict,__IndexInt:
						dict(__DocumentedFlatPresentationsDict,**{
							'prompt_number':__IndexInt}),
						DocumentedFlatPresentationsDictsList,
						xrange(len(DocumentedFlatPresentationsDictsList))
					)
				}
			]

			#debug
			'''
			self.debug(('self.',self,['DocumentedConceptNotebookDict']))
			'''

			#Write
			self.folder(
					self.DocumentingConceptFolderPathStr
				).file(
					_KeyStr='Concept'+self.GuidingBookStr+'.ipynb',
					_WriteVariable=self.DocumentedConceptNotebookDict,
					_FormatStr="json"
				).file(
					_ModeStr='c'
				)

			#nbconvert
			self.NotebookedCodeDict=self.DocumentedConceptNotebookDict
			self.folder(
					self.DocumentingConceptFolderPathStr
				).nbconvert(
					_FormatStr='Slide',
					_FileKeyStr='Concept'+self.GuidingBookStr+'.ipynb'
				)

			#set
			self.DocumentedSlideLocalFilePathStr=DocumentOntologyLocalFolderPathStr+self.DocumentedConceptModule.__name__.split('.')[-1]+'.html'

			#cp
			os.popen('cp '+self.FiledPathStr+' '+self.DocumentedSlideLocalFilePathStr+self.DocumentedConceptModule.__name__.split('.')[-1]+'.ipynb')

			#mv with .html extension
			os.popen(
					'cp '+self.FiledPathStr.replace(
					'.ipynb',
					'.html'
					)+' '+self.DocumentedSlideLocalFilePathStr
				)

			#mv with .php extension
			os.popen(
					'mv '+self.FiledPathStr.replace(
					'.ipynb',
					'.html'
					)+' '+self.DocumentedSlideLocalFilePathStr.replace('.html','.php')
				)

			#deploy
			try:
				self.deploy(
					_ClientFilePathStrToServerFilePathStrOrderedDict=collections.OrderedDict(
						[
							(
								self.DocumentedSlideLocalFilePathStr,
								DocumentOntologyOuvatonFolderPathStr+self.DocumentedConceptModule.__name__.split('.'
									)[-1]+'.php'
							)
						]
					)
				)
			except:
				print('There is NO Internet !')
				
		#Check
		if self.DocumentingConceptReadmeIsBool:

			#debug
			'''
			self.debug('we build the concept readme here')
			'''

			#import submodules
			'''
			map(
					lambda __DocumentedSubModuleStr:
					importlib.import_modules(__DocumentedSubModuleStr),
					self.DocumentedSubModuleStrsList
				)
			'''

			#readme
			self.folder(
					self.DocumentedConceptModuleStr
				).scriptbook(
					_GuideTuplesList=[
						('001','Document','Markdown'),
						('002','Ouvaton','Markdown'),
						('1','Github','Markdown'),
					],
					**{'GuidingBookStr':"Doc"}
				)

			#notebook
			self.scriptbook(
					_GuideTuplesList=[]
				).notebook(
					"PreReadme.ipynb"
				).nbconvert(
					"Readme.md",
					'Markdown',
			)

		#Check
		if self.DocumentingConceptDocumentIsBool:

			#debug
			'''
			self.debug(
						[
							'we document here',
							('self.',self,['DocumentedConceptModuleFolderPathStr'])
						]
					)
			'''

			'''
			#document
			self.document(
				**{'PackagingModuleVariable':self.DocumentedConceptModuleStr}
			)	
			'''

			#folder
			self.folder(self.DocumentedConceptModuleStr)

			#mv with .php extension
			os.popen(
					'cp '+self.PackagedLocalFolderPathStr+'Readme.md  '+DocumentDocumentLocalFolderPathStr+self.DocumentedConceptModuleStr.split('.')[-1]+'.md'
				)

		if self.DocumentingSiteDocumentIsBool:

			#open
			os.popen(
						'mkdocs build --clean'
				)

			#deploy
			try:
				self.deploy(
					_ClientFilePathStrToServerFilePathStrOrderedDict=collections.OrderedDict(
						[
							(
								self.DocumentedSlideLocalFilePathStr,
								DocumentOntologyOuvatonFolderPathStr+self.DocumentedConceptModule.__name__.split('.'
									)[-1]+'.php'
							)
						]
					)
				)
			except:
				print('There is NO Internet !')

#</DefineClass>

#</DefinePrint>
DocumenterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'DocumentingConceptFolderPathStr',
		'DocumentingSubReadmeIsBool',
		'DocumentingConceptReadmeIsBool',
		'DocumentingConceptDocumentIsBool',
		'DocumentingConceptSlideIsBool',
		'DocumentingSiteDocumentIsBool',
		'DocumentedConceptModule',
		'DocumentedConceptModuleStr',
		'DocumentedConceptModuleFolderPathStr',
		'DocumentedSubNameStrsList',
		'DocumentedSubModulesList',
		'DocumentedSubModuleStrsList',
		'DocumentedSubModuleLocalFolderPathStrsList',
		#'DocumentedPresentationsDictsList',
		#'DocumentedConceptNotebookDict'
	]
)
#<DefinePrint>