# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Guider write templated .py or .md files for explaining how
work a certain Module

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Filer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import inspect
import os
#</ImportSpecificModules>

#<DefineFunctions>
GuideFormatTuplesList=[
	('Latex','.tex'),
	('Markdown','.md'),
	('Python','.py'),
]
#</DefineFunctions>

#<DefineLocals>

GuidingDocumentMarkdownTextStr='''
<!--
FrozenIsBool False
-->

#<NameStr>

##Doc
----

<ModuleDocStr>

----

<small>
View the <NameStr> notebook on [NbViewer](http://nbviewer.ipython.org/url/shareyoursystem.ouvaton.org/<NameStr>.ipynb)
</small>

'''

GuidingGithubMarkdownTextStr='''
<!--
FrozenIsBool False
-->

##Code

----

<ClassDocStr>

<small>
View the <NameStr> sources on <a href="'''+SYS.GithubMasterUrlStr+'''/Pythonlogy/<GithubPathStr>" target="_blank">Github</a>
</small>

----

```python
<CodeStr>
```

'''

GuidingOuvatonMarkdownTextStr='''
<!--
FrozenIsBool False
-->

##Concept and SubModules family

<script type="text/javascript">

	var HrefStr=window.location.href;
	//alert(window.location.href)

	if(HrefStr == "'''+SYS.OuvatonUrlStr+'''/site/LibraryReference/<NameStr>/"){

	    //alert('Ouvaton')
	    document.write("from ")
	    document.write("'''+SYS.OuvatonUrlStr+'''/slides/ ")
	    document.write("<iframe width=\\"725\\" height=\\"300\\" src=\\"")
	    document.write("'''+SYS.OuvatonUrlStr+'''")
	    document.write("/slides/<NameStr>.php\\"></iframe>")
	}
	else if(HrefStr == "http://127.0.0.1:8000/LibraryReference/<NameStr>/"){

        //alert('Localhost')
        document.write("from ")
        document.write("localhost mkdocs but direct to ouvaton")
        document.write("<iframe width=\\"725\\" height=\\"300\\" src=\\"")
        document.write("'''+SYS.OuvatonUrlStr+'''")
        document.write("/slides/<NameStr>.php\\"></iframe>")
    }
    else
    {

        //alert('Local')
	    document.write("from ")
	    document.write("'''+SYS.OuvatonLocalFolderPathStr+''' ")
	    document.write("<iframe width=\\"725\\" height=\\"300\\" src=\\"")
	    document.write("'''+SYS.OuvatonLocalFolderPathStr+'''")
	    document.write("<NameStr>.html\\"></iframe>")

    }

</script>

<small>
View the <NameStr> concept on <a href="'''+SYS.OuvatonUrlStr+'''/slides/<NameStr>.php" target="_blank">Ouvaton</a>
</small>

'''

GuidingClassMarkdownTextStr='''
<!--
FrozenIsBool False
-->

##More Descriptions at the level of the class

Special attributes of the <NameStr>Class are :
'''

GuidingClassCodeTextStr='''
#FrozenIsBool False

#ImportModules
import ShareYourSystem as SYS
from <ParentModuleStr> import <NameStr>
		
#Definition the AttestedStr
SYS._attest(
	[
		'DefaultAttributeItemTuplesList is '+SYS._str(
			<NameStr>.<NameStr>Class.DefaultAttributeItemTuplesList,
			**{'RepresentingAlineaIsBool':False}
		)
	]
) 

#Print

'''

GuidingInstanceMarkdownTextStr='''
<!--
FrozenIsBool False
-->

##More Descriptions at the level of the instances

A default call of an instance gives :
'''

GuidingInstanceCodeTextStr='''
#FrozenIsBool False

#ImportModules
from ShareYourSystem.Standards.Classors import Attester
from <ParentModuleStr> import <NameStr>
		
#Definition the AttestedStr
SYS._attest(
	[
		<NameStr>.<NameStr>Class()
	]
) 

#Print


'''
GuidingSortStr='_'
#</DefineLocals>


#<DefineClass>
@DecorationClass()
class GuiderClass(BaseClass):
							
	def default_init(self,
						_GuidingIndexStr="",
						_GuidingPageStr="",
						_GuidingBookStr="",
						_GuidingScriptStr="",
						_GuidedIndexStr="",
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_guide(self):
		
		#Check
		if self.GuidingPageStr!="":

			if self.GuidingIndexStr=="":

				#Definition
				IndexesList=map(
						int,
						map(
								lambda __KeyStr:
								__KeyStr.split(
								GuidingSortStr
								)[0],
							self.GuidedDict.values()
							)
					)

				#Definition the last index of Guide
				IndexInt=max(IndexesList) if len(IndexesList)>0 else -1

				#Define
				self.GuidingIndexStr="%02d"%(IndexInt+1)+GuidingSortStr

		#debug
		'''
		self.debug(('self.',self,['PackagedLocalFolderPathStr']))
		'''
		
		#Write a new file
		self.file(
					self.GuidingIndexStr+GuidingSortStr+self.GuidingPageStr+self.GuidingBookStr+(
						dict(
							GuideFormatTuplesList
						)
					)[self.GuidingScriptStr],
					'wt',
					**{

						'FolderingPathVariable':self.FolderedModuleDict[
							'LocalFolderPathStr'
						]
					}
				)

		#Check
		if self.FiledHardVariable.mode=='wt':

			#Definition
			GuidingTextStrKeyStr='Guiding'+self.GuidingPageStr+self.GuidingScriptStr+'TextStr'

			#debug
			'''
			print('self.FiledHardVariable is ',self.FiledHardVariable)
			print('')
			'''

			#Definition
			GuidedTextStr=globals()[GuidingTextStrKeyStr]

			#debug
			'''
			print('GuidedTextStr is ',GuidedTextStr)
			print('')
			'''

			#Replace
			GuidedTextStr=GuidedTextStr.replace(
										'<NameStr>',
										self.FolderedNameStr
										)

			#debug
			'''
			print('GuidedTextStr is ',GuidedTextStr)
			print('')
			'''
					
			#Replace
			if self.FolderedNameStr=="ShareYourSystem":
				GuidedTextStr=GuidedTextStr.replace(
					"from <ParentModuleStr> ",""
				)
			else:
				GuidedTextStr=GuidedTextStr.replace(
						"<ParentModuleStr>",
						self.FolderedParentModuleStr
					).replace(
						"<GithubPathStr>",
						self.FolderedModuleDict['ModuleStr'].replace('.','/')
					).replace(
						"<ModuleDocStr>",
						self.FolderedModuleDict['ModuleVariable'
						].__doc__.split('</DefineSource>\n'
							)[-1].replace(
							'\n','\n> '
						)
					).replace(
						"<CodeStr>",
						inspect.getsource(
							self.FolderedModuleDict['ModuleVariable']
						)
					)

			#debug
			'''
			print('Guider l.313')
			print('GuidedTextStr is',GuidedTextStr)
			print('')
			'''

			#Write
			self.file(
				_ModeStr='w',
				_WriteVariable=GuidedTextStr,
				_FormatStr='txt'
			)

			#Close
			self.FiledHardVariable.close()
		
#</DefineClass>

#</DefinePrint>
GuiderClass.PrintingClassSkipKeyStrsList.extend(
	[
		'GuidingIndexStr',
		'GuidingPageStr',
		'GuidingBookStr',
		'GuidingScriptStr',
		'GuidedIndexStr'
	]
)
#<DefinePrint>
