# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Noder defines Child ordered dicts with <DoStr> as KeyStr. 
The items inside are automatically setted with Noded<DoStr><TypeStr> and have 
a Pointer to the parent InstanceVariable. This is the beginning for buiding high
arborescent and (possibly circular) structures of objects.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Applyiers.Weaver"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
from ShareYourSystem.Standards.Itemizers import Pather
from ShareYourSystem.Functers import Imitater
#</ImportSpecificModules>

#<DefineLocals>
NodingPrefixGetStr='<'
NodingSuffixGetStr='>'
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class NoderClass(BaseClass):

	#Definition
	RepresentingKeyStrsList=[
									'NodingCollectionStr',
									#'NodedCollectionOrderedDict',
									'NodedPrefixStr',
									'NodedKeyStrKeyStr',
									'NodePointDeriveNoder',
									'NodedInt'
								]

	def default_init(self,
				_NodingCollectionStr="",							
				_NodedCollectionOrderedDict=None, 					
				_NodedPrefixStr="",					
				_NodedKeyStrKeyStr="" ,					
				_NodePointDeriveNoder=None,			 	
				_NodedInt=-1,							
				**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	#@Argumenter.ArgumenterClass()
	def do_node(self,**_KwargVariablesDict):

		#debug
		'''
		self.debug(("self.",self,['NodingCollectionStr']))
		'''

		#Get the NodedStr
		if self.NodingCollectionStr!="":
		
			#set the NodedPrefixStr
			self.NodedPrefixStr='Noded'+self.NodingCollectionStr

			#set the Noded OrderedDict and KeyStr
			NodedCollectionOrderedSetTagStr=self.NodedPrefixStr+'CollectionOrderedDict'
			#self.NodedKeyStrKeyStr=self.NodedPrefixStr+'KeyStr'

			try:
				self.NodedCollectionOrderedDict=getattr(self,NodedCollectionOrderedSetTagStr)
			except AttributeError:
				self.__setattr__(NodedCollectionOrderedSetTagStr,collections.OrderedDict())
				self.NodedCollectionOrderedDict=getattr(self,NodedCollectionOrderedSetTagStr)

			'''
			try:
				self.NodedKeyStr=getattr(self,self.NodedKeyStrKeyStr)
			except AttributeError:
				self.__setattr__(self.NodedKeyStrKeyStr,"")
				self.NodedKeyStr=getattr(self,self.NodedKeyStrKeyStr)
			'''

			#debug
			'''
			self.debug(('self.',self,['NodedPrefixStr','NodedCollectionOrderedDict',]))
			'''

			#If this is a set of a tree of nodes then also init the nodifying attributes	
			if 'IsNoderBool' not in _KwargVariablesDict or _KwargVariablesDict['IsNoderBool']:

				#NodePointDeriveNoderKeyStr=self.NodedPrefixStr+'ParentPointer'
				#NodedIntKeyStr=self.NodedPrefixStr+'Int'
				#NodedPathStrKeyStr=self.NodedPrefixStr+'PathStr'
				#NodedGrandParentPointersListKeyStr=self.NodedPrefixStr+'GrandParentPointersList'

				#try:
					self.NodedInt=getattr(self,NodedIntKeyStr)
				except AttributeError:
					self.__setattr__(NodedIntKeyStr,-1)
					self.NodedInt=getattr(self,NodedIntKeyStr)

				try:
					self.NodePointDeriveNoder=getattr(self,NodePointDeriveNoderKeyStr)
				except AttributeError:
					self.__setattr__(NodePointDeriveNoderKeyStr,None)
					self.NodePointDeriveNoder=getattr(self,NodePointDeriveNoderKeyStr)

				#debug
				'''
				self.debug(
							[
								('vars ',vars(),['NodePointDeriveNoderKeyStr']),
								('self.',self,[NodePointDeriveNoderKeyStr])
							]
						)
				'''

		#Return self
		#return self


	#<Hook>@Hooker.HookerClass(**{'HookingAfterVariablesList':[BaseClass.get]})
	@Imitater.ImitaterClass()
	def get(self):

		#debug
		'''
		self.debug(("self.",self,['GettingKeyVariable']))
		'''
		
		#Definition
		OutputDict={'HookingIsBool':True}

		#Appending set
		if self.GettingKeyVariable.startswith(NodingPrefixGetStr):

			#Definition the SplittedStrsList
			SplittedStrsList=self.GettingKeyVariable.split(NodingSuffixGetStr)

			#Definition the NodingCollectionStr
			NodingCollectionStr=NodingPrefixGetStr.join(
				SplittedStrsList[0].split(NodingPrefixGetStr)[1:])
			
			#debug
			'''
			self.debug(
						[
							'NodingCollectionStr is '+NodingCollectionStr,
							'We are going to node'
						]
					)
			'''

			#Nodify
			self.node(NodingCollectionStr,**{'IsNoderBool':False})

			#Definition the KeyStr
			KeyStr=NodingSuffixGetStr.join(SplittedStrsList[1:])

			#debug
			'''
			self.debug(
							[
								'node is done',
								'KeyStr is '+KeyStr
							]
				)
			'''

			#Get with a digited KeyStr case
			if KeyStr.isdigit():

				#Definition the GettingInt
				GettingInt=(int)(KeyStr)

				#Check if the size is ok
				if GettingInt<len(self.NodedCollectionOrderedDict):

					#Get the GettedVariable 
					self.GettedValueVariable=SYS.get(self.NodedCollectionOrderedDict,'values',GettingInt)

					#Return
					OutputDict['HookingIsBool']=False
					#<Hook>return OutputDict

			#Get in the ValueVariablesList
			elif KeyStr=="":

				#Get the GettedVariable
				self.GettedValueVariable=self.NodedCollectionOrderedDict.values()

				#Return 
				OutputDict['HookingIsBool']=False
				#<Hook>return OutputDict

			elif KeyStr in self.NodedCollectionOrderedDict:
				
				#Get the GettedVariable
				self.GettedValueVariable=self.NodedCollectionOrderedDict[KeyStr]

				#Return 
				OutputDict['HookingIsBool']=False
				#<Hook>return OutputDict

		#Call the parent get method
		if OutputDict['HookingIsBool']:
			BaseClass.get(self)

		#debug
		'''
		self.debug('End of the method')
		'''

	#<Hook>@Hooker.HookerClass(**{'HookingAfterVariablesList':[BaseClass.set]})
	@Imitater.ImitaterClass()
	def set(self):
		""" """

		#debug
		'''
		self.debug('Start of the method')
		'''

		#Definition
		OutputDict={'HookingIsBool':True}

		#Appending set
		if self.SettingKeyVariable.startswith(NodingPrefixGetStr):

			#Definition the SplittedStrsList
			SplittedStrsList=self.SettingKeyVariable.split(NodingSuffixGetStr)

			#Definition the NodingCollectionStr
			NodingCollectionStr=NodingPrefixGetStr.join(
				SplittedStrsList[0].split(NodingPrefixGetStr)[1:])

			#Check if it is an append of Nodes
			IsNoderBool='NoderClass' in map(
											lambda __Class:
											__Class.__name__,
											type(self.SettingValueVariable).__mro__
											)

			#debug
			'''
			self.debug(('vars ',vars(),['NodingCollectionStr','IsNoderBool']))
			'''

			#Nodify
			self.node(NodingCollectionStr,**{'IsNoderBool':IsNoderBool})

			#Definition the KeyStr
			SettedKeyStr=NodingSuffixGetStr.join(SplittedStrsList[1:])

			#debug
			'''
			self.debug('KeyStr is '+KeyStr)
			'''

			#Append (or set if it is already in)
			Pather.setWithPathVariableAndKeyVariable(
				self.NodedCollectionOrderedDict,
				Pather.PathPrefixStr+SettedKeyStr,
				self.SettingValueVariable
			)

			#If it is an object
			if IsNoderBool:

				#Int and Set Child attributes
				self.SettingValueVariable.__setattr__(self.NodedPrefixStr+'Int',len(self.NodedCollectionOrderedDict)-1)
				NodedStrKeyStr=self.NodedPrefixStr+'KeyStr'
				self.SettingValueVariable.__setitem__(NodedStrKeyStr,SettedKeyStr)
				self.SettingValueVariable.__setattr__(self.NodedPrefixStr+'ParentPointer',self)

				#Init GrandChild attributes
				'''
				self.SettingValueVariable.__setattr__(self.NodedPrefixStr+'PathStr',"")
				self.SettingValueVariable.__setattr__(self.NodedPrefixStr+'GrandParentPointersList',[])
				'''

			#Return 
			OutputDict['HookingIsBool']=False
			#<Hook>return OutputDict

		#Call the parent get method
		if OutputDict['HookingIsBool']:
			BaseClass.set(self)

#</DefineClass>

