# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Getter helps for getting attributes safely in 
an instance. Through the __getitem__ method, It looks first in the \_\_dict\_\_ to 
check if there is the corresponding GettingKeyStr.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
import types
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Itemizer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Itemizer=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
def getMapList(_LiargVariablesList):
	return SYS.listify(_LiargVariablesList)
def getLiargVariablesList(_ValueVariable):
	return [_ValueVariable]
class GetClass(object):

	def __init__(self,_Function):

		#Call the base method
		object.__init__(self)

		#init
		self.Function=_Function
		self.SelfVariable=None

	def __call__(self):

		#Debug
		'''
		print('__call__ GetClass')
		print(
				'_LiargVariablesList is '+str(_LiargVariablesList)
			)
		print('')
		'''

		#return
		return self.Function(
			self.SelfVariable
		)

SYS.GetClass=GetClass
GetUndirectStr="#get"
GetDeletePrefixStr="#delete:"
GetDirectPrefixStr="#direct:"
GetUndirectPrefixStr=GetUndirectStr+":"
GetCallPrefixStr="#call:"
GetIdPrefixStr="#id:"
GetModifyGrabStr="#modify"
GetGrabStr="#key"
GetUndirectGrabPrefixStr=GetGrabStr+':'
GetUndirectGrabStr=GetUndirectGrabPrefixStr+GetUndirectStr
GetMapStr=Itemizer.ItemMapPrefixStr+'get'
GetMapUndirectGrabStr=GetUndirectGrabPrefixStr+GetMapStr
GetSetGrabStr='#set'
GetMapSetGrabStr=Itemizer.ItemMapPrefixStr+'set'
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class GetterClass(BaseClass):
	
	def default_init(self,
						_GetSortInt=-1,
						_GettingKeyVariable=None,
						_GettingItemBool=True,
						_GettingNewBool=True,
						_GettedValueVariable=None,
						**_KwargVariablesDict
					):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def getMapValueVariable(self):

		#return
		return self.GettedValueVariable

	def __getitem__(self,_KeyVariable):
		""" """

		#Debug
		'''
		print('l.53 __getitem__ Getter')
		print('self.get is ',self.get.im_func)
		print('_KeyVariables is ',_KeyVariable)
		print('')
		'''

		#get
		self.get(_KeyVariable)
		
		#Debug
		'''
		self.debug(('self.',self,['GettedValueVariable']))
		'''
		
		#return
		return self.GettedValueVariable
	
	#def __delitem__(self,_KeyVariable):


	def do_get(self):
		""" """

		#debug
		'''
		self.debug(
			[
				("self.",self,[
						'GettingKeyVariable',
						'NameStr',
						'GettingItemBool'
					]
				)
			]
		)
		'''
		
		#itemize first
		if self.GettingItemBool:

			#debug
			'''
			self.debug('first we itemize')
			'''

			#Check
			if self.GettingKeyVariable==GetMapStr:

				#set
				self.ItemizingMapGetVariable='GettedValueVariable'

			#itemize
			self.itemize(
					self.GettingKeyVariable
				)

			#Check
			#if self.GettingKeyVariable==GetMapStr:
			#
			#	#set
			#	self.GettingItemBool=False

		else:

			#set
			self.ItemizedValueMethod=None

			#set
			#self.GettingItemBool=True

		#/############################
		# Case of a method get 
		#

		#debug
		'''
		self.debug(
				('self.',self,['ItemizedValueMethod'])
			)
		'''

		#Check 
		if self.ItemizedValueMethod!=None:

			#debug
			'''
			self.debug(
				[
					'This is a method get',
					('self.',self,[
						'ItemizedValueMethod',
						'ItemizingMapGetVariable'
						]
					)
				]
			)
			'''

			#alias
			self.GettedValueVariable=self.ItemizedValueMethod

			#Stop the getting
			return {"HookingIsBool":False}
		

		#/############################
		# Case of a GetClass get
		#

		#Check
		if type(self.GettingKeyVariable)==GetClass:

			#Check
			if self.GettingKeyVariable.SelfVariable==None:
				self.GettingKeyVariable.SelfVariable=self

			#call
			self.GettedValueVariable=self.GettingKeyVariable()

			#Stop the getting
			return {"HookingIsBool":False}


		#/############################
		# Cases of a key str get 
		#

		#Check
		if type(self.GettingKeyVariable) in [str,unicode]:

			#debug
			'''
			self.debug(
					[	
						'This is a non method get',
						('self.',self,[
							'GettingKeyVariable',
							'GettingNewBool'
						])
					]
			)
			'''

			'''
			#/############################
			# Case of a delete in the instance __dict__ 
			#

			if self.GettingKeyVariable.startswith(GetDeletePrefixStr)

				#delete
				del self.__dict__[
					SYS.deprefix(
						self.GettingKeyVariable,
						GetDeletePrefixStr
					)
				]

				#Stop the getting
				return {"HookingIsBool":False}
			'''

			#/############################
			# Case of a direct str get 
			#

			if self.GettingKeyVariable.startswith(GetDirectPrefixStr):

				#debug
				'''
				self.debug('This is a direct get of a str variable')
				'''

				#set
				self.GettedValueVariable=SYS.deprefix(
					self.GettingKeyVariable,
					GetDirectPrefixStr
				)

				#Stop the getting
				return {"HookingIsBool":False}

			#/############################
			# Case of a call str get 
			#

			if self.GettingKeyVariable.startswith(GetCallPrefixStr):

				#get
				GettedMethod=self[
					SYS.deprefix(
						self.GettingKeyVariable,
						GetCallPrefixStr
					)
				]

				#debug
				'''
				self.debug(
					[
						'This is a call get of a str variable',
						'GettedMethod is '+SYS._str(GettedMethod)
					]
				)
				'''
				
				if type(GettedMethod)==types.MethodType:

					#set
					self.GettedValueVariable=GettedMethod()

				else:

					#set
					self.GettedValueVariable=GettedMethod(self)

				#Stop the getting
				return {"HookingIsBool":False}


			#/############################
			# Case of a #id: get of an instance thanks to its id 
			#

			elif self.GettingKeyVariable.startswith(GetIdPrefixStr):

				#deprefix
				GettedKeyStr=SYS.deprefix(
						self.GettingKeyVariable,
						GetIdPrefixStr
					)

				#debug
				'''
				self.debug(
					[
						'This is a id get ',
						'GettedKeyStr is '+GettedKeyStr
					]
				)
				'''

				#IdDict
				self.GettedValueVariable=SYS.IdDict[
					int(GettedKeyStr)
				]

				#Stop the getting
				return {"HookingIsBool":False}


			#/############################
			# Case of a #get: str get 
			#

			elif self.GettingKeyVariable.startswith(GetUndirectPrefixStr):

				#deprefix
				GettedKeyStr=SYS.deprefix(
						self.GettingKeyVariable,
						GetUndirectPrefixStr
					)

				#debug
				'''
				self.debug(
					[
						'This is a undirect of a str variable',
						'GettedKeyStr is '+GettedKeyStr
					]
				)
				'''

				#Check
				if GetUndirectPrefixStr in GettedKeyStr:

					#split
					GettedKeyStrsList=GettedKeyStr.split(GetUndirectPrefixStr)

					#define
					GettedRecursiveKeyStr=''.join(GettedKeyStrsList[:-1])+self[GettedKeyStrsList[-1]]

					#debug
					'''
					self.debug(
							[
								'This is a recursive undirect get',
								'GettedRecursiveKeyStr is '+GettedRecursiveKeyStr
							]
						)
					'''

					#set
					self.GettedValueVariable=self[
						GetUndirectPrefixStr+GettedRecursiveKeyStr
					]

				else:

					#debug
					'''
					self.debug(
							'This is one level undirect get'
						)
					'''

					#set
					self.GettedValueVariable=self[
						self[GettedKeyStr]
					]

				#Stop the getting
				return {"HookingIsBool":False}

			#/############################
			# Case of a get in the instance __dict__ 
			#

			#Get safely the Value
			elif self.GettingKeyVariable in self.__dict__:

				#debug
				'''
				self.debug(
					[
						'self.GettingKeyVariable exists in the __dict__',
						self.GettingKeyVariable
					]
				)
				'''
				
				#__getitem__ in the __dict__
				self.GettedValueVariable=self.__dict__[
					self.GettingKeyVariable
				]

				#Check
				if type(self.GettedValueVariable)==GetClass:

					#debug
					'''
					self.debug(
						[
							'Actually the getted value is a GetClass'
						]
					)
					'''
					
					#set
					self.GettedValueVariable.SelfVariable=self

					#call
					self.GettedValueVariable=self.GettedValueVariable()


				#debug
				'''
				self.debug(
							[
								'This is a Spe in Instance',
								('self.',self,['GettedValueVariable'])
							]
						)
				'''

				#Stop the getting
				return {"HookingIsBool":False}
			
			#/############################
			# Case of the __class__ get
			#

			#Check
			elif self.GettingKeyVariable=='__class__':

				#set
				self.GettedValueVariable=self.__class__

				#Stop the getting
				return {"HookingIsBool":False}

			#/############################
			# Case of a get in the instance __dict__ 
			#

			#Check
			elif self.GettingKeyVariable in self.__class__.__dict__:

				#debug
				'''
				self.debug(
						[
							'this is in a class __dict__',
							('self.',self,['GettingKeyVariable'])
						]
					)
				'''
				
				#get
				GettedClassValueVariable=self.__class__.__dict__[
					self.GettingKeyVariable
				]

				#/############################
				# Case of a get of a property
				#

				if type(GettedClassValueVariable)==property:

					#get by the reactive getattr
					self.GettedValueVariable=getattr(self,self.GettingKeyVariable)

				else:

					#__getitem__ in the __class__
					self.GettedValueVariable=GettedClassValueVariable

				#debug
				'''
				self.debug(
							[
								'This is in the __class__',
								('self.',self,['GettedValueVariable'])
							]
						)
				'''

				#Stop the getting
				return {"HookingIsBool":False}

			elif self.GettingNewBool:

				#debug
				'''
				self.debug(
						[
							'we are going to set a default value here',
							('self.',self,['GettingKeyVariable'])
						]
					)
				'''

				#get
				GettedValueType=SYS.getTypeClassWithTypeStr(
					SYS.getTypeStrWithKeyStr(
						self.GettingKeyVariable)
				)

				#debug
				'''
				self.debug(
					[
						'GettedValueType is '+str(GettedValueType),
						('self.',self,['GettingKeyVariable'])
					]
				)
				'''
				
				#Check
				if callable(GettedValueType):

					#debug
					self.debug(
						[
							'We call here',
							'GettedValueType is '+str(GettedValueType),
							('self.',self,['GettingKeyVariable'])
						]
					)
					
					#alias
					self.GettedValueVariable=GettedValueType()

					#set a default value
					self.__setattr__(
						self.GettingKeyVariable,
						self.GettedValueVariable
					)
					
					#add in the SettingValue
					try:
						self.GettedValueVariable.SetTagStr=self.GettingKeyVariable
						self.GettedValueVariable.SetDeriveSetter=self
					except:
						pass

				#Stop the getting
				return {"HookingIsBool":False}


		#/############################
		# Cases of a dict GetVariable get 
		#

		elif hasattr(self.GettingKeyVariable,'items'
			) and type(self.GettingKeyVariable)!=type:

			#debug
			'''
			self.debug(
				[
					'we get or set with an itemizable instance',
					('self.',self,['GettingKeyVariable'])
				]
			)
			'''
			
			#Init
			GettedReturnBool=False

			#Temp
			GettedTempGettingKeyVariable=self.GettingKeyVariable

			#Check
			if GetGrabStr in GettedTempGettingKeyVariable:

				#debug
				'''
				self.debug(
					[
						'we get with the GetGrabStr'
					]	
				)
				'''
				
				#get
				self.GettedValueVariable=self[
					GettedTempGettingKeyVariable[GetGrabStr]
				]

				#set
				GettedReturnBool=True	

			elif GetUndirectGrabStr in GettedTempGettingKeyVariable:

				#get
				GettedKeyStr=GettedTempGettingKeyVariable[GetUndirectGrabStr]

				#debug
				'''
				self.debug(
					[
						'we get with the GetUndirectGrabStr',
						('self.',self,['GettingKeyVariable']),
						'GettedKeyStr is '+GettedKeyStr
					]	
				)
				'''

				#get get
				self.GettedValueVariable=self[
					self[
							GettedKeyStr
						]
				]

				#set
				GettedReturnBool=True	


			#Check
			elif GetMapUndirectGrabStr in GettedTempGettingKeyVariable:

				#get
				GettedLiargVariablesList=GettedTempGettingKeyVariable[
					GetMapUndirectGrabStr
				]

				#debug
				'''
				self.debug(
					[
						'we get with the GetMapUndirectGrabStr',
						('self.',self,['GettingKeyVariable']),
						'GettedLiargVariablesList is '+SYS._str(GettedLiargVariablesList)
					]	
				)
				'''
				
				#get
				self.GettedValueVariable=self[
					SYS.deprefix(
						GetMapUndirectGrabStr,
						GetUndirectGrabPrefixStr
					)
				](
					*GettedLiargVariablesList
				).ItemizedMapValueVariablesList

				#set
				GettedReturnBool=True				

			#/##################/#
			# Case of a modification 
			#

			#Check
			if GetModifyGrabStr in GettedTempGettingKeyVariable:

				#debug
				'''
				self.debug(
						'We modify here '
					)
				'''

				#call 
				#self.GettedValueVariable=GettedTempGettingKeyVariable[
				#		GetModifyGrabStr
				#]()
				self.GettedValueVariable=self[
					GettedTempGettingKeyVariable[GetModifyGrabStr]
				]

			if GetSetGrabStr in GettedTempGettingKeyVariable:

				#debug
				'''
				self.debug(
						'We set here in the GettedValueVariable'
					)
				'''

				#get
				SetVariable=GettedTempGettingKeyVariable[GetSetGrabStr]

				#set
				self.GettedValueVariable[
					SetVariable[0]
				]=SetVariable[1]

			elif GetMapSetGrabStr in GettedTempGettingKeyVariable:

				#debug
				'''
				self.debug(
						'We map a set here in the GettedValueVariable'
					)
				'''

				#get
				SetVariable=GettedTempGettingKeyVariable[GetMapSetGrabStr]

				#Check
				if hasattr(SetVariable,'items'):
					SetVariablesList=SetVariable.items()
				else:
					SetVariablesList=SetVariable

				#set
				map(
						lambda __SetVariable:
						self.GettedValueVariable.__setitem__(
								__SetVariable[0],
								__SetVariable[1]
							),
						SetVariablesList
					)

			#Check
			if GettedReturnBool:

				#Stop the getting
				return {"HookingIsBool":False}

		#/############################
		# Cases of a direct get 
		#

		#elif hasattr(self.GettingKeyVariable,'MroClassesList'):
		if type(self.GettingKeyVariable)!=str:

			#debug
			'''
			self.debug('This is a direct get of a non str variable')
			'''

			#set
			self.GettedValueVariable=self.GettingKeyVariable

			#Stop the getting
			return {"HookingIsBool":False}

		#set
		self.GettedValueVariable=None

		#debug
		'''
		self.debug(
					[
						'Not found here so set it to None',
						('self.',self,['GettedValueVariable'])
					]
				)
		'''
		#Return an output dict
		return {"HookingIsBool":True}

	def mapGet(self,_MapVariable):

		#map
		return map(
			lambda __ElementVariable:
			self.get(
				__ElementVariable
			).GettedValueVariable,
			_MapVariable.items() if hasattr(_MapVariable,'items')
			else _MapVariable
		)

	def getAttr(self,_KeyVariable):
		return getattr(self,_KeyVariable)

	def mapGetAttr(self,_MapVariable):
		return map(
			lambda __ElementVariable:
			self.getAttr(
				__ElementVariable
			).GettedValueVariable,
			_MapVariable.items() if hasattr(_MapVariable,'items')
			else _MapVariable
		)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#Check
			if self.GetSortInt>-1:
				
				#forcePrint
				self.forcePrint(
					['GetSortInt'],
					'GetterClass'
				)


		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)


#</DefineClass>

#</DefinePrint>
GetterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'GetSortInt',
		'GettingKeyVariable',
		'GettingItemBool',
		'GettingNewBool',
		'GettedValueVariable'
	]
)
#<DefinePrint>
