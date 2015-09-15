# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


An Itemizer...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Debugger"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineLocals>
ItemMapPrefixStr="#map@"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ItemizerClass(BaseClass):

	def default_init(self,
						_ItemizingKeyVariable=None,
						_ItemizingValueVariable=None,
						_ItemizingMapGetVariable=None,
						_ItemizedKeyStr="",
						_ItemizedValueMethod=None,
						_ItemizedMethodStr="",
						_ItemizedValueVariable=None,
						_ItemizedMapValueVariablesList=None,
						**_KwargVariablesDict
					):	

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_itemize(self):

		#reset
		self.setDone(SYS.ItemizerClass)

		#debug
		'''
		self.debug(
				[
					'We itemize here',
					('self.',self,['ItemizingKeyVariable'])
				]
			)
		'''

		#Check
		if type(self.ItemizingKeyVariable) in SYS.StrTypesList:

			#set
			self.ItemizedKeyStr=self.ItemizingKeyVariable

			#Check
			if self.ItemizingKeyVariable.startswith(ItemMapPrefixStr):

				#debug
				'''
				self.debug(
						'It is going to be a map'
					)
				'''

				#deprefix
				ItemizedMapMethodStr=SYS.deprefix(
						self.ItemizingKeyVariable,
						ItemMapPrefixStr
					)

				#get
				ItemizedMapMethod=getattr(
						self,
						ItemizedMapMethodStr
					)

				#set
				ItemizedMapBool=True

				#Check
				ItemizedGetMethod=getattr
				if self.ItemizingMapGetVariable==None:
					ItemizedGetMethod=SYS.getNone
				if type(self.ItemizingMapGetVariable)==list:
					ItemizedGetMethod=SYS.pick
				
				#define
				#def MapMethod(_MapList):
				def MapMethod(*_MapLiargVariablesList):

					#debug
					'''
					self.debug(
						[
							'_MapLiargVariablesList is '+SYS._str(_MapLiargVariablesList),
							#'ItemizedMapMethodStr is '+ItemizedMapMethodStr,
							#'ItemizedMapMethod is '+str(ItemizedMapMethod),
							#'ItemizedMapMethod.im_func is '+str(ItemizedMapMethod.im_func)
						]
					)
					'''

					#get
					ItemizedMapClass=ItemizedMapMethod.im_func.BaseDoClass

					#get
					ItemizedMapList=ItemizedMapClass.Module.getMapList(
						_MapLiargVariablesList
					)

					#debug
					"""
					for __ElementVariable in ItemizedMapList:

						#Debug
						print('ItemizedMapList is l 119')
						print(ItemizedMapList)
						print('__ElementVariable is ')
						print(__ElementVariable)
						print('ItemizedGetMethod is ')
						print(ItemizedGetMethod)
						print('')

						#get
						GetVariable=ItemizedGetMethod(
							ItemizedMapMethod(
									*__ElementVariable 
								),
							self.ItemizingMapGetVariable
						)

						#Debug
						print('GetVariable is ')
						print(GetVariable)
						print('')				
					"""
					
					#Debug
					'''
					self.debug(
						[
							'ItemizedMapMethod is '+SYS._str(ItemizedMapMethod),
							#'self.ItemizedMapMethod.__name__ is '+self.ItemizedMapMethod.__name__,
							#'self.__class__.InspectInspectDict[self.ItemizedMapMethod.__name__] is ',
							#SYS._str(self.__class__.InspectInspectDict[self.ItemizedMapMethod.__name__])
							#'ItemizedMapClass is '+str(ItemizedMapClass),
							'ItemizedMapList is '+SYS._str(ItemizedMapList)
						]
					)
					'''
					
					#return
					self.ItemizedMapValueVariablesList=map(
						lambda __ElementVariable:
						ItemizedMapClass.getMapValueVariable(
							ItemizedMapMethod(
									*__ElementVariable 
								)
						),
						ItemizedMapList
					)

					#return self
					return self

				#alias
				self.ItemizedValueMethod=MapMethod

				#return 
				return

		#try
		try:

			#debug
			'''
			self.debug(
				[
					'We find in the InspectMethodDict',
					'self.__class__.InspectMethodDict is ',
					SYS._str(self.__class__.InspectMethodDict)
				]
			)
			'''
			
			#get
			ItemizedValueUnboundMethod=self.__class__.InspectMethodDict[
				self.ItemizingKeyVariable
			]

			#set
			self.ItemizedMethodStr=self.ItemizingKeyVariable

			#alias
			self.ItemizedValueMethod=getattr(
				self,
				self.ItemizedMethodStr
			)

		except:

			#debug
			'''
			self.debug(
					[
						'This is not a method call directly',
					]
				)
			'''

			#alias
			self.ItemizedValueVariable=self.ItemizingValueVariable
#</DefineClass>


#</DefinePrint>
ItemizerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ItemizingKeyVariable',
		'ItemizingValueVariable',
		'ItemizingMapGetVariable',
		'ItemizedKeyStr',
		'ItemizedValueMethod',
		'ItemizedMethodStr',
		'ItemizedValueVariable',
		'ItemizedMapValueVariablesList'
	]
)
#<DefinePrint>
