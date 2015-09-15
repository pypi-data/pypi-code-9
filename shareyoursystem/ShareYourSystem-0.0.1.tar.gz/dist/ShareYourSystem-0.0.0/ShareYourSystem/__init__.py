# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


ShareYourSystem helps for defining scientific applications
in a Hierarchical Model-View-Controller framework.
"""

#<ImportSpecificModules>
import collections
import copy
import functools
import importlib
import inspect
import inflect
import operator
import os
import re
import sys
import types
#</ImportSpecificModules>

#<DefineLocals>
OuvatonUrlStr="http://shareyoursystem.ouvaton.org"
ShareYourSystemLocalFolderPathStr='/Users/ledoux/Documents/ShareYourSystem/'
OuvatonLocalFolderPathStr=ShareYourSystemLocalFolderPathStr+"Ouvaton/"
PythonlogyLocalFolderPathStr=ShareYourSystemLocalFolderPathStr+'Pythonlogy/'
GithubMasterUrlStr="https://github.com/Ledoux/ShareYourSystem/tree/master"

h5lsPathStr="/usr/local/bin/h5ls"
#PythonPathStr=os.popen('which python'+str(sys.version[0])).read()[:-2]
PythonPathStr="/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python"
IPythonPathStr=os.popen('which ipython'+str(sys.version[0])).read()[:-2]
if IPythonPathStr=="":
	IPythonPathStr="/usr/local/bin/ipython" if sys.version[0
	]=='2' else "/Library/Frameworks/Python.framework/Versions/3.4/bin/ipython3"

NameStrsList=[]

if sys.version[0]==2:
	StrTypesList=[str,unicode]
else:
	StrTypesList=[str]

InflectEngine=inflect.engine()

MutableStrsList=['List','Tuple','Dict','Set']
NotMutableStrsList=['Bool','Int','Float','Str']

ConceptStrsTuplesList=[
	('Object','Objects'),
	('Classor','Classors'),
	('Interfacer','Interfacers'),
	('Guider','Guiders'),
	('Itemizer','Itemizers'),
	('Walker','Walkers'),
	('Noder','Noders'),
	('Controller','Controllers'),
	('Modeler','Modelers'),
	('Viewer','Viewers'),
	('Ploter','Ploters'),
	('Tutorials','Tutorials'),
	('Brianer','Brianers'),
	('Neuroner','Neuroners'),
	('Simulater','Simulaters'),
	('Muziker','Muzikers')
]

#alias
PythonSet=set

#init
IdDict=collections.OrderedDict()
#</DefineLocals>

#<DefineFunctions>
def setStyle(_FilePathStr=""):

	#import
	from IPython import utils
	from IPython.core.display import HTML,display
	import os

	#Check
	if _FilePathStr=="":
		_FilePathStr=os.getcwd()+'/custom.css'

	#Load
	StyleStr = "<style>\n%s\n</style>" % (open(_FilePathStr,'r').read())
	
	#display
	display(
		HTML(
			StyleStr
			)
		)

def setConceptModule(_ModuleGlobalsDict):

	#Debug
	'''
	print('----------------------')
	print('ShareYourSystem  l 73 ')
	print('Begin of the concept set')
	print("_ModuleGlobalsDict['__name__'] is ",_ModuleGlobalsDict['__name__'])
	print('')
	'''

	#Define
	ModuleFolderPathStr='/'.join(_ModuleGlobalsDict['__file__'].split('/')[:-1])
	__all__ = _filter(
					lambda __DirKeyStr:
					os.path.isdir(__DirKeyStr) and os.path.isfile(__DirKeyStr+'/__init__.py'),
					os.listdir(ModuleFolderPathStr)
			)

	#Get
	VarsDict=vars()

	#map
	VarsItemTuplesList=map(
			lambda __VarsKeyStr:
			(
				__VarsKeyStr,
				VarsDict[__VarsKeyStr]
			),
			#_ModuleGlobalsDict.keys()
			[
				'ModuleFolderPathStr',
				'__all__'
			]
		)

	#map Sys to module
	map(
			lambda __VarsItemTuple:
			_ModuleGlobalsDict.__setitem__(
				__VarsItemTuple[0],
				__VarsItemTuple[1]
			) 
			#if __VarsItemTuple[0] not in _ModuleGlobalsDict
			#else None,
			,VarsItemTuplesList
		)

	#Debug
	'''
	print('l 118 ShareYourSystem')
	print("_ModuleGlobalsDict['__name__'] is ",_ModuleGlobalsDict['__name__'])
	print('End of the concept set')
	print('----------------------')
	print('')
	'''

def setSubModule(_ModuleGlobalsDict):
	
	#Debug
	'''
	print('----------------------')
	print('ShareYourSystem  l 131 ')
	print('Begin of the sub set')
	print("_ModuleGlobalsDict['__name__'] is ",_ModuleGlobalsDict['__name__'])
	print('')
	'''

	#map
	'''
	ModuleGlobalsItemTuplesList=map(
			lambda __ModuleGlobalsKeyStr:
			(__ModuleGlobalsKeyStr,_ModuleGlobalsDict[__ModuleGlobalsKeyStr]),
			#_ModuleGlobalsDict.keys()
			[
			]
		)
	'''

	#Debug
	'''
	print('ShareYourSystem l 150')
	print('ModuleGlobalsItemTuplesList is ')
	#print(ModuleGlobalsItemTuplesList)
	print('')
	'''

	'''
	#get
	SysGlobalsDict=globals()

	#map module to sys
	map(
			lambda __ModuleGlobalsItemTuple:
			SysGlobalsDict.__setitem__(*__ModuleGlobalsItemTuple),
			ModuleGlobalsItemTuplesList
		)
	'''
	
	#Define
	BaseModule=None
	BaseNameStr=""
	BaseClass=None
	DecorationModule=None
	DecorationNameStr=""
	DecorationClass=None

	#Get
	BaseModuleStr=_ModuleGlobalsDict['BaseModuleStr']

	#Debug
	'''
	print('ShareYourSystem l 181')
	print("_ModuleGlobalsDict['__name__'] is ",_ModuleGlobalsDict['__name__'])
	print('BaseModuleStr is '+BaseModuleStr)
	print('')
	'''

	if BaseModuleStr!="":
		BaseModule=importlib.import_module(BaseModuleStr)
		BaseNameStr=getNameStrWithModuleStr(BaseModule.__name__)
		BaseClass=getattr(BaseModule,getClassStrWithNameStr(BaseNameStr))

	#Get
	DecorationModuleStr=_ModuleGlobalsDict['DecorationModuleStr']

	#Debug
	'''
	print('ShareYourSystem l 197')
	print("_ModuleGlobalsDict['__name__'] is ",_ModuleGlobalsDict['__name__'])
	print('DecorationModuleStr is '+DecorationModuleStr)
	print('')
	'''

	if DecorationModuleStr!="":
		DecorationModule=importlib.import_module(DecorationModuleStr)
		DecorationNameStr=getNameStrWithModuleStr(DecorationModule.__name__)
		DecorationClass=getattr(DecorationModule,getClassStrWithNameStr(DecorationNameStr))

	#Get
	VarsDict=vars()

	#map
	VarsItemTuplesList=map(
			lambda __VarsKeyStr:
			(
				__VarsKeyStr,
				VarsDict[__VarsKeyStr]
			),
			#_ModuleGlobalsDict.keys()
			[
				'BaseModule',
				'BaseNameStr',
				'BaseClass',
				'DecorationModule',
				'DecorationNameStr',
				'DecorationClass'
			]
		)

	#Debug
	'''
	print('ShareYourSystem l 231')
	print("_ModuleGlobalsDict['__name__'] is ",_ModuleGlobalsDict['__name__'])
	print('VarsItemTuplesList is ')
	print(VarsItemTuplesList)
	print('')
	'''

	#map Sys to module
	map(
			lambda __VarsItemTuple:
			_ModuleGlobalsDict.__setitem__(
				__VarsItemTuple[0],
				__VarsItemTuple[1]
			) 
			#if __VarsItemTuple[0] not in _ModuleGlobalsDict
			#else None,
			,VarsItemTuplesList
		)

	#Debug
	'''
	print('l 252 ShareYourSystem')
	print("_ModuleGlobalsDict['__name__'] is ",_ModuleGlobalsDict['__name__'])
	print('End of the sub set')
	print('----------------------')
	print('')
	'''
	
def getClassStrWithNameStr(_Str):
	return _Str+"Class"

def getNameStrWithClassStr(_ClassStr):
	return 'Class'.join(_ClassStr.split('Class')[:-1])

def getNameStrWithModuleStr(__ModuleStr):
	return __ModuleStr.split('.')[-1]

def getClassWithNameStr(_NameStr):
	return globals()[getClassStrWithNameStr(_NameStr)]

def getKeyStrsListWithClass(_Class):
	return list(filter(
						lambda __KeyStr:
						#You need to do with getattr to have the __getattr__ look up that renders 'instance method' for unbound methods
						__KeyStr[0]==__KeyStr[0].upper() and type(
							getattr(_Class,__KeyStr)
							).__name__!="instancemethod" and __KeyStr[0:2]!="__",
						_Class.__dict__.keys()
					))

def getWordStrsListWithStr(_Str):
	'''
		<Help>
			Split a Str into its Words
		</Help>

		<Test>
			#Load ShareYourSystem as SYS
			import ShareYourSystem as SYS

			#Print some cells
			print("The Words in the Str SuperMan are :"+str(getWordStrsListWithStr("SuperMan")));
			print("The Words in the Str \"FeelLike-A-RainBow\" are :"+str(getWordStrsListWithStr("FeelLike-A-RainBow")));
			print("The Words in the Str \"MySYSHopeItsWorkingHELLO\" are :"+str(getWordStrsListWithStr("MySYSHopeItsWorkingHELLO")));
		</Test>	
	'''
	
	#Get all the Strs with an upper char at the first index
	if type(_Str) in StrTypesList:
		StrsList=list(filter(None,re.split("([A-Z][^A-Z]*)",_Str)))

		#Join the abreviated Strs
		if len(StrsList)>1:

			WordsInt=0
			PreviousStr=StrsList[WordsInt]
			while WordsInt<len(StrsList)-1:
			
				#Increment the Word
				WordsInt+=1
				
				#Definition the Next Str
				NextStr=StrsList[WordsInt]
			
				#Check for Upper Abreviations
				if len(NextStr)==1:
					if (all(map(lambda Char:Char.upper()==Char,list(PreviousStr)))) and (NextStr.upper()==NextStr):
					
						#Join Previous and NextStr
						StrsList[WordsInt-1]=PreviousStr+NextStr

						#Remove the NextStr
						StrsList.pop(WordsInt)
				
						#Increment
						WordsInt-=1

				#Shift the Previous Str
				if WordsInt<len(StrsList):
					PreviousStr=StrsList[WordsInt]

		#Return StrsList
		return StrsList

	#Return [] by default
	else:
		return [""]

def getLowerWordStr(_WordStr):
	if _WordStr[0]=='_':
		return '_'+_WordStr[1].lower()+_WordStr[2:]
	else:
		return _WordStr[0].lower()+_WordStr[1:]

def getUpperWordStr(_WordStr):
	if _WordStr[0]=='_':
		return '_'+_WordStr[1].upper()+_WordStr[2:]
	else:
		return _WordStr[0].upper()+_WordStr[1:]

def getDefaultArray():
	import numpy
	return numpy.array([])

def getTypeClassWithTypeStr(_TypeStr):

	#Debug
	'''
	print('SYS getTypeClassWithTypeStr l.121 ')
	print('_TypeStr is '+_TypeStr)
	print('')
	'''

	#Check
	if _TypeStr=='OrderedDict':

		#Special collections case
		return collections.OrderedDict

	elif _TypeStr=='Function':

		#Return None
		return None.__class__

	#elif _TypeStr=='Array':
	#
	#	#return 
	#	return getDefaultArray

	elif _TypeStr in MutableStrsList+NotMutableStrsList :

		#Other standard mutable cases
		return getattr(
				sys.modules['__builtin__'],
				_TypeStr[0].lower()+_TypeStr[1:]
			)

	elif _TypeStr in NameStrsList:

		#Type defined in the SYS system
		return getattr(
				globals()[_TypeStr],
				getClassStrWithNameStr(_TypeStr)
			)

	else:

		#Define
		ClassStr=getClassStrWithNameStr(_TypeStr)

		#debug
		'''
		print('SYS getTypeClassWithTypeStr l.166 ')
		print('ClassStr is '+ClassStr)
		print('')
		'''
		
		#Return an instance of this corresponding class		
		if hasattr(sys.modules['ShareYourSystem'],ClassStr):
			return getattr(sys.modules['ShareYourSystem'],ClassStr)

		#Return None class
		else:
			return None.__class__

def getTypeStrWithKeyStr(_KeyStr):

	#debug
	'''
	print('SYS  getTypeStrWithKeyStr l.168 ')
	print('_KeyStr is '+_KeyStr)
	print('')
	'''

	#Definition
	global NameStrsList

	#filter
	TypeStrsList=list(
		filter(
		lambda __Variable:
		__Variable!=None,
		map(
			lambda __TypeStr:
			__TypeStr if _KeyStr.endswith(__TypeStr)
			else None,
			[
				'OrderedDict'
			]+NameStrsList
		)
	))

	#Check
	if len(TypeStrsList)==1:

		#Return the found type
		return TypeStrsList[0]

	else:

		#Return the last word
		return getWordStrsListWithStr(_KeyStr)[-1]

def getNewMethodBool(_Class,_MethodStr):

	#base
	if len(_Class.__bases__)>0:
		BaseClass=_Class.__bases__[0]
	else:
		return True

	#get
	Method=getattr(_Class,_MethodStr)

	#Check
	if hasattr(BaseClass,_MethodStr):
		return getattr(BaseClass,_MethodStr)!=Method
	else:
		return True

def getIsNoneBool(_Variable):

	#debug
	'''
	print('SYS  getIsNoneBool l.443 ')
	print('_Variable is ',_Variable)
	print('type(_Variable) is ',type(_Variable))
	print('')
	'''

	#Define 
	Type=type(_Variable)

	#Check
	import numpy
	if Type!=numpy.ndarray:

		#Debug
		'''
		print('SYS  getIsNoneBool l.456 ')
		print('Type is ')
		print(Type)
		print('')
		'''
		
		#return
		return Type==None.__class__

	else:

		#Debug
		'''
		print('SYS  getIsNoneBool l.456 ')
		print('Type is ')
		print(Type)
		print('')
		'''

		#return 
		return False

def getLocalFolderPathStr(_ModuleVariable):
	return ShareYourSystemLocalFolderPathStr+_ModuleVariable

def getNone(_KeyVariable,_ValueVariable):
	return None

def add(_VariableA,_VariableB):

	#Debug
	'''
	print('SYS l 500 ')
	print('add')
	print('type(_VariableA) is '+str(type(_VariableA)))
	print('')
	'''

	#Check
	if hasattr(_VariableA,'__add__'):

		#Debug
		'''
		print('SYS l 502')
		print('_VariableA has __add__')
		print('')
		'''

		#set
		_VariableA=_VariableA.__add__(_VariableB)

		#return 
		return _VariableA

	elif type(_VariableA)==PythonSet:

		#Debug
		'''
		print('SYS l 512')
		print('_VariableA is a set')
		print('_VariableB is ')
		print(_VariableB)
		print('')
		'''

		#set
		_VariableA=_VariableA.union(_VariableB)
		
		#Debug
		'''
		print('_VariableA is after union')
		print(_VariableA)
		print('')
		'''
		
		#return
		return _VariableA

def stdout(_PrintStr):
	sys.stdout.write(_PrintStr+'\n')
	sys.stdout.flush()

def wait(_SecondInt):
	import time
	for __IndexInt in xrange(_SecondInt):
		sys.stdout.write('...'+str(_SecondInt-__IndexInt)+'s')
		sys.stdout.flush()
		time.sleep(1)
	sys.stdout.write('\n')
	sys.stdout.flush()

def indent(_Variable):
	if hasattr(_Variable,'items')==False:
		_Variable=_Variable.__dict__
	import json
	return json.dumps(
			dict(
				zip(
						_Variable.keys(),
						map(str,_Variable.values())
					)
			),
				indent=2
		)

def pick(_Variable,_GetVariablesList,_GetMethodStr='getattr'):

	#Check
	if _GetMethodStr=='getattr':

		#return 
		return map(
				lambda __GetVariable:
				getattr(
					_Variable,
					__GetVariable
				),
				_GetVariablesList
			)
	elif _GetMethodStr=='__getitem__':

		#return 
		return map(
				lambda __GetVariable:
				_Variable[__GetVariable],
				_GetVariablesList
			)

def match(_KeyList,_ValueList):

	#Debug
	'''
	print('SYS l 632')
	print('_KeyList is ')
	print(_KeyList)
	print('_ValueList is ')
	print(_ValueList)
	'''

	#Check
	if len(_KeyList)<len(_ValueList):
		MatchTuplesList=zip(
			_KeyList,
			_ValueList[:len(_KeyList)]
		)
	else:
		MatchTuplesList=zip(
			_KeyList,
			_ValueList
		)

	#Debug
	'''
	print('MatchTuplesList is ')
	print(MatchTuplesList)
	print('')
	'''

	#return
	return MatchTuplesList

def _filter(_Function,_List):
	if sys.version[0]==2:
		return filter(_Function,_List)
	else:
		return list(filter(_Function,_List))

def filterNone(_List):

	#Debug
	"""
	print("List is")
	print(_List)
	print("")
	"""

	#return
	return _filter(
		lambda __ListedVariable:
		type(__ListedVariable)!=None.__class__,
		_List
	)

def flip(_Dict):
	return type(_Dict)(
				map(lambda __ItemTuple:(__ItemTuple[1],__ItemTuple[0]),_Dict.items())
			)

def reverse(_List):
	ReversedList=copy.copy(list(_List))
	ReversedList.reverse()
	return ReversedList

def sum(_VariablesListOrArray):

	#import
	import numpy as np

	if type(_VariablesListOrArray)==np.ndarray:

		#Check
		if type(_VariablesListOrArray[0])==np.ndarray:

			#list
			ShapeIntsList=list(np.shape(_VariablesListOrArray))

			#add
			NewShapeIntsList=[ShapeIntsList[0]*ShapeIntsList[1]]+ShapeIntsList[2:]

			#Debug
			'''
			print('l 705 sum SYS')
			print('ShapeIntsList is ')
			print(ShapeIntsList)
			print('NewShapeIntsList is ')
			print(NewShapeIntsList)
			print('')
			'''

			#return
			return _VariablesListOrArray.reshape(
					NewShapeIntsList
				)

		else:

			#return
			return np.sum(_VariablesListOrArray)

	else:

		#Check
		if len(_VariablesListOrArray)>0:

			#reduce
			return functools.reduce(
									lambda __List,__Variable:
									__List+list(__Variable) 
									if type(__Variable) in [list,tuple] 
									else __List+[__Variable],
									_VariablesListOrArray
								)
		else:

			#return
			return []

def flat(_VariablesList):
	if len(_VariablesList)>0:
		if type(_VariablesList[0])!=list:
			_VariablesList[0]=[_VariablesList[0]]
		return functools.reduce(
									lambda __List,__Variable:
									__List+flat(list(__Variable)) 
									if type(__Variable) in [list,tuple] 
									else __List+[__Variable],
									_VariablesList
								)
	else:
		return _VariablesList

def path(_PathStrsList):

	#Reduce
	PathStr=functools.reduce(
			lambda _TotalPathStr,_PathStr:
			_TotalPathStr+_PathStr 
			if (len(_TotalPathStr)>0 and _TotalPathStr[-1]=='/') and (len(_PathStr)>0 and _PathStr[0]!='/'
				) or (len(_TotalPathStr)>0 and _TotalPathStr[-1]!='/') and (len(_PathStr)>0 and _PathStr[0]=='/')
			else 
			_TotalPathStr[:-1]+_PathStr 
			if (len(_TotalPathStr)>0 and _TotalPathStr[-1]=='/') and (len(_PathStr)>0 and _PathStr[0]=='/'
				)
			else _TotalPathStr+'/'+_PathStr 
			if '/' not in [_PathStr,_TotalPathStr]
			else "",
			_PathStrsList
			)

	#Maybe add / at the beginning
	if (len(PathStr)>0 and PathStr[0]!='/') or PathStr=="":
		PathStr='/'+PathStr

	#Return
	return PathStr

def collect(_Variable,_WalkingKeyStr,_GettingKeyStr):

	#Get the collectedListsList
	return flat(map(
					lambda _ListedVariable:
					flat(
							([
								getattr(_ListedVariable,_GettingKeyStr
									)] if hasattr(_ListedVariable,_GettingKeyStr)
								else []
							)+(collect(_ListedVariable,_WalkingKeyStr,_GettingKeyStr
								) if hasattr(_ListedVariable,_WalkingKeyStr)
								else []
							)
						)
					,getattr(_Variable,_WalkingKeyStr)
				))

def map_(_Function,_List,**_KwargVariablesDict):
	
	#Check
	if 'MultiprocessBool' in _KwargVariablesDict and _KwargVariablesDict['MultiprocessBool']:

		from multiprocessing import Pool
		MapPool=Pool(min(len(_List),100))
		return MapPool.map(_Function,_List)

	else:

		#Check version
		if sys.version[0]==2:
			map(_Function,_List)
		else:
			return list(map(_Function,_List))

	
def range_(*ArgsList):
	if sys.version[0]==2:
		return range(*ArgsList).__iter__()
	else:
		return range(*ArgsList)

def unzip(_TuplesList,_IndexesList,_ArrayBool=False):

	#map
	PickedList=map_(
				lambda __Tuple:
				map(__Tuple.__getitem__,_IndexesList),
				_TuplesList
			)

	#Check
	if len(_IndexesList)==1 and len(PickedList)>0:
		OutVariable=list(zip(*PickedList)[0])
	else:
		OutVariable=zip(*PickedList)

	#Check
	if _ArrayBool:
		import numpy as np
		return np.array(OutVariable)
	else:
		return OutVariable 

def dictify(_TuplesList,_KeyIndexInt,_ValueIndexInt):
	TuplesList=unzip(_TuplesList,[_KeyIndexInt,_ValueIndexInt])
	return collections.OrderedDict(zip(TuplesList[0],TuplesList[1]))

def listify(_List):
	return map(lambda __ElementVariable:[__ElementVariable],_List)

def arrayify(_VariablesList,_ShapeIntsList=None):

	#Debug
	'''
	print('SYS l 807 arrayify')
	print('_VariablesList is ')
	print(_VariablesList)
	print('')
	'''

	#unzip
	[
		IndexIntsTuplesList,
		ValueVariablesList
	]=unzip(_VariablesList,[0,1])

	#Debug
	'''
	print('SYS l 818 arrayify')
	print('IndexIntsTuplesList is ')
	print(IndexIntsTuplesList)
	print('')
	'''

	#get
	DimensionsInt=len(IndexIntsTuplesList[0])

	#Check
	if _ShapeIntsList==None:

		#unzip
		ShapeIntsList=map(
			lambda __DimensionInt:
			max(unzip(IndexIntsTuplesList,[__DimensionInt]))+1,
			xrange(DimensionsInt)
		)
	else:

		#set
		ShapeIntsList=_ShapeIntsList

	#Debug
	'''
	print('SYS l 820 arrayify')
	print('ShapeIntsList is ')
	print(ShapeIntsList)
	print('')
	'''

	#import
	import numpy as np

	#init
	if type(_VariablesList[0][1]) in [list,np.ndarray]:

		#init
		VariablesArray=np.zeros(
			ShapeIntsList+[len(_VariablesList[0][1])],
			dtype=type(_VariablesList[0][1])
		)

		#set
		map(
			lambda __IndexIntsTuple,__ValueVariable:
			VariablesArray.__setitem__(
				__IndexIntsTuple,
				np.array(__ValueVariable)
			),
			IndexIntsTuplesList,
			ValueVariablesList
		)

	else:

		#init
		VariablesArray=np.zeros(
			ShapeIntsList,
			dtype=type(_VariablesList[0][1])
		)

		#set
		map(
			lambda __IndexIntsTuple,__ValueVariable:
			VariablesArray.__setitem__(
				__IndexIntsTuple,
				np.array(__ValueVariable)
			),
			IndexIntsTuplesList,
			ValueVariablesList
		)

	#return
	return VariablesArray

def split(_StartVariable=0,_StopInt=1,_SplitInt=2):

	#import
	import numpy as np

	#Check
	if type(_StartVariable)==int:

		#set
		CutIntsList=np.linspace(_StartVariable,_StopInt,_SplitInt+1,dtype=int)

		#Debug
		"""
		print("SYS l 967 split")
		print("CutIntsList is ")
		print(CutIntsList)
		print("")
		"""

		#map
		return map(
			lambda __IndexIntAndCutInt:
			[CutIntsList[__IndexIntAndCutInt[0]],__IndexIntAndCutInt[1]],
			enumerate(
				CutIntsList[1:]
			)
		)

	else:

		#map
		SplitIntsListsList=map(
			lambda __ShapeInt:
			split(0,__ShapeInt,_SplitInt),
			np.shape(_StartVariable)
		)

		#Debug
		print("SYS l 991 split")
		print("SplitIntsListsList is ")
		print(SplitIntsListsList)
		print("")

		#import
		import itertools

		#product
		return map(
			lambda __GetIntsListsTuple:
			_StartVariable.__getitem__(
				map(
					lambda __GetIntsList:
					slice(__GetIntsList[0],__GetIntsList[1]),
					__GetIntsListsTuple
				)	
			),
			list(itertools.product(*SplitIntsListsList))
		)

def getArray(_Array,_IndexIntsTuple,_LoopBool=True):

	#Debug
	"""
	print("_IndexIntsTuple is ")
	print(_IndexIntsTuple)
	print("-1 in _IndexIntsTuple is "+str(-1 in _IndexIntsTuple))
	print("")
	"""

	#Check
	if _LoopBool==False:

		#Check
		if -1 in _IndexIntsTuple:

			#return
			return None

	#try
	try:

		#return
		return _Array.__getitem__(_IndexIntsTuple)
	except:

		#return
		return None

def contour(_GridBoolsArray,_ContourIntsList=None):

	#import
	import numpy as np

	#get
	LocalArray=getLocalArray(len(np.shape(_GridBoolsArray)))

	#Debug
	"""
	print('LocalArray is ')
	print(LocalArray)
	print('')
	"""

	#map
	return np.array(
		map(
			lambda __Tuple:
			__Tuple[0],
			_filter(
				lambda __Tuple:
				__Tuple[1],
				map(
					lambda __IndexIntsTupleAndValueVariableTuple:
					(
						__IndexIntsTupleAndValueVariableTuple[0],
						any(
							map(
								lambda __Value:
								__Value!=__IndexIntsTupleAndValueVariableTuple[1],
								filterNone(
									map(
										lambda __IndexIntsArray:
										getArray(_GridBoolsArray,tuple(__IndexIntsArray),_LoopBool=False),
										map(
											lambda __LocalArray:
											np.array(__IndexIntsTupleAndValueVariableTuple[0])+__LocalArray,
											LocalArray
										)
									)
								)
							)
						)
					),
					np.ndenumerate(_GridBoolsArray)
				)
			)
		)
	)

def where(_DictsList,_TuplesList,**_KwargsDict):

	if 'IsInCheckingBool' in _KwargsDict and _KwargsDict['IsInCheckingBool']:

		return map(
						lambda __RowingDict:
						#Say True for the ones that respect all the conditions
						__RowingDict
						if all(
							map(
								lambda __FilteringTuple:
								__FilteringTuple[1][0](__RowingDict[__FilteringTuple[0]],__FilteringTuple[1][1])
								#Check that the Key exists...Can maybe make slower the process....
								if __FilteringTuple[0] in __RowingDict else False
								,_TuplesList
								)
							)
						#set None either
						else None,
						_DictsList
					)

	else:

		return map(
						lambda __RowingDict:
						#Say True for the ones that respect all the conditions
						__RowingDict
						if all(
							map(
								lambda __FilteringTuple:
								__FilteringTuple[1][0](__RowingDict[__FilteringTuple[0]],__FilteringTuple[1][1])
								,_TuplesList
								)
							)
						#set None either
						else None,
						_DictsList
					)

def find(_Array, _PredicateFunction, _ChunkSizeInt=1024):
	"""
	Find the indices of array elements that match the predicate.

	Parameters
	----------
	_Array : array_like
	    Input data, must be 1D.

	_PredicateFunction : function
	    A function which operates on sections of the given array, returning
	    element-wise True or False for each data value.

	_ChunkSizeInt : integer
	    The length of the chunks to use when searching for matching indices.
	    For high probability predicates, a smaller number will make this
	    function quicker, similarly choose a larger number for low
	    probabilities.

	Returns
	-------
	index_generator : generator
	    A generator of (indices, data value) tuples which make the predicate
	    True.

	See Also
	--------
	where, nonzero

	Notes
	-----
	This function is best used for finding the first, or first few, data values
	which match the predicate.

	Examples
	--------
	>>> _Array = np.sin(np.linspace(0, np.pi, 200))
	>>> result = find(_Array, lambda arr: arr > 0.9)
	>>> next(result)
	((71, ), 0.900479032457)
	>>> np.where(_Array > 0.9)[0][0]
	71

	"""

	#Check
	if _Array.ndim != 1:
		Array=_Array.flatten()
		#raise ValueError('The array must be 1D, not {}.'.format(_Array.ndim))
	else:
		Array=_Array

	#import
	from itertools import chain, izip

	#init
	InitInt = 0
	ChunkIndexIntsIterator = chain(
		xrange(
			_ChunkSizeInt, 
			Array.size, 
			_ChunkSizeInt
		), 
		[None]
	)

	#for
	for _IndexInt in ChunkIndexIntsIterator:
		ChunkArray = Array[InitInt:_IndexInt]
		for __IndexList in izip(*_PredicateFunction(ChunkArray).nonzero()):
			yield (__IndexList[0] + InitInt, ), ChunkArray[__IndexList]
		InitInt = _IndexInt


def getIsConstantBool(_BoolsArray):

	#import
	import numpy as np

	#get
	ConstantBool=_BoolsArray.__getitem__(tuple([0]*len(np.shape(_BoolsArray))))
	OppositeBool=not ConstantBool

	#Debug
	'''
	print("ConstantBool is ")
	print(ConstantBool)
	print("")
	'''

	#return
	try:

		#next
		next(
			find(
				_BoolsArray,
				lambda __Bool:__Bool==OppositeBool
			)
		)

		#return True
		return False

	except StopIteration:

		#return
		return True

def getFlattenedListWithVariablesList(_VariablesList):
	return functools.reduce(
		lambda x,y:
			x+list(y) if type(y)==tuple 
			else list(x)+[y] if type(x) in [list,tuple] 
			else [x,y],_VariablesList
	)

def getPermutedIntsListWithCategoriesIntAndLengthInt(_CategoriesInt,_LengthInt):

	#import
	import itertools

	#return
	return functools.reduce(
		lambda x,y:
			map(
					lambda __IntOrTuple:
							getFlattenedListWithVariablesList(list(__IntOrTuple)) 
							if type(__IntOrTuple)==tuple
							else __IntOrTuple,
							itertools.product(x,y)
				),
			map(lambda Int:xrange(_LengthInt),xrange(_CategoriesInt))
	)

def getLocalArray(_DimensionInt,_DiagonalBool=False):

	#import
	import numpy as np

	#Check
	if _DiagonalBool:
		
		#array
		PositiveArray=np.array(
			getPermutedIntsListWithCategoriesIntAndLengthInt(
				_DimensionInt,
				2
			)
		)

		#return
		return PositiveArray

	else:

		#diag
		DiagonalArray=np.diag([1]*_DimensionInt)

		#init
		LocalArray=np.zeros((2*_DimensionInt,_DimensionInt),dtype=int)

		#fill
		LocalArray[:_DimensionInt,:]=DiagonalArray
		LocalArray[_DimensionInt:,:]=-1.*DiagonalArray

		#return
		return LocalArray






def translate(_TextStr,_TranslationVariable):

	#Debug
	'''
	print('SYS l 811')
	print('_TextStr is ')
	print(_TextStr)
	print('_TranslationVariable is ')
	print(_TranslationVariable)
	print('')
	'''

	#/##################/#
	# Adapt the shape of the _TranslationVariable
	#

	#Check just for one word translation
	if hasattr(_TranslationVariable,'items')==False:
		_TranslationVariable={
			'#__Variable':_TranslationVariable
		}

	#import 
	import re

	#set
	RepDict = dict((re.escape(k), v) for k, v in _TranslationVariable.iteritems())

	#compile
	pattern = re.compile("|".join(RepDict.keys()))

	#sub
	ReplaceStr=pattern.sub(
		lambda m: 
		RepDict[re.escape(m.group(0))],
		_TextStr
	)

	#Debug
	'''
	print('SYS l 841')
	print('ReplaceStr is ')
	print(ReplaceStr)
	print('')
	'''

	#return
	return ReplaceStr

def replace(
				_TextVariable,
				_ReplaceVariable,
				_GetterVariable=None,
				_TranslationVariable=None
			):

	#Debug
	'''
	print('SYS 905')
	print('_TextVariable is ')
	print(_TextVariable)
	print('')
	'''

	#/##################/#
	# Is the _TranslationVariable setted already
	# 

	#Check
	if _TranslationVariable==None:

		#Debug
		'''
		print('SYS l 870')
		print('_ReplaceVariable is ')
		print(_ReplaceVariable)
		print('')
		'''
		
		#Check
		if hasattr(_ReplaceVariable,'items'):
			ReplaceVariable=_ReplaceVariable.items()
		else:
			ReplaceVariable=_ReplaceVariable

		#Debug
		'''
		print('SYS l 920')
		print('ReplaceVariable is ')
		print(ReplaceVariable)
		print('')
		'''

		#map
		_TranslationVariable=dict(
			map(
				lambda __ItemTuple:
				(
					__ItemTuple[0],
					str(__ItemTuple[1])
				),
				ReplaceVariable
			)
		)

	#/##################/#
	# Is it a str 
	# 

	#init
	ReplaceMapBool=False

	#Check
	if type(_TextVariable) in [str,unicode]:

		#/##################/#
		# Check that it is maybe already in
		# the translation dict

		if _TextVariable in _TranslationVariable:

			#get
			TextVariable=_TranslationVariable[_TextVariable]

		else:

			#translate
			TextVariable=translate(
				_TextVariable,
				_TranslationVariable
			)

		#/##################/#
		# Do we have to get 
		# with it

		#Check
		if _GetterVariable!=None:

			#Check
			if type(TextVariable) in [str,unicode]:

				#Check
				if TextVariable.startswith('#get:'):

					#return
					return _GetterVariable[
								deprefix(
									TextVariable,
									'#get:'
								)
							]

			else:

				#return
				return _GetterVariable[
							TextVariable
						]

		#return
		return TextVariable

	#/##################/#
	# It is a dict iter variable
	# transform to a tuples list

	elif hasattr(_TextVariable,'items'):

		#items
		TextVariable=_TextVariable.items()

		#set
		ReplaceMapBool=True

	elif getIsTuplesListBool(_TextVariable):

		#alias
		TextVariable=_TextVariable

		#set
		ReplaceMapBool=True

	#Check
	if ReplaceMapBool:

		#/##################/#
		# Map the replace
		# 

		#Debug
		'''
		print('SYS l 992')
		print('TextVariable is ')
		print(TextVariable)
		print('')
		'''

		#map
		TextVariable=map(
				lambda __ItemTuple:
				(
					replace(
					__ItemTuple[0],
					_TranslationVariable,
					_GetterVariable
					),
					replace(
						__ItemTuple[1],
						_TranslationVariable,
						_GetterVariable
					)
				),
				TextVariable
			)

		#return
		return type(_TextVariable)(TextVariable)

	#/##################/#
	# It is a list iter variable
	# transform to a tuples list

	elif type(_TextVariable) in [list,tuple]:

		#set
		TextVariable=map(
				lambda __ElementVariable:
				replace(
					__ElementVariable,
					_TranslationVariable,
					_GetterVariable
				),
				_TextVariable
			)

		#return
		return type(_TextVariable)(TextVariable)

	#/##################/#
	# default
	# 

	else:

		#set
		TextVariable=_TextVariable

	#/##################/#
	# return
	# 

	#return
	return type(_TextVariable)(TextVariable)

def mapReplace(
		_TextVariable,
		_ReplaceMapVariable,
		_GetterVariable=None,
		_TranslationVariable=None
	):
	
	#Debug
	'''
	print('SYS l 1001')
	print('_ReplaceMapVariable is ')
	print(_ReplaceMapVariable)
	print('')
	'''
	
	#Check
	if type(_ReplaceMapVariable)==list and len(
		_ReplaceMapVariable)>1 and type(
		_ReplaceMapVariable[1])==list:

		#Debug
		'''
		print('SYS l 1014')
		print('It is a header list replace')
		print('')
		'''

		#map
		ReplaceVariablesList=map(
					lambda __ValueVariable:
					zip(
						_ReplaceMapVariable[0],
						__ValueVariable
					),
					_ReplaceMapVariable[1]
				)
	elif type(_ReplaceMapVariable)==list and type(
		_ReplaceMapVariable[0]) in [str,unicode]:

		#Debug
		'''
		print('SYS l 1035')
		print('It is just one value replace')
		print('')
		'''

		#map
		ReplaceVariablesList=map(
			lambda __Variable:
			{'#__Variable':__Variable},
			_ReplaceMapVariable
		)

	else:
		#Debug
		'''
		print('SYS l 1050')
		print('Alias direct')
		print('')
		'''

		#alias
		ReplaceVariablesList=_ReplaceMapVariable

	#Debug
	'''
	print('SYS l 1059')
	print('ReplaceVariablesList is ')
	print(ReplaceVariablesList)
	print('')
	'''

	#return
	return map(
		lambda __ReplaceVariable:
		replace(
			_TextVariable,
			__ReplaceVariable,
			_GetterVariable,
			_TranslationVariable
		),
		ReplaceVariablesList
	)

def getStrsListWithBeginStrAndEndStrAndStrsIntAndStr(
		_BeginStr,_EndStr,_StrsInt,_Str,**_KwargVariablesDict):
	
	#set the PickedStrsList
	PickedStrsList=[]
	
	#CountsInt
	if _StrsInt=="All":
		CountsInt=1
	else:
		CountsInt=_StrsInt

	#Scan the Strs
	StrInt=0
	while StrInt<CountsInt:
	
		#Get With the Beginning
		BeginSplittedPickedStr=_Str.split(_BeginStr)
		
		#Check that there is this Flag
		if len(BeginSplittedPickedStr)>1:
		
			#Join the End
			PickedStr=_BeginStr.join(BeginSplittedPickedStr[1:])
			
			#SplittedPickedStr by the EndStr
			EndSplittedPickedStr=PickedStr.split(_EndStr)
			
			#Record if it not the EndStr in the FlagsDict !
			if EndSplittedPickedStr[0]!='",\'EndStr\':"':
			
				#Record the PickedStr
				PickedStrsList.append(EndSplittedPickedStr[0])

			#set the new Str
			_Str=_EndStr.join(EndSplittedPickedStr[1:])

		#Increment
		StrInt+=1

		#Special All Case
		if _StrsInt=="All" and len(BeginSplittedPickedStr)>1:
			StrInt-=1
	
	#Return '' by default
	return PickedStrsList

def sign(_Variable):
	if _Variable<0:
		return -1
	else:
		return 1

def chunk(_LimitStrsList,_TextStr,**_KwargVariablesDict):
	if 'ChunksInt' in _KwargVariablesDict:
		ChunksInt=_KwargVariablesDict['ChunksInt']
	else:
		ChunksInt=1
	return getStrsListWithBeginStrAndEndStrAndStrsIntAndStr(
		_LimitStrsList[0],_LimitStrsList[1],ChunksInt,_TextStr,**_KwargVariablesDict)

def deprefix(_WordStr,_PrefixStr):
	return _PrefixStr.join(_WordStr.split(_PrefixStr)[1:]) if _PrefixStr!="" else _WordStr

def desuffix(_WordStr,_SuffixStr):
	return _SuffixStr.join(_WordStr.split(_SuffixStr)[:-1]) if _SuffixStr!="" else _WordStr

def groupby(_FunctionPointer,_List):
	return getSplitListsListWithSplittedListAndFunctionPointer(_List,_FunctionPointer)

def itemizable(_Variable):
	return hasattr(_Variable,'items') or hasattr(_Variable,'__dict__')

def previous(_PathStr,_SplitStr='/'):

	#split
	WordStrsList=_PathStr.split(_SplitStr)

	#Check
	if len(WordStrsList)>0:
		return _SplitStr.join(WordStrsList[:-1]),WordStrsList[-1]
	else:
		return _SplitStr

def _del(_Variable,_KeyVariable):

	#Check
	if hasattr(_Variable,'__delitem__'):

		#type
		KeyType=type(_KeyVariable)

		#Check
		if (
				hasattr(_Variable,'items') and KeyType==str
			) or KeyType==int:

			#del
			del _Variable[_KeyVariable]

		else:

			KeyInt=unzip(_Variable,[0]).index(_KeyVariable)
			del _Variable[KeyInt]

	#return
	return _Variable

def append(_List,_Variable):
	if _List==None:
		return [_Variable]
	else:
		_List.append(_Variable)
		return _List

def update(_ItemizableVariable,_UpdateVariable):

	#Debug
	"""
	print('l 898 SYS update')
	#print('_ItemizableVariable is ')
	#print(_ItemizableVariable)
	#print('_UpdateVariable is ')
	#print(_UpdateVariable)
	print('')
	"""

	#Check
	if _UpdateVariable==None:
		_UpdateVariable=[]

	#Check
	if hasattr(_ItemizableVariable,'items'):

		#/#################/#
		# Dict cases
		#

		#update
		_ItemizableVariable.update(_UpdateVariable)

	elif getIsTuplesListBool(_ItemizableVariable):

		#/#################/#
		# Tuples list case
		#

		if hasattr(_UpdateVariable,'items'):

			#add
			_ItemizableVariable+=_UpdateVariable.items()

		else:

			#add
			_ItemizableVariable+=_UpdateVariable

	elif type(_ItemizableVariable).__name__=='DataFrame':

		#/#################/#
		# Dataframe cases
		#

		#map
		map(
				lambda __ItemTuple:
				_ItemizableVariable.__setitem__(*__ItemTuple),
				_UpdateVariable.items()
			)

	elif hasattr(_ItemizableVariable,'NameStr'):

		#/#################/#
		# SYS objects cases
		#

		#map set
		_ItemizableVariable['#map@set'](_UpdateVariable)

	elif _ItemizableVariable==None:

		#/#################/#
		# The _ItemizableVariable is directly the update variable
		#

		#Debug
		'''
		print('l 962 SYS update')
		print('_ItemizableVariable is None')
		print('')
		'''
		
		#alias
		_ItemizableVariable=_UpdateVariable

	#Debug
	"""
	print('l 965 SYS update')
	print('in the end')
	#print('_ItemizableVariable is ')
	#print(_ItemizableVariable)
	print('')
	"""

	#return
	return _ItemizableVariable

def complete(_Dict,_CompleteVariable):

	#map
	map(
		lambda __ItemTuple:
		_Dict.__setitem__(
			*__ItemTuple
		) 
		if __ItemTuple[0] not in _Dict
		else None,
		_CompleteVariable.items()
		if hasattr(_CompleteVariable,'items')
		else _CompleteVariable
	)


def get(_Variable,_KeyVariable):

	#/#################/#
	# We get with SYS
	#

	#Check
	if type(_KeyVariable)==str and '.' in _KeyVariable:

		#return reduce
		return reduce(
				lambda __GetterVariable,__GetKeyStr:
				getattr(__GetterVariable,__GetKeyStr),
				[_Variable]+_KeyVariable.split('.')
			)

	#return normal
	return getattr(_Variable,_KeyVariable)

def startswith(_FirstStr,_SecondStr):

	#Debug
	'''
	print('SYS l 1378 startswith ')
	print('_FirstStr is ')
	print(_FirstStr)
	print('_SecondStr is ')
	print(_SecondStr)
	print('')
	'''
	
	#Check
	if type(_FirstStr) in [str,unicode] and type(_SecondStr) in [str,unicode]:

		#return
		return _FirstStr.startswith(_SecondStr)

	else:

		#return
		return False

def endswith(_FirstStr,_SecondStr):

	#Debug
	'''
	print('SYS l 1398 endswith ')
	print('_FirstStr is ')
	print(_FirstStr)
	print('_SecondStr is ')
	print(_SecondStr)
	print('')
	'''

	#Check
	if type(_FirstStr) in [str,unicode] and type(_SecondStr) in [str,unicode]:

		#return
		return _FirstStr.endswith(_SecondStr)
	else:

		#return
		return False

def set(_Variable,_KeyVariable,_ValueVariable):

	#Debug
	'''
	print('We set SYS here l 1457')
	print('_Variable is')
	print(_Variable)
	print('_KeyVariable is ')
	print(_KeyVariable)
	print('')
	'''

	#Check
	if type(_KeyVariable)==str:

		#/#################/#
		# direct set
		#

		#Debug
		'''
		print('setattr direct l 1091')
		print('_KeyVariable is ')
		print(_KeyVariable)
		print("_KeyVariable.startswith('#setattr:')")
		print(_KeyVariable.startswith('#setattr:'))
		print('')
		'''

		#Check
		if _KeyVariable.startswith('#setattr:'):

			#Debug
			'''
			print('setattr direct l 1091')
			print('#setattr:')
			print('')
			'''

			#set
			setattr(
					_Variable,
					deprefix(_KeyVariable,'#setattr:'),
					_ValueVariable
				)

			#return
			return _Variable

		#/#################/#
		# Go deeper maybe
		#

		if '.' in _KeyVariable:

			#split
			SplitStrsList=_KeyVariable.split('.')

			#Debug
			'''
			print('SYS l 1056')
			print('SplitStrsList is ')
			print(SplitStrsList)
			print('')
			'''
			
			#set recursive
			_set(
				getattr(
					_Variable,
					SplitStrsList[0]
				),
				".".join(SplitStrsList[1:]),
				_ValueVariable
			)

			#return
			return 

	#/#################/#
	# Special function with arg calls
	#

	#Check
	if hasattr(_Variable,_KeyVariable):

		#get
		_GetVariable=getattr(_Variable,_KeyVariable)

		#Type
		GetType=type(_GetVariable)

		#Debug
		'''
		print('set l 978')
		print('_GetVariable is ')
		print(_GetVariable)
		print('GetType is ')
		print(GetType)
		print(GetType.__name__)
		print('')
		'''
		
		#Check
		if GetType.__name__ in [
						'instancemethod',
						'builtin_function_or_method',
						'method-wrapper'
					]:

			#Check
			if hasattr(_ValueVariable,'items'):

				#Check
				if '#liarg' not in _ValueVariable:

					#Check
					if '#kwarg' in _ValueVariable:

						#call
						_GetVariable(**_ValueVariable['#kwarg'])

					else:

						#call
						_GetVariable(_ValueVariable)

				else:

					#get
					LiargVariable=_ValueVariable['#liarg']

					#Check
					if '#kwarg' in _ValueVariable:

						#Check
						if LiargVariable==None:

							#call
							_GetVariable(
								**LiargVariable
							)

						else:

							#call
							_GetVariable(
								*LiargVariable,
								**LiargVariable
							)

					else:

						#Check
						if LiargVariable==None:

							#call
							_GetVariable()

						else:

							#call
							_GetVariable(*LiargVariable)

			else:

				#Debug
				'''
				print('set l 1053')
				print('_GetVariable is ')
				print(_GetVariable)
				print('_ValueVariable is ')
				print(_ValueVariable)
				print('')
				'''

				#call
				_GetVariable(*_ValueVariable)

			#return
			return _Variable


	#/#################/#
	# Special __setitem__ call
	#

	#Debug
	'''
	print('l 1079 ')
	print('Check for a __setitem__')
	print("hasattr(_Variable,'__setitem__')")
	print(hasattr(_Variable,'__setitem__'))
	print('')
	'''

	#Check
	if hasattr(_Variable,'__setitem__'):

		#set
		_Variable[_KeyVariable]=_ValueVariable

		#return
		return _Variable

	#/#################/#
	# Special setattr call
	#

	#Debug
	'''
	print('set default l 1091')
	print('_KeyStr')
	print('')
	'''
	
	#set
	setattr(
			_Variable,
			_KeyVariable,
			_ValueVariable
		)

	#return 
	return _Variable
_set=set

def setAttrOrCall(_Variable,_ItemVariable):
	if type(_ItemVariable)==str:
		setattr(_Variable,*_ItemVariable)
	else:
		getattr(_Variable,_ItemVariable)()
	return _Variable

def setRowArray(_SettedArray,_SettingVariable):

	#Debug
	'''
	print('setRowArray l 1840')
	print('Before setting')
	print('_SettedArray is')
	print(_SettedArray)
	print('_SettingVariable is ')
	print(_SettingVariable)
	print('')
	'''

	#set
	_SettedArray[:]=_SettingVariable

	#Debug
	'''
	print('setRowArray l 1846')
	print('After setting')
	print('_SettedArray is')
	print(_SettedArray)
	print('_SettingVariable is ')
	print(_SettingVariable)
	print('')
	'''

	#return
	return _SettedArray

def setMatrixArray(
		_SettedArray,
		_SettingVariable,
		_SetMethod=setRowArray,
		_AxisInt=0
	):

	#import 
	import numpy as np

	#Debug
	'''
	print('setMatrixArray l 1846')
	print('_SettedArray is')
	print(_SettedArray)
	print('_SettingVariable is ')
	print(_SettingVariable)
	print('_SetMethod is ')
	print(_SetMethod)
	print('')
	'''
	
	#type
	SettingType=type(_SettingVariable)

	#Check
	#if SettingType in [int,float,np.float64,complex,np.complex,str,bool]:
	if hasattr(_SettingVariable,'__iter__')==False or type(_SettingVariable)==str:

		#map
		map(
			lambda __IndexInt:
			_SettedArray.__setitem__(
				__IndexInt,
				_SetMethod(
					_SettedArray[__IndexInt],
					_SettingVariable
				)
			),
			xrange(len(_SettedArray))
		)

	else:

		#Check
		if _AxisInt==1:
			_SettedArray=_SettedArray.T
			_SettingVariable=_SettingVariable.T

		#shape
		#SettingShapeIntsTuple=np.shape(_SettingArray)

		#map
		map(
			lambda __IndexInt:
			_SettedArray.__setitem__(
				__IndexInt,
				_SetMethod(
					_SettedArray[__IndexInt],
					_SettingVariable[__IndexInt]
				)
			)
			#if type(_SettingVariable[__IndexInt]) in [
			#	int,float,np.float64,complex,str,bool
			#]
			if hasattr(_SettingVariable[__IndexInt],'__iter__')==False or type(_SettingVariable[__IndexInt])==str 
			else _SettedArray.__setitem__(
				__IndexInt,
				_SetMethod(
					_SettedArray[__IndexInt],
					_SettingVariable[__IndexInt][:]
				)
			),
			xrange(len(_SettedArray))
		)

		#Check
		if _AxisInt==1:
			_SettedArray=_SettedArray.T
			_SettingVariable=_SettingVariable.T

	#return
	return _SettedArray


def getIsTuplesListBool(_TuplesList):

	#Check for list of tuples
	if type(_TuplesList)==list:
		return all(
					map(
							lambda __Tuple:
							type(__Tuple)==tuple,
							_TuplesList
						)
					)

	#Return False either
	return False

def getIsListsListBool(_ListsList):

	#Check for list of list
	if type(_ListsList)==list:
		return all(
					map(
							lambda __List:
							type(__List)==list,
							_ListsList
						)
					)

	#Return False either
	return False

def addSingPlural(_SingularStr,_PluralStr):
	SingularAndPluralTuplesList.append((_SingularStr,_PluralStr))
	SingularStrToPluralStrOrderedDict[_SingularStr]=_PluralStr
	PluralStrToSingularStrOrderedDict[_PluralStr]=_SingularStr

def getSingularStrWithPluralStr(_PluralStr):
	if _PluralStr in PluralStrToSingularStrOrderedDict:
		return  PluralStrToSingularStrOrderedDict[_PluralStr]
	else:
		return _PluralStr[:-1]

def getPluralStrWithSingularStr(_SingularStr):
	if _SingularStr in SingularStrToPluralStrOrderedDict:
		return  SingularStrToPluralStrOrderedDict[_SingularStr]
	else:
		return _SingularStr+'s'

def getIsEqualBool(_VariableA,_VariableB):
		
	#debug
	'''
	print('getIsEqualBool Avant')
	print('_VariableA is',_VariableA)
	print('_VariableB is ',_VariableB)
	print('')
	'''
	
	#import
	import numpy

	#Cast maybe into numpy array before
	if type(_VariableA)==numpy.ndarray and type(_VariableB)==list:
		_VariableB=numpy.array(_VariableB)
	elif type(_VariableB)==numpy.ndarray and type(_VariableA)==list:
		_VariableA=numpy.array(_VariableA)

	#debug
	'''
	print('getIsEqualBool Apres')
	print('_VariableA is',_VariableA)
	print('_VariableB is ',_VariableB)
	print('')
	'''
	
	#Then do the equal process
	if numpy.ndarray not in map(type,[_VariableA,_VariableB]):

		#special unicode case
		if type(_VariableA)==unicode:
			_VariableA=str(_VariableA)
		if type(_VariableB)==unicode:
			_VariableB=str(_VariableB)	

		#return
		return _VariableA==_VariableB

	elif len(_VariableA)!=len(_VariableB):
		
		#return
		return False
		
	else:

		#return
		return all(
					map(
						lambda __ArrayingInt:
						getIsEqualBool(_VariableA[__ArrayingInt],_VariableB[__ArrayingInt]),
						range_(len(_VariableA))
					))

def getIsInListBool(_ContainedVariable,_ContainingList):

	#debug
	'''
	print('getIsInListBool function')
	print('_ContainedVariable is ',_ContainedVariable)
	print('_ContainingList is ',_ContainingList)
	print('')
	'''

	return any(
				map(
					lambda __ListedVariable:
					getIsEqualBool(_ContainedVariable, __ListedVariable),
					_ContainingList
				)
			)

def getSplitListsListWithSplittedListAndFunctionPointer(_SplittedList,_FunctionPointer):

	#Init the SplitListsList
	SplitListsList=[[],[]]

	#do the map with side effect
	map(
			lambda ListedVariable:
			SplitListsList[0].append(ListedVariable) 
			if _FunctionPointer(ListedVariable) 
			else SplitListsList[1].append(ListedVariable),
			_SplittedList
		)

	#Return
	return SplitListsList

def getIndexTuplesList(__SizeTuple):

	#numpy
	import itertools

	#map
	return list(
		itertools.product(*map(xrange,__SizeTuple))
	)

def getUnSerializedTuple(_Variable,_SerializedList):

	#debug
	'''
	print('_SerializedList is ',_SerializedList)
	print('')
	'''
	
	#Return 
	return tuple(
					[
						_SerializedList[0],
						type(_Variable[_SerializedList[0]])(_SerializedList[1])
					]
				)

def getColorTuplesList(
		_FromColorStr='red',
		_ToColorStr='black',
		_SampleInt=5,
		_FormatStr='rgb',
		_PlotBool=True
	):

	#import
	from colour import Color
	
	#color range
	ColorsList=list(
		Color(_FromColorStr).range_to(
			Color(_ToColorStr),
			_SampleInt
		)
	)

	#map
	ColorTuplesList=map(
		lambda __Color:
		getattr(
			__Color,
			_FormatStr
		),
		ColorsList
	)
	
	#Check
	if _PlotBool:
		from matplotlib import pyplot
		pyplot.bar(
				xrange(_SampleInt),
				[1 for __Int in xrange(_SampleInt)],
				color=map(lambda __Color:__Color.rgb,ColorsList)
			)
		pyplot.show()

	#return 
	return ColorTuplesList
	
def getProcessIdStrsListWithProcessNameStr(_ProcessNameStr):

	return map(
				lambda __LineStr:
				__LineStr.split(' ')[3],
				_filter(
					lambda __LineStr:
					'.py' in __LineStr,
					os.popen(
						"ps -ef | grep "+_ProcessNameStr
					).read().split('\n')
				)
			)

def setGUI(*_LiargVariablesList):
	from ShareYourSystem.Standards.Controllers import Systemer

def lib():

	#join
	SetupFilePathStr='/'.join(__file__.split('/')[:-1])+'/lib.py'

	#open
	SetupFile=open(SetupFilePathStr,'r')

	#chunk
	InstalledPackageStr=chunk(
			['packages=[','],'],SetupFile.read()
		)[0]

	#close
	SetupFile.close()
	
	#filter
	InstalledTextStrsList=InstalledPackageStr.split('\n')
	InstalledTextStrListsList=_filter(
		lambda __InstalledChunkList:
		len(__InstalledChunkList)>0,
		map(
				lambda __InstalledTextStr:
				chunk(
					["'ShareYourSystem","',"],
					__InstalledTextStr
				),
				InstalledTextStrsList
		)
	)

	#return
	return map(
		lambda __InstalledTextStrList:
		('ShareYourSystem'+__InstalledTextStrList[0])
		if __InstalledTextStrList[0]!="'"
		else 'ShareYourSystem',
		InstalledTextStrListsList
	)[:-1]

def getKrenelFloatsArray(
		_LevelFloatsTuple=[0,1.],
		_TimeFloatsTuple=[25.,75.],
		_RunTimeFloat=100.,
		_StepTimeFloat=0.1,
	):

	#import
	import numpy as np

	#get the bins
	BinsInt=_RunTimeFloat/_StepTimeFloat

	#init
	KrenelFloatsArray=_LevelFloatsTuple[0]*np.ones(
		BinsInt,
		dtype=type(_LevelFloatsTuple[0])
	)

	#Debug
	'''
	print('getKrenelFloatsArray')
	print('_TimeFloatsTuple[0]/_StepTimeFloat:_TimeFloatsTuple[1]/_StepTimeFloat')
	print(_TimeFloatsTuple[0]/_StepTimeFloat,_TimeFloatsTuple[1]/_StepTimeFloat)
	print('_LevelFloatsTuple[1] is '+str(_LevelFloatsTuple[1]))
	print('')
	'''

	#put the second level
	KrenelFloatsArray[
		int(_TimeFloatsTuple[0]/_StepTimeFloat):int(_TimeFloatsTuple[1]/_StepTimeFloat)
	]=_LevelFloatsTuple[1]

	#return
	return KrenelFloatsArray

def getFourierFloatsArray(
		_RunTimeFloat=100.,
		_StepTimeFloat=0.1,
	):

	#import
	import numpy as np

	#get the bins
	BinsInt=_RunTimeFloat/_StepTimeFloat

	#compute
	FourierFloatsArray=np.array(
		map(
			lambda __TimeFloat:
			sum(
				map(
					lambda __FrequencyFloat,__PhaseFloat: 
					np.cos(2.*np.pi*0.001*__TimeFloat*__FrequencyFloat+__PhaseFloat),
					[200.],
					[np.pi/2.]
				)
			),
			np.arange(0.,_RunTimeFloat,_StepTimeFloat)
		)
	)
	
	#Debug
	'''
	print('getFourierFloatsArray l 86')
	print('FourierFloatsArray is ')
	print(FourierFloatsArray)
	print('')
	'''

	#return
	return FourierFloatsArray

def sort(_SortList):

	#maybe order
	[SortAttributeValueVariablesList,UnSortValueVariablesList]=groupby(
		lambda __Variable:hasattr(
			__Variable,
			'GetSortInt'
		) and __Variable.GetSortInt>-1,
		_SortList
	)

	#maybe order
	[SortItemValueVariablesList,UnSortValueVariablesList]=groupby(
		lambda __Variable:hasattr(
			__Variable,
			'items'
		) and 'GetSortInt' in __Variable and __Variable['GetSortInt']>-1,
		UnSortValueVariablesList
	)

	#Debug
	'''
	print('SYS GetList')
	print('SortItemValueVariablesList is ')
	print(SortItemValueVariablesList)
	print('UnSortValueVariablesList is ')
	print(UnSortValueVariablesList)
	print('order')
	'''
	
	#map
	SortAttributeTuplesList=map(
		lambda __SortAttributeValueVariable:
		(__SortAttributeValueVariable,__SortAttributeValueVariable.GetSortInt),
		SortAttributeValueVariablesList
	)

	#map
	SortItemTuplesList=map(
		lambda __SortItemValueVariable:
		(__SortItemValueVariable,__SortItemValueVariable['GetSortInt']),
		SortItemValueVariablesList
	)

	#Debug
	'''
	print('SYS GetList')
	print('SortAttributeTuplesList is ')
	print(SortAttributeTuplesList)
	print('SortItemTuplesList is ')
	print(SortItemTuplesList)
	print('order')
	'''

	#map
	SortValueVariablesList=map(
		lambda __SortTuple:
		__SortTuple[0],
		sorted(
			SortAttributeTuplesList+SortItemTuplesList,
			key=lambda __Variable:__Variable[1]
		)
	)

	#Debug
	'''
	print('SYS GetList')
	print('order')
	print('SortValueVariablesList is ')
	print(SortValueVariablesList)
	print('UnSortValueVariablesList')
	print(UnSortValueVariablesList)
	print('')
	'''
	
	#return
	return SortValueVariablesList+UnSortValueVariablesList

#/##############/#
# Special Singular and Plural dicts
# 

SingularAndPluralTuplesList=copy.copy(ConceptStrsTuplesList)
SingularStrToPluralStrOrderedDict=dictify(ConceptStrsTuplesList,0,1)
PluralStrToSingularStrOrderedDict=dictify(ConceptStrsTuplesList,1,0)

#/##############/#
# Special derives list and dict classes
# 

class ClassesList(list):

	def __init__(self,_ClassVariable=None):
		
		#call the base 
		list.__init__(self)

		#/#################/#
		# Adapt the shape of the args
		#

		#Check
		if type(_ClassVariable)!=list:

			#Check
			if _ClassVariable==None:

				#/#################/#
				# Give all the mro doer
				#

				#alias
				self.extend(_InstanceVariable.__class__.MroDoerClassesList)

			elif type(_ClassVariable)==str:
				
				#get
				_ClassVariable=getattr(
						sys.modules['ShareYourSystem'],
						getClassStrWithNameStr(_ClassVariable)
				)

				#listify
				self.append(_ClassVariable)

			else:

				#listify
				self.append(_ClassVariable)

		else:

			#map
			_ClassVariable=map(
					lambda __ElementVariable:
					getattr(
						sys.modules['ShareYourSystem'],
						getClassStrWithNameStr(__ElementVariable)
					) if type(__ElementVariable)==str else __ElementVariable,
					_ClassVariable
				)

			#extend
			self.extend(_ClassVariable)


class GetList(list):

	def __init__(self,_ListVariable=None,_GetterVariable=None):
		
		#call the base 
		list.__init__(self)

		#init
		self.ListVariable=_ListVariable
		self.GetterVariable=_GetterVariable

		#Check
		if hasattr(self.GetterVariable,'__getitem__'):
			GetMethod=getattr(
				self.GetterVariable,
				'__getitem__'
			)
		else:
			GetMethod=lambda __KeyVariable:getattr(
				self.GetterVariable,
				__KeyVariable
			) if type(__KeyVariable)==str else __KeyVariable

		#init
		if self.ListVariable==None:
			self.ListVariable=[]

		#Check
		if type(self.ListVariable)!=list:
			
			#debug
			'''
			self.debug(
				[
					'We get nicely',
					('self.',self,['CommandingGetVariable'])
				]
			)
			'''

			#Check
			if self.GetterVariable!=None:

				#get
				ValueVariable=GetMethod(
						self.ListVariable
					)
			else:

				#alias
				ValueVariable=self.ListVariable

			#Check
			if type(ValueVariable)!=list:
				ValueVariable=[ValueVariable]

		else:

			#Check
			if self.GetterVariable!=None:

				#map a get
				ValueVariable=map(
						lambda __ElementVariable:
						GetMethod(__ElementVariable),
						self.ListVariable
					)
			else:

				#alias
				ValueVariable=self.ListVariable

		#Debug
		'''
		print('SYS GetList')
		print('ValueVariable is ')
		print(ValueVariable)
		print('')
		'''

		#flat maybe
		ValueVariablesList=flat(ValueVariable)

		#filterNone
		ValueVariablesList=filterNone(
					ValueVariablesList
				)

		#/####################/#
		# Maybe order
		#

		#sort
		#ValueVariablesList=sort(ValueVariablesList)

		#extend
		self.extend(
			ValueVariablesList
		)

class SetList(list):

	def __init__(self,_ListVariable=None):

		#call the base 
		list.__init__(self)

		#init
		self.ListVariable=_ListVariable

		#init
		if self.ListVariable==None:
			self.ListVariable=[]

		#Check
		if type(self.ListVariable)!=list:
			
			#Check
			if hasattr(self.ListVariable,'items'):

				#items
				self.extend(self.ListVariable.items())

			elif type(self.ListVariable)==tuple and len(self.ListVariable)==2:

				#append the tuple
				self.append(self.ListVariable)

			else:

				#list
				self.append(
					('get',self.ListVariable)
				)

		else:

			#adapt
			self.ListVariable=map(
					lambda __ElementVariable:
					__ElementVariable
					if type(__ElementVariable) in [list,tuple]
					else ('get',__ElementVariable),
					self.ListVariable
				)

			#alias
			self.extend(self.ListVariable.__iter__())

def mapSet(_Variable,_MapVariable):

	#Debug
	'''
	print('mapSet SYS l 1402')
	print('_MapVariable is ')
	print(_MapVariable)
	print('SetList(_MapVariable) is')
	print(SetList(_MapVariable))
	print('')
	'''
	
	#map
	map(
			lambda __ElementVariable:
			_set(
					_Variable,
					__ElementVariable[0],
					__ElementVariable[1]
			),
			SetList(_MapVariable)
		)

	#return 
	return _Variable

class ListDict(collections.OrderedDict):

	def __init__(self,_LiargVariable=None,**_KwargDict):

		#Check
		if _LiargVariable==None:
			_LiargVariable={}

		#call the manage init method
		collections.OrderedDict.__init__(
			self,
			_LiargVariable,
			**_KwargDict
		)

	def getItem(self,_IndexInt):

		#iterkeys
		Iterator=self.iterkeys()
		
		#next
		if _IndexInt==0:
			NextVariable=Iterator.next()
		else:
			NextVariable=map(
				lambda __Int:
				Iterator.next(),
				xrange(_IndexInt+1)
			)[-1]

		return (NextVariable,self[NextVariable])

	def getKey(self,_IndexInt):

		#iterkeys
		if _IndexInt>=0:
			Iterator=self.iterkeys()
			IndexInt=_IndexInt
		else:
			Iterator=reversed(self.keys())
			IndexInt=-_IndexInt
		
		#next
		if _IndexInt==0:

			#next
			NextVariable=Iterator.next()

		else:

			#map
			NextVariable=map(
				lambda __Int:
				Iterator.next(),
				xrange(IndexInt+1)
			)[-1]

		#return
		return NextVariable

	def getValue(self,_IndexInt):

		#iterkeys
		if _IndexInt>=0:
			Iterator=self.iterkeys()
			#DebugIterator=self.iterkeys()
			IndexInt=_IndexInt
		else:
			Iterator=reversed(self.keys())
			#DebugIterator=reversed(self.keys())
			IndexInt=-_IndexInt-1

		#Debug
		'''
		print('getValue l 2385')
		print('_IndexInt is ')
		print(_IndexInt)
		print('IndexInt is ')
		print(IndexInt)
		print('list(DebugIterator) is ')
		print(list(DebugIterator))
		#print('self is ')
		#print(self)
		print('')
		'''

		#next
		if IndexInt==0:

			#next
			NextVariable=Iterator.next()

		else:

			#map
			NextVariable=map(
				lambda __Int:
				Iterator.next(),
				xrange(IndexInt+1)
			)[-1]

		#Debug
		'''
		print('getValue l 2385')
		print('_IndexInt is ')
		print(_IndexInt)
		print('IndexInt is ')
		print(IndexInt)
		print('NextVariable is ')
		print(NextVariable)
		print('')
		'''
		
		#return
		return self[NextVariable]

	def insert(self,
			_IndexInt,
			_ValueVariable,
			_KeyVariable=None,
			_PrefixKeyStr=""
		):

		#get
		KeyVariablesList=self.keys()
		ValueVariablesList=self.values()

		#del
		map(
			lambda __KeyVariable:
			self.__delitem__(
				__KeyVariable
			),
			KeyVariablesList
		)

		#set
		KeyStr=str(_IndexInt) if _KeyVariable==None else _KeyVariable

		#insert
		KeyVariablesList.insert(_IndexInt,KeyStr)
		ValueVariablesList.insert(_IndexInt,_ValueVariable)

		#update
		self.update(
			zip(
					KeyVariablesList,
					ValueVariablesList
				)
		)

		#Check
		if _PrefixKeyStr!="":

			#set
			IndexIntKeyStr=_PrefixKeyStr+"IndexInt"

			#Debug
			'''
			print('IndexIntKeyStr is ')
			print(IndexIntKeyStr)
			print('KeyVariablesList is ')
			print(KeyVariablesList)
			print('')
			'''

			#map
			map(
				lambda __IndexInt:
				_set(
					ValueVariablesList[__IndexInt],
					IndexIntKeyStr,
					__IndexInt
				),
				xrange(len(ValueVariablesList))
			)

		#return
		return self

	def move(self,_OldIndexVariable,_NewIndexInt):

		#get
		if type(_OldIndexVariable)==int:
			TempKeyVariable,TempValueVariable=self.getItem(_OldIndexVariable)
		else:
			TempKeyVariable=_OldIndexVariable
			TempValueVariable=self[TempKeyVariable]
			
		#Debug
		'''
		print('move SYS l 2812')
		print('TempKeyVariable,TempValueVariable')
		print(TempKeyVariable,TempValueVariable)
		print('_NewIndexInt is')
		print(_NewIndexInt)
		print('')
		'''

		#del
		del self[TempKeyVariable]

		#insert
		self.insert(
			_NewIndexInt,
			TempValueVariable,
			_KeyVariable=TempKeyVariable
		)

		#Debug
		'''
		print('self is')
		print(self)
		print('')
		'''
		
		#return
		return self


class MethodDict(collections.OrderedDict):

	def __init__(self,_Class=None):

		#set
		self.Class=_Class

		#init
		collections.OrderedDict.__init__(self)

		#init
		self.MethodKeyStrsList=[]
		self.UnboundMethodsList=[]

		#Check
		if _Class!=None:

			"""
			print(
				"\n".join(
					map(
						lambda __KeyStr:
						str((__KeyStr,type(getattr(_Class,__KeyStr)))),
						dir(_Class)
					)
				)
			)
			"""

			#filter
			self.MethodKeyStrsList=_filter(
				lambda __KeyStr:
				type(
					getattr(
						_Class,
						__KeyStr
					)
				).__name__=='instancemethod',
				dir(_Class)
			)

			#map
			self.UnboundMethodsList=map(
					lambda __MethodKeyStr:
					getattr(_Class,__MethodKeyStr),
					self.MethodKeyStrsList
				)

		#update
		self.update(
			zip(
					self.MethodKeyStrsList,
					self.UnboundMethodsList
				)
		)

class InspectDict(collections.OrderedDict):

	def __init__(self,_Function=None):

		#set
		self.Function=_Function

		#init
		collections.OrderedDict.__init__(self)

		#Check
		if _Function!=None:

			#Unpack
			InputKeyStrList,ArgVariablesListKeyStr,KwargsVariablesSetTagStr,DefaultVariablesList=inspect.getargspec(
				_Function
			)

			#debug
			'''
			print('InputKeyStrList is',InputKeyStrList)
			print('DefaultVariablesList is',DefaultVariablesList)
			print('')
			'''

			#set
			DefaultVariablesList=DefaultVariablesList if DefaultVariablesList!=None else []
		
			#Definition the DefaultIndexInt
			self['DefaultIndexInt']=len(InputKeyStrList)-len(DefaultVariablesList)

			#set the ArgumentOrderedDict
			self.update(
				[
					('InputKeyStrsList',InputKeyStrList),
					('LiargVariablesListKeyStr',ArgVariablesListKeyStr if ArgVariablesListKeyStr!=None else ""),
					('KwargVariablesSetTagStr',KwargsVariablesSetTagStr if KwargsVariablesSetTagStr!=None else ""),
					('DefaultOrderedDict',collections.OrderedDict(
						zip(
							InputKeyStrList[self['DefaultIndexInt']:],
							DefaultVariablesList
							)
						)
					),
					('FunctionNameStr',_Function.__name__)
				]
			)


def getExtremumFloat(_Variable,_MinOrMaxStr='min'):

	#import numpy
	import numpy as np

	#Debug
	'''
	print('SYS l 2518')
	print('np.shape(_Variable) is ')
	print(np.shape(_Variable))
	print('_MinOrMaxStr is '+_MinOrMaxStr)
	print('len(_Variable)>0 is ')
	print(len(_Variable)>0)
	print('')
	'''

	#Check
	if np.shape(_Variable)[-1]>0:

		#Debug
		'''
		print('We get the min or max')
		print('_Variable[0] is ')
		print(_Variable[0])
		print('')
		'''

		#get
		ExtremumFloat=getattr(
			np.array(_Variable),
			_MinOrMaxStr
		)()

	else:

		#set
		ExtremumFloat=-0.00000000001 if _MinOrMaxStr=='min' else 0.000000000001

	#Debug
	'''
	print('ExtremumFloat is ')
	print(ExtremumFloat)
	print('')	
	'''
	
	#return
	return ExtremumFloat

def getTickFloatsArray(_LimList,_SampleFloat):

	#import
	import numpy as np

	#Debug
	'''
	print('SYS l 2517')
	print('getTickFloatsArray l 64')
	print('_LimList is')
	print(_LimList)
	print('_SampleFloat is ')
	print(_SampleFloat)
	print('')
	'''
	
	#Check
	LimList=[
		_LimList[0] if np.isnan(_LimList[0])==False else -10.,
		_LimList[1] if np.isnan(_LimList[1])==False else 10.
	]
	
	#return
	TickFloatsArray=np.array(
		list(
			np.arange(
				LimList[0],
				LimList[1],
				(LimList[1]-LimList[0])/float(_SampleFloat)
			)
		)+[LimList[1]]
	)

	#Debug
	'''
	print('TickFloatsArray l 2536')
	print('TickFloatsArray is')
	print(TickFloatsArray)
	print('')
	'''

	#return 
	return TickFloatsArray

def getTickIntsArray(_LimList,_SampleInt):

	#import
	import numpy

	#max
	MinInt=max(0,int(_LimList[0]))

	#Debug
	'''
	print('SYS l 2517')
	print('getTickIntsArray l 64')
	print('_LimList is')
	print(_LimList)
	print('_SampleInt is ')
	print(_SampleInt)
	print('int(_LimList[1]-MinInt)/_SampleInt is')
	print(int(_LimList[1]-MinInt)/_SampleInt)
	print('')
	'''
	
	#set
	StepInt=int(_LimList[1]-MinInt)/_SampleInt
	if StepInt==0:
		StepInt=1

	#return
	TickIntsArray=numpy.array(
		range(
				MinInt,
				int(_LimList[1]),
				StepInt
			)+[int(_LimList[1])]
	)

	#Debug
	'''
	print('TickIntsArray l 2536')
	print('TickIntsArray is')
	print(TickIntsArray)
	print('')
	'''

	#return 
	return TickIntsArray

def getIsNullBool(_NullVariable):

	#import
	import numpy as np

	#type
	NullVariableType=type(_NullVariable)

	#Check
	if NullVariableType==np.ndarray:

		#return
		return _NullVariable.all()==0

	#return
	return _NullVariable==0

def getFloatStr(_Float):

	#Debug
	'''
	print('SYS l 2552')
	print('_Float is')
	print(_Float)
	print('')
	'''

	#Check
	if _Float==0.:

		#return
		FloatStr='0'

	else:

		#Check
		if abs(_Float)>1.:

			#format
			FloatStr='%.2f'%_Float

			#remove 0 on the right
			while FloatStr[-1]=='0':
				FloatStr=FloatStr[:-1]

		elif abs(_Float)<0.000000001:

			#return
			FloatStr='0'

		else:

			#str
			#FloatStr=str(_Float)
			FloatStr='%.10f'%_Float

			#Debug
			'''
			print('SYS l 2576')
			print('FloatStr is')
			print(FloatStr)
			print('')
			'''

			#Check
			if FloatStr[0]=='-':
				DecimalFloatStr=FloatStr[1:]
			else:
				DecimalFloatStr=FloatStr

			#index
			DecimalInt=map(
				lambda __Str:
				__Str not in '0' and __Str!='.',
				DecimalFloatStr
			).index(True)

			#Debug
			'''
			print('DecimalInt is')
			print(DecimalInt)
			print('')
			'''

			#get
			if FloatStr[0]=='-':
				FloatStr='-'+DecimalFloatStr[:DecimalInt+2]
			else:
				FloatStr=DecimalFloatStr[:DecimalInt+2]

			#Debug
			'''
			print('FloatStr is')
			print(FloatStr)
			print('')
			'''

			#remove 0 on the right
			while FloatStr[-1]=='0':
				FloatStr=FloatStr[:-1]

	#Debug
	'''
	print('SYS l 2612')
	print('FloatStr is')
	print(FloatStr)
	print('')
	'''

	#return
	return FloatStr

def argmax(_Array):

	#import
	import numpy as np
	from scipy.signal import argrelextrema

	#Maxima
	return argrelextrema(
		_Array, 
		np.greater
	)[0]

def getInverseFunction(_Function,_SeedVariable=0.,_ArrayBool=False):

	#import
	import scipy.optimize

	#define
	if _ArrayBool:
		def getRootFloat(_SearchVariable,_TargetVariable):
			return _Function(_SearchVariable)-_TargetVariable
	else:
		def getRootFloat(_SearchVariable,_TargetVariable):
			return _Function(_SearchVariable[0])-_TargetVariable[0]

	#return
	return lambda __Variable:scipy.optimize.fsolve(
		getRootFloat,
		_SeedVariable,
		args=[__Variable]
	)[0]
#</DefineLocals>

#<DefineClass>
class ShareYourSystem():

	def __init__(self,_WrapModule):

		#Bind the Module
		self.__dict__['WrapModule']=_WrapModule

		#Get the library ref
		_WrapModule.ModuleStrsList=lib()
		_WrapModule.NameStrsList=map(
			lambda __ModuleStr:
			__ModuleStr.split('.')[-1],
			_WrapModule.ModuleStrsList
		)
		_WrapModule.ClassStrsList=map(getClassStrWithNameStr,_WrapModule.NameStrsList)

		#figure
		_WrapModule.Figure=None
		_WrapModule.Axes=None

	def __setattr__(self,_KeyVariable,_ValueVariable):
		
		'''
		#Give it the IdInt
		if hasattr(_ValueVariable,'IdInt'):
			_ValueVariable.IdInt=id(_ValueVariable)
			_ValueVariable.SysStr=_KeyVariable

		#set
		self.__dict__[_KeyVariable]=_ValueVariable
		'''

		#Give it to the Module
		setattr(
					self.__dict__['WrapModule'],
					_KeyVariable,
					_ValueVariable
			)

	def __getattr__(self,_KeyVariable):

		#alias
		WrapModule=self.__dict__['WrapModule']

		#VERY pretentious way of accessing 
		#numpy, matplotlib operator functions as if it was in the SYS library...
		#(but it's then simpler as the pylab module)
		if _KeyVariable=='array':

			#import
			import numpy
			return numpy.array

		elif _KeyVariable=='contains':

			#return
			return operator.contains

		elif _KeyVariable in ['plot','show']:

			#import
			from matplotlib import pyplot

			#Check
			if _KeyVariable=='plot':

				#Check
				if type(WrapModule.Figure) == None.__class__:
					WrapModule.Figure=pyplot.figure()
					WrapModule.Axes=None

				#Check
				if type(WrapModule.Axes) == None.__class__:
					WrapModule.Axes=pyplot.axes()
					WrapModule.Axes._figure=WrapModule.Figure

				#return
				return WrapModule.Axes.plot

			else:

				#return
				return getattr(
						pyplot,
						_KeyVariable
					)

		elif _KeyVariable in ["plot3D","scatter3D"]:

			#Check
			if type(WrapModule.Figure) == None.__class__:
				
				#import
				from matplotlib import pyplot
				WrapModule.Figure=pyplot.figure()
				WrapModule.Axes=None

			#Check
			if type(WrapModule.Axes) == None.__class__:

				#import
				from mpl_toolkits.mplot3d import Axes3D

				#define
				class NewAxes3D(Axes3D):
					def set_xlabel(self,*args,**kwargs):
						Axes3D.set_xlabel(self,*args,**kwargs)
						return self
					def set_ylabel(self,*args,**kwargs):
						Axes3D.set_ylabel(self,*args,**kwargs)
						return self
					def set_zlabel(self,*args,**kwargs):
						Axes3D.set_zlabel(self,*args,**kwargs)
						return self

				WrapModule.Axes = NewAxes3D(WrapModule.Figure)

			#define
			def localPlot(*args,**kwargs):
				getattr(WrapModule.Axes,desuffix(_KeyVariable,"3D"))(*args,**kwargs)
				return WrapModule

			#return
			return localPlot

		#Check for maybe automatically importing submodules
		if hasattr(WrapModule,_KeyVariable)==False:

			#Debug
			'''
			print('SYS l. 889')
			print('SYS has not this _KeyVariable')
			print('_KeyVariable is ',_KeyVariable)
			print('')
			'''

			#Check for special methods
			if _KeyVariable in ['_print','_str']:
				from ShareYourSystem.Standards.Interfacers import Printer
				return getattr(WrapModule,_KeyVariable)

			#Check
			if _KeyVariable.endswith('Class'):

				#Debug
				'''
				print('SYS l. 898')
				print('it looks like a class')
				print('')
				'''

				#try
				try:

					#get
					ValueModuleStr=WrapModule.ModuleStrsList[
							WrapModule.ClassStrsList.index(_KeyVariable)
						]

					#Debug
					'''
					print('SYS l. 948')
					print('ValueModuleStr is '+ValueModuleStr)
					print('')
					'''
					
					#import
					ValueModule=importlib.import_module(ValueModuleStr)

					#return
					return getattr(ValueModule,_KeyVariable)

				except:
					
					#print
					'''
					print('l 941 SYS')
					print('No _KeyVariable like')
					print(_KeyVariable)
					print('')
					'''

					#raise
					raise AttributeError

			#Check for a SYS module call
			else:

				#try
				try:

					#get
					ValueModuleStr=WrapModule.ModuleStrsList[
							WrapModule.NameStrsList.index(_KeyVariable)
						]

					#import
					ValueModule=importlib.import_module(ValueModuleStr)

					#return
					return ValueModule

				except:

					#Check for a non SYS module call
					try:

						#import
						ValueModule=importlib.import_module(_KeyVariable)

						#return
						return ValueModule

					except:

						#print
						'''
						print('l 1050 SYS')
						print('No _KeyVariable like')
						print(_KeyVariable)
						print('WrapModule.NameStrsList is ')
						print(WrapModule.NameStrsList)
						print('WrapModule.ModuleStrsList is ')
						print(WrapModule.ModuleStrsList)
						'''

						#raise
						raise AttributeError
						
		else:

			#return 
			return getattr(WrapModule,_KeyVariable)

#set
sys.modules[__name__]=ShareYourSystem(sys.modules[__name__])
#</DefineClass>




