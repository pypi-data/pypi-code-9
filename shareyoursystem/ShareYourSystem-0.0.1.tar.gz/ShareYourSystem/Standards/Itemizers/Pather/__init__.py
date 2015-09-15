# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Pather use its __setitem__ method for setting attributes in deeper levels thanks to 
the PathPrefixStr 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Arrayer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
#</ImportSpecificModules>

#<DefineLocals>
PathPrefixStr="/"
PathOriginStr="~"
PathPreviousStr=".."
#</DefineLocals>

#<DefineFunctions>
def getVariableWithPathVariableAndKeyList(_DictatedVariable,_KeyList):
	''''''
	if type(_KeyList)==list:

		#Empty list case : return the Objects
		if len(_KeyList)==0:
			return _DictatedVariable;
		elif len(_KeyList)==1:

			#One Variable List case : return the associated Value at the Int
			if type(_DictatedVariable) in [list,tuple]:
				if type(_KeyList[0])==int:
					if _KeyList[0]<len(_DictatedVariable):
						return _DictatedVariable[_KeyList[0]]

			elif _KeyList[0] in _DictatedVariable:

				#One Variable Dict case : return the associated Value at the KeyStr
				return _DictatedVariable[_KeyList[0]]
		else:
			
			#Multi Variables case : recursive call with the reduced list
			if _KeyList[0] in _DictatedVariable:
				return getVariableWithPathVariableAndKeyList(_DictatedVariable[_KeyList[0]],_KeyList[1:])

	#Return by default "NotFound"
	return "NotFound"

def getVariableWithDictatedVariableAndKeyVariable(_DictatedVariable,_KeyVariable):
	if type(_KeyVariable)==list:
		return getVariableWithPathVariableAndKeyList(_DictatedVariable,_KeyVariable)
	elif type(_KeyVariable) in SYS.StrTypesList:
		return _DictatedVariable[_KeyVariable] if _KeyVariable in _DictatedVariable else None

def getPathedBackGetStrWithGetStr(_GetStr):

	#Check
	if PathPrefixStr in _GetStr:

		#Get the path just before
		return PathPrefixStr.join(
			_GetStr.split(PathPrefixStr)[:-1]
			)

	else:

		return ""

def getPathedBackVariableWithVariableAndGetStr(_Variable,_GetStr):

	#get
	PathedBackGetStr=getPathedBackGetStrWithGetStr(_GetStr)

	#Check
	if PathedBackGetStr!="":

		#Get the path just before
		PointedBackVariable=_Variable[PathedBackGetStr]

	else:

		#Return the variable directly
		PointedBackVariable=_Variable

	#Return 
	return PointedBackVariable

#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class PatherClass(BaseClass):

	def default_init(self,
				_PathPreviousDerivePatherVariable=None,
				_PathOriginDerivePatherVariable=None,
				_PathingKeyStr="", 				
				_PathedKeyStrsList=None, 		
				_PathedGetKeyStr="", 						
				_PathedGetValueVariable=None,  
				_PathedChildKeyStr="",			
				**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#init
		

	def do_path(self):

		#debug
		'''
		self.debug(('self.',self,['PathingKeyStr']))
		'''
		
		#Split
		self.PathedKeyStrsList=self.PathingKeyStr.split(PathPrefixStr)

		#set
		#self.PathedGetKeyStr=PathPrefixStr.join(self.PathedKeyStrsList[1:])
		self.PathedGetKeyStr=self.PathedKeyStrsList[1]

		#debug
		'''
		self.debug(
					('self.',self,[
									'PathingKeyStr',
									'PathedKeyStrsList',
									'PathedGetKeyStr',
								])
				)
		'''

		#set the PathedGetValueVariable
		if self.PathedGetKeyStr=="":

			#debug
			'''
			self.debug('self.PathedGetKeyStr is ""')
			'''

			#set
			self.PathedGetValueVariable=self

		else:

			#debug
			'''
			self.debug('This is recursive path set so get the pathedvalue')
			'''

			#Set
			if len(self.PathedKeyStrsList)>2:
				self.PathedChildKeyStr=PathPrefixStr+PathPrefixStr.join(
					self.PathedKeyStrsList[2:]
				)

			#getitem
			self.PathedGetValueVariable=self[
				self.PathedGetKeyStr
			]

			#Set the previous
			try:
				#set
				self.PathedGetValueVariable.PathPreviousDerivePatherVariable=self
			
			except:

				#pass
				pass
			

			#Set the origin
			try:

				#Check
				if self.PathOriginDerivePatherVariable!=None:

					#set
					self.PathedGetValueVariable.PathOriginDerivePatherVariable=self.PathOriginDerivePatherVariable

				else:

					#set
					self.PathedGetValueVariable.PathOriginDerivePatherVariable=self

			except:

				#pass
				pass

		#debug
		'''
		self.debug(
			[
				'At the end of the path',
				('self.',self,[
								'PathedGetValueVariable'
							])
			]
		)
		'''

	def mimic_get(self):

		#debug
		'''
		self.debug(
			("self.",self,[
					'GettingKeyVariable',
					'NameStr'
				])
		)
		'''

		#Definition
		OutputDict={'HookingIsBool':True}

		#Check
		if type(
			self.GettingKeyVariable
		)==str:

			#/####################/#
			# Case of getting the origin of the path
			#

			#Check
			if self.GettingKeyVariable==PathOriginStr:

				#debug
				'''
				self.debug('We get the origin here ')
				'''

				#alias
				self.GettedValueVariable=self.PathOriginDerivePatherVariable

				#return 
				return {'HookingIsBool':False}

			#/####################/#
			# Case of getting the previous pather
			#

			#Check
			if self.GettingKeyVariable==PathPreviousStr:

				#debug
				'''
				self.debug('We get the origin here ')
				'''
				
				#alias
				self.GettedValueVariable=self.PathPreviousDerivePatherVariable

				#return 
				return {'HookingIsBool':False}

			#/####################/#
			# Case of walking through the path
			#

			elif self.GettingKeyVariable.startswith(
				PathPrefixStr
			):

				#debug
				'''
				self.debug('We path here')
				'''

				#Path
				self.path(self.GettingKeyVariable)

				#debug
				'''
				self.debug(('self.',self,[
											"PathedKeyStrsList",
											"PathedGetKeyStr",
											"PathedGetValueVariable"
										]
									))
				'''

				#Check
				if self.PathedGetKeyStr=="":

					#debug
					'''
					self.debug('This is a local already self get ')
					'''

					#Direct get
					self.GettedValueVariable=self.PathedGetValueVariable

				elif self.PathedGetKeyStr!="" and len(self.PathedKeyStrsList)==2:

					#debug
					'''
					self.debug('This is a local already get ')
					'''

					#Return the first level
					self.GettedValueVariable=self.PathedGetValueVariable

				else:

					#debug
					'''
					self.debug(
								[
									'This is recursive get with ',
									('self.',self,[
													'PathedGetValueVariable',
													'PathedChildKeyStr',
													'NameStr'
												]
									)
								]
							)
					'''

					#Get with the PathedChildKeyStr
					if self.PathedGetValueVariable!=None:
			
						#get
						self.GettedValueVariable=self.PathedGetValueVariable[
							self.PathedChildKeyStr
						]

				#Stop the getting
				OutputDict['HookingIsBool']=False
				#<Hook>return OutputDict

				#Return
				return OutputDict

		#Call the parent get method
		if OutputDict['HookingIsBool']:

			#debug
			'''
			self.debug(
						[
							'BaseClass.get is '+str(BaseClass.get),
							('self.',self,['GettingKeyVariable'])
						]
					)
			'''
			
			#Call
			return BaseClass.get(self)

		else:

			#return 
			return OutputDict

	def mimic_set(self):
		""" """

		#debug
		'''
		self.debug(
			('self.',self,[
					'SettingKeyVariable',
					'SettingValueVariable'
				]))
		'''

		#Definition
		OutputDict={'HookingIsBool':True}

		#Deep set
		if type(
			self.SettingKeyVariable
		)==str and self.SettingKeyVariable.startswith(
					PathPrefixStr
				):

			#deprefix
			SetKeyVariable=SYS.deprefix(self.SettingKeyVariable,PathPrefixStr)

			#Check
			if PathPrefixStr not in SetKeyVariable:

				#set
				self.set(
					SetKeyVariable,
					self.SettingValueVariable
				)

				#stop the set
				return {'HookingIsBool':False}

			#debug
			'''
			self.debug('We are going to path')
			'''

			#Path
			self.path(self.SettingKeyVariable)

			#debug
			'''
			self.debug(('self.',self,[
										"PathedGetKeyStr",
										"PathedChildKeyStr",
										"PathedGetValueVariable"
									]
								))
			'''

			#set
			#Direct update in the Child or go deeper with the ChildPathStr
			if self.SettingKeyVariable[-1]==PathPrefixStr: 
				
				#debug
				'''
				self.debug('this is a special set inside the pathed variable')
				'''

				#Check
				if self.PathedGetValueVariable!=None:

					#Case where it is an object to set inside
					if 'PatherClass' in map(
										lambda __Class:
										__Class.__name__,
										type(self.PathedGetValueVariable).__mro__
										):

						#debug
						'''
						self.debug(('self.',self,[
													'PathedGetKeyStr',
													'SettingKeyVariable',
													'SettingValueVariable',
													'PathedGetValueVariable'
												]))
						'''

						#Modify directly the PathedGetValueVariable with self.SettingValueVariable
						self.PathedGetValueVariable.__setitem__(
																self.SettingValueVariable[0],
																self.SettingValueVariable[1]
															)


					#Case where it is a set at the level of self of an already setted thing
					else:

						#set to the corresponding point
						self[self.PathedGetKeyStr]=self.SettingValueVariable

				else:

					#debug
					'''
					self.debug(
							[
								'set with setWithPathVariableAndKeyVariable',
								("self.",self,[
												'SettingValueVariable',
												'PathedChildKeyStr'])
							]
					)
					'''

					#Call the setWithPathVariableAndKeyVariable
					setWithPathVariableAndKeyVariable(
						self.PathedGetValueVariable,
						self.PathedChildKeyStr,
						self.SettingValueVariable
					)

			#Case where it is a set at the level of self of new setted thing
			else:

				#debug
				'''
				self.debug(
					[
						'we setitem here',
						('self.',self,['PathedKeyStrsList'])
					]
				)
				'''
				
				#Check
				if self.PathedGetKeyStr!="" and len(
					self.PathedKeyStrsList
				)==2:

					#debug
					'''
					self.debug('we setitem at this level')
					'''

					#set
					self[self.PathedGetKeyStr]=self.SettingValueVariable
				else:

					#define
					ChildSettingKeyStr=PathPrefixStr+PathPrefixStr.join(
						self.PathedKeyStrsList[2:]
					)

					#debug
					'''
					self.debug(
						[
							'we setitem further',
							'ChildSettingKeyStr is '+ChildSettingKeyStr
						]
					)
					'''

					#set
					self.PathedGetValueVariable[
						ChildSettingKeyStr
					]=self.SettingValueVariable

			#Stop the setting
			OutputDict["HookingIsBool"]=False

		#Call the parent get method
		if OutputDict['HookingIsBool']:
			return BaseClass.set(self)
		else:
			return OutputDict

#</DefineClass>

#<DefineFunctions>
def setWithPathVariableAndKeyVariable(_DictatedVariable,_KeyVariable,_ValueVariable,**_KwargsDict):
	'''	'''

	#Get the type
	Type=type(_DictatedVariable)

	#debug
	'''
	print('Pather l.286 ')
	print('Type is ',Type)
	print('_KeyVariable is ',_KeyVariable)
	print('')
	'''

	#Special dict case for also handling SluggerNamesList Key
	if Type in [dict,collections.OrderedDict] or PatherClass in Type.__mro__:

		#debug
		'''
		print('_DictatedVariable has items')
		print('')
		'''

		#set with a list
		if type(_KeyVariable)==list:
			if len(_KeyVariable)>0:
				if _KeyVariable[0]==PathPrefixStr:
					if len(_KeyVariable)==1:

						#debug
						'''
						print('_KeyVariable==[PathPrefixStr]')
						print('So just update')
						print('')
						'''

						#Update
						_DictatedVariable.update(_ValueVariable)
						return

					else:
						_KeyVariable=_KeyVariable[1:]

				#debug
				'''
				print('_KeyVariable is a list')
				print('_KeyVariable is '+str(_KeyVariable))
				print('')
				'''

				#Get the next "path"
				GettedVariable=getVariableWithDictatedVariableAndKeyVariable(_DictatedVariable,_KeyVariable[:-1])

				#debug
				'''
				print('GettedVariable is '+str(GettedVariable))
				print('')
				'''

				#set
				setWithPathVariableAndKeyVariable(GettedVariable,_KeyVariable[-1],_ValueVariable)

				#Return 
				return
		else:

			#debug
			'''
			print('_KeyVariable is not a list')
			print('_KeyVariable is '+str(_KeyVariable))
			print('')
			'''

			#Escape
			if len(_KeyVariable)==0:
				
				#debug
				'''
				print('Pather l.330')
				print('This is an empty _KeyVariable here')
				print('_ValueVariable is '+str(_ValueVariable))
				print('')
				'''

				pass

			#Call a method of the dict
			#elif  (_KeyVariable[0].isalpha() or _KeyVariable[0:2]=="__") and  _KeyVariable[0].lower()==_KeyVariable[0]:
			elif type(_ValueVariable)==SYS.ApplyDictClass:

				#debug
				'''
				print('Pather l.342')
				print('_DictatedVariable is ',_DictatedVariable)
				print('_KeyVariable is ',_KeyVariable)
				print('_ValueVariable is ',_ValueVariable)
				print('')
				'''

				#Get
				Function=getattr(_DictatedVariable,_KeyVariable)

				#Call
				try:
					Function(
								*_ValueVariable['LiargVariablesList'],
								**_ValueVariable['KwargVariablesDict']
							)
				except:
					Function(*_ValueVariable['LiargVariablesList'])
				
				#Return 
				return

			#set deeply in the dict
			elif _KeyVariable.startswith(PathPrefixStr):

				#Case of the dict or OrderedDict we have to convert in list to make the key been understood
				if Type in [dict,collections.OrderedDict]:

					#Split
					_KeyVariable=_KeyVariable.split(PathPrefixStr)[1:]

					#debug
					'''
					print('_KeyVariable has PathPrefixStrs so convert the _KeyVariable into a list')
					print(_KeyVariable)
					print('')
					'''

					#set in the dict
					setWithPathVariableAndKeyVariable(
							_DictatedVariable,
							_KeyVariable,
							_ValueVariable
						)

					#Return 
					return

				else:

					#debug
					'''
					print('_KeyVariable has PathPrefixStrs bu the _DictatedVariable knows how to deal with that')
					'''

					#This is an object that understandsa already how to do
					_DictatedVariable[_KeyVariable]=_ValueVariable

					#Return 
					return

			else:

				#debug
				'''
				print('_KeyVariable has no PathPrefixStr so set direclty')
				print(_KeyVariable)
				print('')
				'''

				#set 
				_DictatedVariable[_KeyVariable]=_ValueVariable

				#Return 
				return

	#List Case
	if type(_DictatedVariable)==list:
		if type(_KeyVariable)==list():
			NextSlugger=getVariableWithDictatedVariableAndKeyVariable(_DictatedVariable,_KeyVariable[0])
			setWithPathVariableAndKeyVariable(NextSlugger,_KeyVariable[1:],_ValueVariable)
			return
		else:
			_DictatedVariable[_KeyVariable]=_ValueVariable
			return	
#</DefineFunctions>

#</DefinePrint>
PatherClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PathPreviousDerivePatherVariable',
		'PathOriginDerivePatherVariable',
		'PathingKeyStr',
		'PathedKeyStrsList',
		'PathedGetKeyStr',
		'PathedChildKeyStr',
		'PathedGetValueVariable'
	]
)
#<DefinePrint>
