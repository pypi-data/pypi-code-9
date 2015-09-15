# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Setter has a __setitem__ method for setting things in the <InstanceVariable>.__dict__

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Getter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Getter=BaseModule
from ShareYourSystem.Standards.Itemizers import Itemizer
import collections,copy
#</ImportSpecificModules>

#<DefineLocals>
def getMapList(_LiargVariablesList):

	#Debug
	'''
	print('Setter l 31')
	print('_LiargVariablesList is ')
	print(_LiargVariablesList)
	print("len(_LiargVariablesList)==1")
	print(len(_LiargVariablesList)==1)
	print('')
	'''
	
	#Check
	if len(_LiargVariablesList)==1:

		#Debug
		'''
		print('len(_LiargVariablesList)==1')
		print('type(_LiargVariablesList) is ')
		print(type(_LiargVariablesList))
		print('type(_LiargVariablesList[0]) is ')
		print(type(_LiargVariablesList[0]))
		print('')
		'''

		#Check
		if hasattr(_LiargVariablesList[0],'items'):
			return _LiargVariablesList[0].items()
		elif type(_LiargVariablesList)==tuple and type(_LiargVariablesList[0])==tuple and len(
			_LiargVariablesList[0])==2:
			return [_LiargVariablesList[0]]
		else:
			return _LiargVariablesList[0]

	else:

		#return the total
		return _LiargVariablesList
		
def getLiargVariablesList(_ValueVariable):
	return _ValueVariable
SetSetterShortStr="<"
SetEachPrefixStr="#each:"
SetAllPrefixStr="#all:"
SetBoundPrefixStr="#bound:"
SetKeyGrabStr=Getter.GetGrabStr
SetValueGrabStr="#value"
SetValueGrabPrefixStr=SetValueGrabStr+':'
SetValueGetGrabStr=SetValueGrabPrefixStr+Getter.GetUndirectStr
SetMapStr=Itemizer.ItemMapPrefixStr+'set'
SetMapValueGetGrabStr=SetValueGrabPrefixStr+Getter.GetMapStr
SetModifyGrabStr='#set'
SetUndirectPrefixStr=Getter.GetUndirectPrefixStr
SetLiargGrabStr='#liarg'
SetLiargGrabPrefixStr=SetLiargGrabStr+':'
SetLiargGetGrabStr=SetLiargGrabPrefixStr+Getter.GetUndirectStr
SetMapLiargGetGrabStr=SetLiargGrabPrefixStr+Getter.GetMapStr
SetKwargGrabStr='#kwarg'
SetKwargGrabPrefixStr=SetKwargGrabStr+':'
SetKwargGetGrabStr=SetKwargGrabPrefixStr+Getter.GetUndirectStr
SetKwargGetGrabPrefixStr=SetKwargGetGrabStr+':'
SetMapKwargGetGrabPrefixStr=SetKwargGrabPrefixStr+Getter.GetMapStr+':'
SetMapKwargGetKeyGrabStr=SetMapKwargGetGrabPrefixStr+'#key'
SetMapKwargGetValueGrabStr=SetMapKwargGetGrabPrefixStr+'#value'
SetMapKwargGetKeyValueGrabStr=SetMapKwargGetGrabPrefixStr+'#key:value'
SetListTypesSet=set(['list','ndarray'])
SetCopyPrefixStr='#copy:'
SetDeepCopyPrefixStr='#deepcopy:'
SetLambdaGrabStr=':#lambda'
SetValueLambdaGrabStr=SetValueGrabStr+SetLambdaGrabStr
SetMapKeyStr='#map'
SetMapVariableStr='#__Variable'
SetUntypePrefixStr='#untype:'
SetLiargLambdaGrabStr=SetLiargGrabStr+SetLambdaGrabStr

class ArgumentDict(collections.OrderedDict):

	def __init__(self,_ArgumentDict=None,_GetterVariable=None):

		#call the base method
		collections.OrderedDict.__init__(self)

		#debug
		'''
		_GetterVariable.debug(
			[
				'_ArgumentDict is ',
				SYS._str(_ArgumentDict)
			]
		)
		'''

		#init
		self['LiargVariablesList']=[]
		self['KwargVariablesDict']=None
		"""
		self['ArgumentDictBool']=any(
			map(
				lambda __KeyStr:
				__KeyStr in _ArgumentDict,
				[
					SetLiargGrabStr,
					SetMapLiargGetGrabStr,
					SetLiargGetGrabStr,
					SetKwargGrabStr,
					SetMapKwargGetKeyGrabStr,
					SetMapKwargGetKeyValueGrabStr
				]
			)
		)
		"""

		#Check
		if hasattr(_ArgumentDict,'items'):

			#/###################/#
			# Check for #liarg
			#

			if SetLiargGrabStr in _ArgumentDict:

				#debug
				'''
				_GetterVariable.debug(
					[
						'we itemize with a value with a SetValueGrabStr inside',
						'SettedTempLiargSettingValueVariable is '+SYS._str(
							SettedTempLiargSettingValueVariable)
					]
				)
				'''

				#set
				self['LiargVariablesList']=_ArgumentDict[
					SetLiargGrabStr
				]

			elif SetMapLiargGetGrabStr in _ArgumentDict:

				#debug
				'''
				_GetterVariable.debug(
					[
						'we set a value with a SetMapLiargGetGrabStr inside'
					]
				)
				'''
				
				#set
				self['LiargVariablesList']=_GetterVariable[
					SYS.deprefix(
						SetMapLiargGetGrabStr,
						SetLiargGrabPrefixStr
					)
				](
					*_ArgumentDict[SetMapLiargGetGrabStr]
				).ItemizedMapValueVariablesList

				#debug
				'''
				_GetterVariable.debug(
					[
						"self['LiargVariablesList'] is ",
						SYS._str(self['LiargVariablesList'])
					]
				)	
				'''
				
			#Check
			elif SetLiargGetGrabStr in _ArgumentDict:

				#debug
				_GetterVariable.debug(
					[
						'we set a value with a SetLiargGetGrabStr inside',
						'_ArgumentDict[SetLiargGetGrabStr] is ',
						_ArgumentDict[SetLiargGetGrabStr]
					]
				)
				
				#Get 
				self['LiargVariablesList']=_GetterVariable[
					_ArgumentDict[SetLiargGetGrabStr]
				]

				#debug
				_GetterVariable.debug(
					[
						'we set a value with a SetLiargGetGrabStr inside',
						'self[\'LiargVariablesList\'] is ',
						str(self['LiargVariablesList'])
					]
				)

			#/###################/#
			# Check for #kwarg
			#

			#Check
			if SetKwargGrabStr in _ArgumentDict:

				#debug
				'''
				_GetterVariable.debug(
						[
							'There is a #kwarg here'
						]
					)
				'''

				#get
				self['KwargVariablesDict']=_ArgumentDict[
					SetKwargGrabStr
				]

			elif SetMapKwargGetKeyGrabStr in _ArgumentDict:

				#debug
				'''
				_GetterVariable.debug(
					[
						'we set a value with a map SetMapKwargGetKeyGrabStr inside',
					]
				)
				'''

				#get get the keys
				SettedKeyVariablesList=_GetterVariable[
					Getter.GetMapStr
				](
					*_ArgumentDict[SetMapKwargGetKeyGrabStr].keys()
				).ItemizedMapValueVariablesList

				#get the values
				SettedValueVariablesList=_ArgumentDict[
					SetMapKwargGetKeyGrabStr
				].values()

				#set
				self['KwargVariablesDict']=dict(
					zip(
						SettedKeyVariablesList,
						SettedValueVariablesList
					)
				)
				
			elif SetMapKwargGetValueGrabStr in _ArgumentDict:

				#debug
				'''
				_GetterVariable.debug(
					[
						'we set a value with a map SetMapKwargGetValueGrabStr inside',
					]
				)
				'''

				#get get the keys
				SettedKeyVariablesList=_ArgumentDict[
					SetMapKwargGetValueGrabStr
				].keys()

				#get the values
				SettedValueVariablesList=_GetterVariable[
					Getter.GetMapStr
				](
					*_ArgumentDict[
					SetMapKwargGetValueGrabStr
				].values()
				).ItemizedMapValueVariablesList

				#set
				self['KwargVariablesDict']=dict(
					zip(
						SettedKeyVariablesList,
						SettedValueVariablesList
					)
				)

			elif SetMapKwargGetKeyValueGrabStr in _ArgumentDict:

				#debug
				'''
				_GetterVariable.debug(
					[
						'we set a value with a map SetMapKwargGetKeyValueGrabStr inside',
					]
				)
				'''

				#get get the keys
				SettedKeyVariablesList=_GetterVariable[
					Getter.GetMapStr
				](
					*_ArgumentDict[
						SetMapKwargGetKeyValueGrabStr
					].keys()
				).ItemizedMapValueVariablesList

				#get the values
				SettedValueVariablesList=_GetterVariable[
					Getter.GetMapStr
				](
					*_ArgumentDict[
						SetMapKwargGetKeyValueGrabStr
					].values()
				).ItemizedMapValueVariablesList

				#set
				self['KwargVariablesDict']=dict(
					zip(
						SettedKeyVariablesList,
						SettedValueVariablesList
					)
				)

		else:

			#Check
			if _ArgumentDict!="Noarg":

				#append
				self['LiargVariablesList'].append(_ArgumentDict)

#</DefineLocals>

#<DefineClass>
@DecorationClass()
class SetterClass(BaseClass):

	def default_init(self,
						_SetTagStr="",
						_SetDeriveSetter=None,
						_SettingKeyVariable=None, 
						_SettingValueVariable=None, 
						_SettingItemBool=True, 	
						_SettingTypeBool=True,	
						_SettedValueVariable=None,
						**_KwargVariablesDict
					):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#Init
		#self.SetTagStr=""
		#self.SetDeriveSetter=None

	def getMapValueVariable(self):

		#return None
		return None

	def __setitem__(self,_KeyVariable,_ValueVariable):
		""" """

		#debug
		'''
		self.debug(
					[
						('locals()[\'',locals(),[
										'_KeyVariable',
										'_ValueVariable']
										,'\']'),
						('self.',self,[
									'SettingKeyVariable',
									#'SettingValueVariable'
									])
					])
		'''
		
		#set (and set before argument to facilitate switch triggers (see later...)
		self.SettingKeyVariable=_KeyVariable
		self.SettingValueVariable=_ValueVariable
		self.set()		

		#set
		return self

	def do_set(self):
		""" """

		#debug
		'''
		self.debug(
			("self.",self,[
				'SettingKeyVariable',
				'SettingValueVariable'
			])
		)	
		'''

		#itemize first
		if self.SettingItemBool:

			#debug
			'''
			self.debug('first we itemize')
			'''

			#itemize
			self.itemize(
					self.SettingKeyVariable
				)

		else:

			#set
			self.ItemizedValueMethod=None

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
					'we are going to call the method but first get it',
					('self.',self,['ItemizedValueMethod'])
				]
			)	
			'''

			#/####################/#
			# Get the method and init the liarg and kwarg
			#

			#get
			SettedValueMethod=self[self.SettingKeyVariable]

			#alias
			SettedLiargVariable=self.SettingValueVariable
			SettedKwargVariable=None

			#/####################/#
			# Check for an argument dict
			#

			#debug
			'''
			self.debug(
					[
						'SettedValueMethod is '+SYS._str(SettedValueMethod),
						'Before calling the itemized method, we adapt the liarg',
						('self.',self,['SettingValueVariable'])
					]
				)
			'''

			#Check
			if hasattr(
					self.SettingValueVariable,'items'
				):

				#Check
				if any(
					map(
						lambda __KeyStr:
						__KeyStr in self.SettingValueVariable,
						[
							SetLiargGrabStr,
							SetMapLiargGetGrabStr,
							SetLiargGetGrabStr,
							SetKwargGrabStr,
							SetMapKwargGetKeyGrabStr,
							SetMapKwargGetKeyValueGrabStr
						]
					)
				):

					#debug
					'''
					self.debug(
							[
								'It is an argument dict'
							]
						)
					'''

					#get
					[SettedLiargVariable,SettedKwargVariable]=map(
						lambda __KeyStr:
						ArgumentDict(
							self.SettingValueVariable,
							self
						)[__KeyStr],
						['LiargVariablesList','KwargVariablesDict']
					)

					#debug
					'''
					self.debug(
							[
								'SettedLiargVariable is '+SYS._str(SettedLiargVariable),
								'SettedKwargVariable is '+SYS._str(SettedKwargVariable),
							]
						)
					'''

				#/#################/#
				# Set a map lambda
				#

				elif SetLiargLambdaGrabStr in self.SettingValueVariable:

					#debug
					'''
					self.debug(
						[
							'we set a value with a SetLiargLambdaGrabStr inside',
							('self.',self,['SettingValueVariable'])
						]
					)
					'''

					#temp
					SettedLambdaValueVariable=self.SettingValueVariable
					SettedLambdaKeyVariable=self.SettingKeyVariable

					#getMap
					SettedMapLambdaList=self.getMapLambdaList(
						SettedLambdaValueVariable
					)

					#debug
					'''
					self.debug(
						[
							'SettedMapLambdaList is',
							str(SettedMapLambdaList)
						]
					)
					'''
					
					#map map set
					map(
						lambda __SettedVariable:
						self.mapSet(__SettedVariable),
						SettedMapLambdaList
					)

					#Stop the setting
					return {"HookingIsBool":False}
				
			#set
			SettedIsBool=False

			#define
			if hasattr(SettedValueMethod,'im_func'):

				#Check
				if hasattr(SettedValueMethod.im_func,'BaseDoClass'):

					#debug
					'''
					self.debug(
							[
								"hasattr(SettedValueMethod.im_func.BaseDoClass.Module,'getLiargVariablesList') is",
								str(hasattr(SettedValueMethod.im_func.BaseDoClass.Module,'getLiargVariablesList'))
							]
						)
					'''

					#Check
					if hasattr(
						SettedValueMethod.im_func.BaseDoClass.Module,
						'getLiargVariablesList'
					):
					
						#set
						SettedIsBool=True

						#get
						SettedLiargVariablesList=SettedValueMethod.im_func.BaseDoClass.Module.getLiargVariablesList(
							SettedLiargVariable
						)

						#debug
						'''
						self.debug(
								'SettedLiargVariablesList is '+str(SettedLiargVariablesList)
							)
						'''
						
						if SettedKwargVariable!=None:

							#get the method and put the value as arguments
							SettedValueMethod(*SettedLiargVariablesList,**SettedKwargVariable)

						else:

							#get the method and put the value as arguments
							SettedValueMethod(*SettedLiargVariablesList)

						#Stop the setting
						return {"HookingIsBool":False}

			if SettedIsBool==False:

				#debug
				'''
				self.debug(
					[
						'call the SettedValueMethod with self.SettingValueVariable directly',
						'SettedLiargVariable is '+SYS._str(SettedLiargVariable)
					]
				)
				'''
				
				#Check
				if hasattr(SettedLiargVariable,'items'):
					SettedLiargVariable=SettedLiargVariable.items()
				elif type(SettedLiargVariable)!=list:
					SettedLiargVariable=[SettedLiargVariable]

				#Check
				if SettedKwargVariable!=None:

					#direct
					#SettedValueMethod(*self.SettingValueVariable)
					SettedValueMethod(*SettedLiargVariable,**SettedKwargVariable)

				else:

					#direct
					#SettedValueMethod(*self.SettingValueVariable)
					SettedValueMethod(*SettedLiargVariable)
			
				#Stop the setting
				return {"HookingIsBool":False}

		#/####################/#
		# Case of a non method  with set with a set key str 
		#

		elif type(
			self.SettingKeyVariable
				) in [str,unicode]:

			#cast
			self.SettingKeyVariable=str(self.SettingKeyVariable)

			#/####################/#
			# Case of #bound: set
			#

			#Check
			if self.SettingKeyVariable.startswith(
				SetBoundPrefixStr
			):

				#deprefix
				SettedMethodStr=SYS.deprefix(
						self.SettingKeyVariable,
						SetBoundPrefixStr
					)

				#debug
				'''
				self.debug(
					[
						'We bound here',
						'SettedMethodStr is '+SettedMethodStr
					]
				)
				'''

				#bound
				setattr(
					self.__class__,
					SettedMethodStr,
					self.SettingValueVariable
				)

				#call
				self.SettingValueVariable(self)

				#stop the setting
				return {'HookingIsBool':False}

			#/####################/#
			# Case of #untype: set
			#

			#Check
			elif self.SettingKeyVariable.startswith(
				SetUntypePrefixStr
			):

				#set
				self.SettingTypeBool=False

				#get
				SettedEachGetVariable=self.set(
					SYS.deprefix(
						self.SettingKeyVariable,
						SetUntypePrefixStr
					),
					self.SettingValueVariable
				)

				#reset
				self.SettingTypeBool=True

				#Return stop the setting
				return {'HookingIsBool':False}

			#/####################/#
			# Case of #each: set
			#

			#Check
			elif self.SettingKeyVariable.startswith(
				SetEachPrefixStr
			):

				#temp
				SettedTempLiargSettingValueVariable=self.SettingValueVariable

				#get
				SettedEachGetVariable=self[
					SYS.deprefix(
						self.SettingKeyVariable,
						SetEachPrefixStr
					)
				]

				#debug
				'''
				self.debug(
					[
						'We each here',
						('self.',self,['SettingKeyVariable']),
						'SettedEachGetVariable is '+str(SettedEachGetVariable)
					]
				)
				'''
				
				#Check
				if hasattr(SettedEachGetVariable,'values'):
					SettedEachGetVariablesList=SettedEachGetVariable.values()
				else:
					SettedEachGetVariablesList=SettedEachGetVariable

				#debug
				'''
				self.debug(
					[
						'SettedEachGetVariablesList is ',
						SYS._str(SettedEachGetVariablesList),
						'SettedTempLiargSettingValueVariable is ',
						SYS._str(SettedTempLiargSettingValueVariable)
					]
				)
				'''
				
				#map
				map(
						lambda __SettedGetVariable,__SettedValueVariable:
						__SettedGetVariable[SetMapStr](
							SYS.SetList(__SettedValueVariable)
						),
						SettedEachGetVariablesList,
						SettedTempLiargSettingValueVariable
					)

				#Return stop the setting
				return {'HookingIsBool':False}

			#/####################/#
			# Case of #all: set
			#

			#Check
			elif self.SettingKeyVariable.startswith(
				SetAllPrefixStr
			):

				#get
				SettedGetVariable=self[
					SYS.deprefix(
						self.SettingKeyVariable,
						SetAllPrefixStr
					)
				]

				#Check
				if hasattr(SettedGetVariable,'values'):
					SettedGetVariablesList=SettedGetVariable.values()
				else:
					SettedGetVariablesList=SettedGetVariable

				#debug
				'''
				self.debug(
					[
						'SettedGetVariablesList is ',
						SYS._str(SettedGetVariablesList),
						('self.',self,['SettingValueVariable'])
					]
				)
				'''

				#Check
				if type(self.SettingValueVariable) in [
							list,tuple
						] and len(self.SettingValueVariable)==2:

					#map
					map(
							lambda __SettedGetVariable:
							__SettedGetVariable.set(
								*self.SettingValueVariable
							),
							SettedGetVariablesList
						)

				else:

						
					#map
					map(
							lambda __SettedGetVariable:
							__SettedGetVariable[SetMapStr](
								self.SettingValueVariable
							),
							SettedGetVariablesList
						)

				#Return stop the setting
				return {'HookingIsBool':False}

			#/####################/#
			# Case of #copy: set
			#

			#Check
			elif self.SettingKeyVariable.startswith(
				SetCopyPrefixStr
			):

				#deprefix
				GetKeyStr=SYS.deprefix(
						self.SettingKeyVariable,
						SetCopyPrefixStr
					)

				#debug
				'''
				self.debug(
					[
						'We copy set here',
						'GetKeyStr is ',
						GetKeyStr
					]
				)
				'''

				#set
				self[GetKeyStr]=copy.copy(self.SettingValueVariable)

				#Return stop the setting
				return {'HookingIsBool':False}

			#Check
			elif self.SettingKeyVariable.startswith(
				SetDeepCopyPrefixStr
			):

				#deprefix
				GetKeyStr=SYS.deprefix(
						self.SettingKeyVariable,
						SetDeepCopyPrefixStr
					)

				#debug
				'''
				self.debug(
					[
						'We deepcopy set here',
						'GetKeyStr is ',
						GetKeyStr
					]
				)
				'''

				#set
				self[GetKeyStr]=copy.deepcopy(self.SettingValueVariable)

				#Return stop the setting
				return {'HookingIsBool':False}

			#/####################/#
			# Case of a set in the __dict__
			#

			else:

				#/####################/#
				# Case of a set with a #get in the value
				#

				if type(
					self.SettingValueVariable
				)==str and self.SettingValueVariable.startswith(SetUndirectPrefixStr):

					#deprefix
					SettedKeyStr=SYS.deprefix(
							self.SettingValueVariable,
							SetUndirectPrefixStr
						)

					#debug
					'''
					self.debug(
						[
							'This is a undirect of a str variable',
							'SettedKeyStr is '+SettedKeyStr
						]
					)
					'''

					#Check
					if SetUndirectPrefixStr in SettedKeyStr:

						#split
						SettedKeyStrsList=SettedKeyStr.split(SetUndirectPrefixStr)

						#define
						SettedRecursiveKeyStr=''.join(
							SettedKeyStrsList[:-1])+self[SettedKeyStrsList[-1]]

						#debug
						'''
						self.debug(
								[
									'This is a recursive undirect set',
									'SettedRecursiveKeyStr is '+SettedRecursiveKeyStr
								]
							)
						'''

						#set
						self[
							self.SettingKeyVariable
						]=SetUndirectPrefixStr+SettedRecursiveKeyStr

					else:

						#debug
						'''
						self.debug(
								'This is one level undirect set'
							)
						'''

						#set
						self[
							self.SettingKeyVariable
						]=self[SettedKeyStr]

					#Stop the getting
					return {"HookingIsBool":False}

				#/####################/#
				# Case of a set with a set dict
				#

				#Check
				elif hasattr(
						self.SettingValueVariable,'items'
					):

					#debug
					'''
					self.debug(
							[
								'Check for a set value dict',
								('self.',self,['SettingValueVariable'])
							]
						)
					'''

					if SetValueGrabStr in self.SettingValueVariable:

						#debug
						'''
						self.debug(
							[
								'we set a value with a SetValueGrabStr inside',
								('self.',self,['SettingValueVariable'])
							]
						)
						'''

						#set
						self[self.SettingKeyVariable]=self.SettingValueVariable[SetValueGrabStr]

						#Return
						return {'HookingIsBool':False}

					elif SetMapValueGetGrabStr in self.SettingValueVariable:

						#debug
						'''
						self.debug(
							[
								'we set a value with a map SetMapValueGetGrabStr inside',
								('self.',self,['SettingValueVariable'])
							]
						)
						'''

						#set
						self[self.SettingKeyVariable]=self[
							SYS.deprefix(
								SetMapValueGetGrabStr,
								SetValueGrabPrefixStr
							)
						](
							*self.SettingValueVariable[SetMapValueGetGrabStr]
						).ItemizedMapValueVariablesList
						

						#Return
						return {'HookingIsBool':False}

					#Check
					elif SetValueGetGrabStr in self.SettingValueVariable:

						#Get 
						SettedGrabValueVariable=self[
							self.SettingValueVariable[SetValueGetGrabStr]
						]

						#debug
						'''
						self.debug(
							[
								'we set a value with a SetValueGetGrabStr inside',
								('self.',self,['SettingValueVariable']),
								'SettedGrabValueVariable is '+SYS._str(
									SettedGrabValueVariable)
							]
						)
						'''

						#set
						self[
							self.SettingKeyVariable
						]=SettedGrabValueVariable

						#Return
						return {'HookingIsBool':False}

					elif SetValueLambdaGrabStr in self.SettingValueVariable:

						#debug
						'''
						self.debug(
							[
								'This is a lambda map set',
								('self.',self,['SettingValueVariable'])
							]
						)
						'''

						#temp
						SettedTempKeyVariable=self.SettingKeyVariable
						SettedTempValueVariable=self.SettingValueVariable
						
						#getMap
						SettedReplaceValueVariablesList=self.getMapLambdaList(
							SettedTempValueVariable
						)

						#set
						self[SettedTempKeyVariable]=SettedReplaceValueVariablesList

						#Return
						return {'HookingIsBool':False}


				#/####################/#
				# Case of an instancing set
				#

				#Check
				if self.SettingTypeBool:

					#debug
					'''
					self.debug(
							[
								'we check if we have to set a default value here',
								('self.',self,[
									'SettingKeyVariable',
									'SettingValueVariable'
								])
							]
						)
					'''

					#get
					SettedValueType=SYS.getTypeClassWithTypeStr(
						SYS.getTypeStrWithKeyStr(
							self.SettingKeyVariable)
					)

					#type
					SettedSettingValueVariableType=type(self.SettingValueVariable)

					#cast
					if SettedSettingValueVariableType==unicode:
						self.SettingValueVariable=str(self.SettingValueVariable)
						SettedSettingValueVariableType=str
						
					#Check
					if SettedValueType!=SettedSettingValueVariableType:

						#debug
						'''
						self.debug(
								[
									'Check that the type is not a lst and a numpy array'
								]
							)
						'''
						
						#Check
						if set([
							SettedValueType.__name__,
							SettedSettingValueVariableType.__name__
						])!=SetListTypesSet:

							#debug
							'''
							self.debug(
								[
									'SettedValueType is '+str(SettedValueType),
									('self.',self,['SettingKeyVariable'])
								]
							)	
							'''

							#Check
							if SettedValueType!=None.__class__:

								#debug
								'''
								self.debug(
									[
										'we wrap the setting value',
										('self.',self,['SettingValueVariable'])
									]
								)
								'''
								
								#alias
								'''
								try:
								'''

								#map set
								self[self.SettingKeyVariable]=SettedValueType(
									).mapSet(
									self.SettingValueVariable
								)
								#self[self.SettingKeyVariable]=SettedValueType(
								#	)[SetMapStr](
								#	self.SettingValueVariable
								#)
								#self.SettingValueVariable=SettedValueType(
								#	)[SetMapValueGetGrabStr](
								#	self.SettingValueVariable
								#)

								'''
								except:

									#debug
									self.debug(
											[
												'set failed because the suffix str indicates a different type from the value',
												'SettedValueType is '+str(SettedValueType),
												'type(self.SettingValueVariable) is '+str(
													type(self.SettingValueVariable))
											]
										)
								'''

								#debug
								'''
								self.debug(
									'Ok we have instanced'
								)
								'''

								#Return
								return {'HookingIsBool':False}

				#/####################/#
				# Check that it is not a property
				#

				#Check
				if hasattr(self.__class__,self.SettingKeyVariable):

					#get
					SettedPropertyValueVariable=getattr(self.__class__,self.SettingKeyVariable)
					
					#Check
					if type(SettedPropertyValueVariable)==property:

						#debug
						'''
						self.debug('It is a property set')
						'''

						#set the property
						setattr(
								self,
								self.SettingKeyVariable,
								self.SettingValueVariable
							)

						#Return
						return {'HookingIsBool':False}


				#/####################/#
				# Set in the __dict__ ... finally 
				# 

				#debug
				'''
				self.debug(
					[
						'we just maybe set in the __dict__',
						('self.',self,[
								'SettingKeyVariable',
								'SettingValueVariable'
							])
					]
				)
				'''
				
				#__setitem__ in the __dict__, this is an utility set
				self.__dict__[
					self.SettingKeyVariable
				]=self.SettingValueVariable

				#/####################/#
				# GIve maybe some things to the setted value 
				# 

				#add in the SettingValue
				try:
					self.SettingValueVariable.SetTagStr=self.SettingKeyVariable
					self.SettingValueVariable.SetDeriveSetter=self
				except:
					pass

				#Return
				return {'HookingIsBool':False}

		#/####################/#
		# Case of a non method set with a set dict in the Key Variable
		#

		elif hasattr(self.SettingKeyVariable,'items'):

			#get
			SettedGetKeyVariable=self[self.SettingKeyVariable]

			#debug
			'''
			self.debug(
					[
						'SettingKeyVariable has items...',
						('self.',self,['SettingKeyVariable']),
						'SettedGetKeyVariable is '+SYS._str(SettedGetKeyVariable)
					]
				)
			'''

			#set
			self.set(
				SettedGetKeyVariable,
				self.SettingValueVariable
			)

			#Return
			return {'HookingIsBool':False}


		#/####################/#
		# Case of a function set
		#

		elif callable(self.SettingKeyVariable):

			#/####################/#
			# Case of a non method with a set dict in the Value Variable
			#

			#debug
			'''
			self.debug(
					[
						'The key is callable',
						('self.',self,[
							'SettingValueVariable',
							'PathDerivePather'
						]),
						'map get the values to have the liargvariables list'
					]
				)
			'''
			
			#Set 
			SettedTempKeyVariable=self.SettingKeyVariable
			SettedLiargVariable=self.SettingValueVariable
			SettedKwargVariable=None

			#/####################/#
			# Check for an argument dict
			#

			#Check
			if hasattr(
					SettedLiargVariable,'items'
				): 

				#Check
				if any(
					map(
						lambda __KeyStr:
						__KeyStr in SettedLiargVariable,
						[
							SetLiargGrabStr,
							SetMapLiargGetGrabStr,
							SetLiargGetGrabStr,
							SetKwargGrabStr,
							SetMapKwargGetKeyGrabStr,
							SetMapKwargGetKeyValueGrabStr
						]
					)
				):

					#debug
					self.debug(
							[
								'It is a argument dict'
							]
						)

					#get
					[SettedLiargVariable,SettedKwargVariable]=map(
						lambda __KeyStr:
						ArgumentDict(
							SettedLiargVariable,
							self
						)[__KeyStr],
						['LiargVariablesList','KwargVariablesDict']
					)

					#debug
					'''
					self.debug(
							[
								'SettedLiargVariable is '+SYS._str(SettedLiargVariable),
								'SettedKwargVariable is '+SYS._str(SettedKwargVariable),
							]
						)
					'''

				else:

					#/###################/
					# It is a get dict
					#

					#call a set to active the #value get
					self.set(
							'TempSetVariable',
							SettedLiargVariable
						)

					#debug
					'''
					self.debug(
							[
								'This is a get dict ',
								'self.TempSetVariable is '+SYS._str(self.TempSetVariable),
								('self.',self,['SettingValueVariable'])
							]
						)
					'''

					#get
					SettedLiargVariable=self.TempSetVariable if type(
						self.TempSetVariable)==list else [self.TempSetVariable]

					#delete
					del self.__dict__['TempSetVariable']

					#reupdate
					self.SettingKeyVariable=SettedTempKeyVariable

			#Check
			if type(SettedLiargVariable)!=list:

				#get
				SettedLiargVariablesList=[SettedLiargVariable]
			else:

				#alias
				SettedLiargVariablesList=SettedLiargVariable

			#debug
			'''
			self.debug(
				[
					'we call here',
					('self.',self,['SettingKeyVariable']),
					'SettedLiargVariablesList is '+SYS._str(SettedLiargVariablesList)
				]
			)
			'''

			#call
			if SettedLiargVariable!=None and SettedKwargVariable!=None:

				self.SettingKeyVariable(
						*SettedLiargVariablesList,
						**SettedKwargVariable
					)
			else:

				self.SettingKeyVariable(
						*SettedLiargVariablesList	
					)

			#debug
			'''
			self.debug(
					'self.SettingKeyVariable.__self__ is '+SYS._str(
						self.SettingKeyVariable.__self__
					)
				)
			'''

			#Return
			return {'HookingIsBool':False}

	def mimic_get(self):

		#Check
		if self.GettingKeyVariable==SetSetterShortStr:

			#get
			self.GettedValueVariable=self.SetDeriveSetter

			#return 
			return {'HookingIsBool':False}
		
		#call the base method
		return BaseClass.get(self)

	def mapSet(self,_MapVariable):

		#debug
		'''
		self.debug(
				[
					'_MapVariable is ',
					SYS._str(_MapVariable)
				]
			)
		'''

		#map
		map(
				lambda __MapTuple:
				self.set(*__MapTuple),
				_MapVariable.items() 
				if hasattr(_MapVariable,'items')
				else _MapVariable
			)

		#return
		return self		

	def getMapLambdaList(self,_SettingValueVariable):

		#debug
		'''
		self.debug(
			[
				'This is a lambda map set',
				'_SettingValueVariable is ',
				SYS._str(_SettingValueVariable)
			]
		)
		'''

		#get
		try:
			SettedTextValueVariable=_SettingValueVariable[SetValueLambdaGrabStr]
		except:
			SettedTextValueVariable=_SettingValueVariable[SetLiargLambdaGrabStr]

		#Check
		if SetMapKeyStr in _SettingValueVariable:

			#get
			SettedMapVariablesList=_SettingValueVariable[SetMapKeyStr]

		elif Getter.GetMapStr in _SettingValueVariable:

			#get
			SettedMapVariablesList=self[Getter.GetMapStr](
				*_SettingValueVariable[Getter.GetMapStr]
			).ItemizedMapValueVariablesList
			
		#debug
		'''
		self.debug(
			[
				'SettedTextValueVariable is ',
				SYS._str(SettedTextValueVariable),
				'SettedMapVariablesList is ',
				SYS._str(SettedMapVariablesList),

			]
		)
		'''

		#mapReplace
		SettedReplaceValueVariablesList=SYS.mapReplace(
			copy.copy(SettedTextValueVariable),
			SettedMapVariablesList,
			self
		)

		#debug
		'''
		self.debug(
				[
					'We have mapReplaced',
					'SettedReplaceValueVariablesList is ',
					SYS._str(SettedReplaceValueVariablesList)
				]
			)
		'''

		#return
		return SettedReplaceValueVariablesList

	def mapArgument(self,_SetVariable,_MapVariable):

		#Debug
		'''
		print('mapArgument l 353')
		print('_MapVariable is ')
		print(_MapVariable)
		print('')
		'''
		
		#map
		ArgumentTuplesList=map(
				lambda __ItemTuple:
				(
					__ItemTuple[0],
					ArgumentDict(
							__ItemTuple[1],
							self
						)
				),
				SYS.SetList(
					_MapVariable
				)
			)

		#debug
		'''
		self.debug(
				[
					'We have setted the map arguments',
					'ArgumentTuplesList is ',
					SYS._str(ArgumentTuplesList),
				]
			)
		'''
		
		#alias
		get=SYS.get

		#map
		VariablesList=map(
				lambda __ArgumentTuple:
				get(
					_SetVariable,
					__ArgumentTuple[0]
				)()
				if len(__ArgumentTuple[1]['LiargVariablesList']
					)==0 and __ArgumentTuple[1]['KwargVariablesDict']==None
				else(
					get(
						_SetVariable,
						__ArgumentTuple[0]
					)(**__ArgumentTuple[1]['KwargVariablesDict'])
					if len(__ArgumentTuple[1]['LiargVariablesList']
					)==0
					else(
						get(
							_SetVariable,
							__ArgumentTuple[0]
						)(
							*__ArgumentTuple[1]['LiargVariablesList'],
							**__ArgumentTuple[1]['KwargVariablesDict']
						) 
						if __ArgumentTuple[1]['KwargVariablesDict']!=None
						else
						get(
							_SetVariable,
							__ArgumentTuple[0]
						)(
							*__ArgumentTuple[1]['LiargVariablesList']
						)
					)
				),
				ArgumentTuplesList
			)

		#debug
		'''
		self.debug(
			[
				'VariablesList is ',
				SYS._str(VariablesList)
			]
		)
		'''

		#return 
		return VariablesList

	def setAttr(self,_KeyStr,_ValueVariable):

		#set
		setattr(self,_KeyStr,_ValueVariable)

		#return
		return self

	def mapSetAttr(self,_MapVariable):

		#map
		map(
			lambda __ElementVariable:
			self.setAttr(*__ElementVariable),
			_MapVariable.items()
			if hasattr(_MapVariable,'items')
			else _MapVariable
		)

		#return
		return self

	def setAttrOrCall(self,_ItemVariable):

		#debug
		'''
		self.debug(
			[
				'_ItemVariable is',
				SYS._str(_ItemVariable)
			]
		)
		'''

		#Check
		if type(_ItemVariable)==str:

			#getattr
			getattr(self,_ItemVariable)()

			
		else:

			#setattr
			setattr(self,*_ItemVariable)

		#return
		return self

	def mapManage(self,_ManageVariablesList):

		#debug
		'''
		self.debug(
			[
				'We mapManage here',
				'_ManageVariablesList is ',
				str(_ManageVariablesList)
			]
		)
		'''
		
		#map
		map(
			lambda __ManageVariable:
			self.manage(
				__ManageVariable[0],
				__ManageVariable[1]
			),
			_ManageVariablesList
		)



#</DefineClass>

#</DefinePrint>
SetterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'SetTagStr',
		'SetDeriveSetter',
		'SettingKeyVariable',
		'SettingValueVariable',
		'SettingItemBool',
		'SettingTypeBool',
		'SettedValueVariable'
	]
)
#<DefinePrint>
