# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Boxer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Viewers.Viewer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class BoxerClass(BaseClass):
	
	#Definition 
	RepresentingKeyStrsList=[
								'BoxingPatchStr',
								'BoxingSystemStr',
								'BoxedDerivePatcherVariable',
								'BoxedCollectionsOrderedDict',
								'BoxedPathStr'
							]

	def default_init(self, 
						_BoxingPatchStr="",
						_BoxingSystemStr="",
						_BoxedDerivePatcherVariable=None,
						_BoxedCollectionsOrderedDict=None,
						_BoxedParentPathStr="",
						_BoxedPathStr="",
						**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_box(self):
		
		#debug
		'''
		self.debug('We box here')
		'''

		#parent first
		self.parent(['MeteoredConcurrentDDPClientVariable'])

		#Check
		if self.BoxedDerivePatcherVariable==None:
			self.BoxedDerivePatcherVariable=self.NodePointDeriveNoder

		'''
		#debug
		self.debug(('self.',self,[
			#'ParentedDeriveParentersList',
			'ParentedNodePathStr'
		]))

		#Determine the deep
		self.BoxedDeepInt=len(self.ParentedNodePathStr.split('/'))
		'''

		#set
		self.BoxedParentPathStr=self.BoxedDerivePatcherVariable.ParentedNodePathStr
		self.BoxedPathStr=self.BoxedDerivePatcherVariable.ParentedNodePathStr+'/'+self.BoxedDerivePatcherVariable.NodeKeyStr


		#insert the node box
		self.MeteoredConcurrentDDPClientVariable.call(
				#'mongo',
				'box',
				#'insert',
				{
					'ParentPatchStr':self.BoxingPatchStr,
					'ParentSystemStr':self.BoxingSystemStr,
					'ParentPathStr':self.BoxedParentPathStr,
					'ParentCollectionStr':self.NodeCollectionStr,
					'IsNoderBool':True,
					'PathStr':self.BoxedPathStr,
					'NodeStr':self.BoxedDerivePatcherVariable.NodeKeyStr
				}
			)

		#set
		self.BoxedCollectionsOrderedDict=self.BoxedDerivePatcherVariable.CollectionsOrderedDict

		#debug
		'''
		self.debug(('self.',self,['BoxedCollectionsOrderedDict']))
		'''

		"""
		#insert the child collections ordered dict
		self.MeteoredConcurrentDDPClientVariable.call(
			'mongo',
			'coops',
			'insert',
			{
				'PathStr':self.BoxedPathStr,
				'CollectionStrsList':self.BoxedCollectionsOrderedDict.keys()
			}
		)
		"""	
	

#</DefineClass>