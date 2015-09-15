# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Defaultor is a crucial module for understanding how we
can manage high-computer-performance of many instanciations 
without making the memory crashes. For an Instance that is setted
by default, this latter will find its attributes in the 
class __dict__. Once the instance has setted in its __dict__ a 
special value it will stop to look at the class level. 
There is for now no distinction of get,set for mutable or non mutable 
variable.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Classor"
DecorationModuleStr=BaseModuleStr
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import six
Classor=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
DefaultPrefixStr="_"
DefaultDecorationMethodStr="default_init"
DefaultAttributePrefixStr='_'
DefaultWrapMethodStr='default_init'
DefaultDecorationMethodStr="superDefault_init"
#</DefineLocals>

#<DefineLocals>
def DefaultInitFunction(
	_InstanceVariable,
	*_LiargVariablesList,
	**_KwargVariablesDict
):
	pass

def getDefaultedValueVariableWithSetVariable(_SetVariable):

	#Return the instanciation of the type
	if hasattr(_SetVariable,'items'):

		#If it is direct a call of a type without extra argument then instancify
		if 'DefaultValueType' in _SetVariable and len(_SetVariable)==1:
			DefaultedValueVariable=_SetVariable['DefaultValueType']()
			return DefaultedValueVariable 
	
	#Return direct the Variable
	return _SetVariable

def setDefaultMutable(
	_InstanceVariable,
	_ClassVariable,
	_AttributeKeyVariable=None,
	**_KwargVariablesDict
):
	
	#get
	DefaultClassesList=SYS.GetList(_ClassVariable,SYS)

	#Set
	if 'ForceSetIsBool' in _KwargVariablesDict:
		ForceSetIsBool=_KwargVariablesDict['ForceSetIsBool']
	else:
		ForceSetIsBool=False

	#/#################/#
	# Get all the attribute to default set again and filter 
	# the ones that have not the right
	#

	#Check
	if _AttributeKeyVariable==None:
		AttributeKeyStrsList=SYS.sum(
			map(
				lambda __DefaultClass:
				__DefaultClass.DefaultSpecificKeyStrsList,
				DefaultClassesList
			)
		)
	elif type(_AttributeKeyVariable)!=list:
		AttributeKeyStrsList=[AttributeKeyVariable]
	else:
		AttributeKeyStrsList=_AttributeKeyVariable
		
	#/################/#
	# map an init for the mutable variables by detecting them at the level of the class 
	# they are None
	#

	#map
	TypeClassesList=map(
			lambda __AttributeKeyStr:
			SYS.getTypeClassWithTypeStr(
				SYS.getTypeStrWithKeyStr(__AttributeKeyStr)
			)
			if (
					SYS.getIsNoneBool(
						getattr(
							_InstanceVariable,
							__AttributeKeyStr
						)
					) 
					if ForceSetIsBool==False 
					else True
				)
			and getattr(
				_InstanceVariable.__class__,
				__AttributeKeyStr
			)==None
			else None.__class__,
			AttributeKeyStrsList
	)

	#debug
	'''
	print('l 122 Defaultor')
	print('AttributeKeyStrsList is '+str(AttributeKeyStrsList))
	print('TypeClassesList is '+str(TypeClassesList))
	print('')
	'''

	#set in the instance
	map(
			lambda __AttributeKeyStr,__TypeClass:
			setattr(
					_InstanceVariable,
					__AttributeKeyStr,
					__TypeClass()
			)
			if __TypeClass!=None.__class__ 
			else None,
			AttributeKeyStrsList,
			TypeClassesList
	)

	#return 
	return _InstanceVariable

def setDefault(
	_InstanceVariable,
	_ClassVariable,
	_AttributeKeyVariable=None,
	**_KwargVariablesDict
):
	
	#/#################/#
	# Get all the default classes
	#

	#get
	DefaultClassesList=SYS.GetList(_ClassVariable,SYS)

	#Debug
	print('setDefault l 168')
	print('DefaultClassesList is ')
	print(DefaultClassesList)
	print('')

	#/#################/#
	# Get all the attribute to default set again and filter 
	# the ones that have not the right
	#

	#Check
	if _AttributeKeyVariable==None:
		AttributeKeyStrsList=SYS.sum(
			map(
				lambda __DefaultClass:
				__DefaultClass.DefaultSpecificKeyStrsList,
				DefaultClassesList
			)
		)
	elif type(_AttributeKeyVariable)!=list:
		AttributeKeyStrsList=[_AttributeKeyVariable]
	else:
		AttributeKeyStrsList=_AttributeKeyVariable

	#Check
	if 'DefaultNotSetTagStrsList' in _KwargVariablesDict:

		#filter
		AttributeKeyStrsList=SYS._filter(
				lambda __AttributeKeyStr:
				__AttributeKeyStr not in _KwargVariablesDict['DefaultNotSetTagStrsList'],
				AttributeKeyStrsList
			)
		
	#Debug
	print('Defaultor l 194')
	print('AttributeKeyStrsList is ')
	print(AttributeKeyStrsList)
	print('')

	#map a set for all the class attributes into the instance
	map(
			lambda __AttributeKeyStr:
			_InstanceVariable.__setattr__
			(
				__AttributeKeyStr,
				getattr(
						_InstanceVariable.__class__,
						__AttributeKeyStr
					)
			),
			AttributeKeyStrsList
		)

	#set
	'''
	setDefaultMutable(
		_InstanceVariable,
		DefaultClassesList,
		AttributeKeyStrsList
	)
	'''

	#return 
	return _InstanceVariable

#Definition the new init method
def initDefault(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#debug
	'''
	print('Defaultor l.134 : ')
	print('_LiargVariablesList is ',_LiargVariablesList)
	print('_KwargVariablesDict is ',_KwargVariablesDict)
	print('')
	'''

	#set at the level of the class
	InitKwargVariablesDict=dict(
		map(
			lambda __SettingItemTuple:
			(
				DefaultPrefixStr.join(__SettingItemTuple[0].split(DefaultPrefixStr)[1:]) 
				if __SettingItemTuple[0].startswith(DefaultPrefixStr)
				else __SettingItemTuple[0],
				__SettingItemTuple[1]
			),
			_KwargVariablesDict.items()
			)
	)

	#debug
	'''
	print('Defaultor l.155 : ')
	print('InitKwargVariablesDict is ',InitKwargVariablesDict)
	print('')
	'''

	#Update and call the init method of a python object 
	map(
			lambda __ItemTuple:
			_InstanceVariable.__setattr__(__ItemTuple[0],__ItemTuple[1]) 
			#If we want to not set the items setted during hooks and that are not specified...
			if hasattr(_InstanceVariable,__ItemTuple[0]) else None
			,InitKwargVariablesDict.iteritems()
		)

	#call the base method
	object.__init__(_InstanceVariable)

	#get
	DefaultClass=getattr(SYS,_KwargVariablesDict['DefaultClassStr'])
	DefaultWrapUnboundMethod=getattr(DefaultClass,_KwargVariablesDict['DefaultWrapMethodStr'])

	#debug
	'''
	print('Defaultor l.182 : ')
	print('DefaultClass is ',DefaultClass)
	print('DefaultWrapUnboundMethod is ',DefaultWrapUnboundMethod)
	print('')
	'''

	#Call the InitMethodFunction
	try:
		DefaultWrapUnboundMethod(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict)
	except:
		DefaultWrapUnboundMethod(_InstanceVariable,*_LiargVariablesList)

#<DefineLocals>

#<DefineClass>
@DecorationClass()
class DefaultorClass(BaseClass):

	def default_init(self,**_KwargVariablesDict):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#debug
		'''
		print('Defaultor l.31 __call__ method')
		print('_Class is ',_Class)
		print('')
		'''

		#Call the parent init method
		BaseClass.__call__(self,_Class)

		#debug
		'''
		print('Defaultor l.47 look for an __init__ method')
		print('_Class is ',_Class)
		print('')
		'''

		#Check
		if hasattr(_Class,"__init__"):

			#debug
			'''
			print('It has an __init__ method')
			print('')
			'''

			#get
			InitWrapUnboundMethod=getattr(_Class,DefaultWrapMethodStr) if hasattr(_Class,DefaultWrapMethodStr) else DefaultInitFunction

			#set the DefaultDict
			_Class.InitInspectDict=SYS.InspectDict(InitWrapUnboundMethod)

			#Definition the DefaultAttributeItemTuplesList
			DefaultAttributeItemTuplesList=map(
					lambda __DefaultSetItemTuple:
					(
						DefaultPrefixStr.join(
						__DefaultSetItemTuple[0].split(DefaultPrefixStr)[1:]
						),
						getDefaultedValueVariableWithSetVariable(
								__DefaultSetItemTuple[1]
							)
					),
					SYS._filter(
								lambda __DefaultItemTuple:
								__DefaultItemTuple[0].startswith(DefaultPrefixStr),
								_Class.InitInspectDict['DefaultOrderedDict'].items()
							)
			)

			#set
			_Class.DefaultAttributeVariablesOrderedDict=collections.OrderedDict(
					DefaultAttributeItemTuplesList
				)

			#debug
			'''
			print('_Class.DefaultAttributeItemTuplesList is ',_Class.DefaultAttributeItemTuplesList)
			print('')
			'''

			#set at the level of the class
			map(	
					lambda __DefaultSetItemTuple:
					setattr(_Class,*__DefaultSetItemTuple),
					_Class.DefaultAttributeVariablesOrderedDict.items()
				)

			#set the DefaultSpecificKeyStrsList
			_Class.DefaultSpecificKeyStrsList=_Class.DefaultAttributeVariablesOrderedDict.keys()

			#Get the BaseKeyStrsList
			_Class.DefaultBaseKeyStrsList=list(
								SYS.collect(
											_Class,
											'__bases__',
											'DefaultSpecificKeyStrsList'
								)
			)
			
			#Debug
			'''
			print("l 269 Defaultor")
			print("DefaultDecorationMethodStr is ",DefaultDecorationMethodStr)
			print("")
			'''

			#Define the decorated function
			InitExecStr="def "+DefaultDecorationMethodStr+"(_InstanceVariable,"
			InitExecStr+="*_LiargVariablesList,"
			InitExecStr+="**_KwargVariablesDict):\n\t"
			InitExecStr+="initDefault(_InstanceVariable,"
			InitExecStr+="*_LiargVariablesList,"
			InitExecStr+="**dict(_KwargVariablesDict,**{'DefaultWrapMethodStr':'"+DefaultWrapMethodStr+"','DefaultClassStr':'"+_Class.__name__+"'}))\n"
		
			#debug
			'''
			print('Defaultor l 280')
			print('InitExecStr is ')
			print(InitExecStr)
			print('')
			'''
			
			#exec
			six.exec_(InitExecStr)

			#set with the specific name
			setattr(
						_Class,
						DefaultDecorationMethodStr,
						locals()[DefaultDecorationMethodStr]
					)

			#set with the DoMethodStr shortcut
			setattr(
						_Class,
						"__init__",
						locals()[DefaultDecorationMethodStr]
					)

			#set in the class fi not already 
			if hasattr(_Class,'setDefault')==False:

				#set setDefault
				setattr(
							_Class,
							setDefault.__name__,
							setDefault
						)
				
				#set setDefaultMutable
				setattr(
							_Class,
							setDefaultMutable.__name__,
							setDefaultMutable
						)

			#Add to the KeyStrsList
			_Class.KeyStrsList+=[
										#'DefaultAttributeItemTuplesList',
										'DefaultAttributeVariablesOrderedDict',
										'InitInspectDict',
										'DefaultBaseKeyStrsList',
										'DefaultSpecificKeyStrsList'
								]
		#Return 
		return _Class

#</DefineClass>



