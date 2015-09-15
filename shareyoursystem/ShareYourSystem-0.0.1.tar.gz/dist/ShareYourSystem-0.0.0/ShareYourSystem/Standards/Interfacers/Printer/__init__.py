# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Printer is an object that can directly print 
Strs in the Printer context.

"""


#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Interfacer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Doer"
SYS.setSubModule(globals())
SYS.addDo('Printer','_Print','Printing','Printed')
#</DefineAugmentation>

#<ImportSpecificModules>
import copy
#</ImportSpecificModules>

#<DefineLocals>
PrintDictIndentStr="  "
PrintListIndentStr="  "
PrintIndentStr="   /"
PrintEofStr="\n"
PrintIdBool=True
PrintCircularStr="{...}"
PrintAlineaStr=""
PrintAlreadyIdIntsList=[]

def getNumpyArrayStr(_NumpyArray):

	#Definition the ShapeList
	ShapeList=list(numpy.shape(_NumpyArray))

	#debug
	'''
	print('Printer l.25 : getNumpyArrayStr')
	print('ShapeList is',ShapeList)
	print('')
	'''

	#Return the array directly if it is small or either a short represented version of it
	if (len(ShapeList)==1 and ShapeList[0]<3) or (len(ShapeList)>1 and ShapeList[1]<3):
		return str(_NumpyArray)
	return "<numpy.ndarray shape "+str(ShapeList)+">" 
											
def getPointerStr(_Variable,**_KwargVariablesDict):

	#Debug
	'''
	print('Printer l.39 : getPointerStr')
	print('')
	'''

	#Define
	if hasattr(_Variable,'PrintingInfoStr'):
		InfoStr=_Variable.PrintingInfoStr
	else:
		InfoStr=_KwargVariablesDict['InfoStr'] if 'InfoStr' in _KwargVariablesDict else ""
	
	#Debug
	'''
	print('Printer l.71 : InfoStr')
	print('InfoStr is ')
	print(InfoStr)
	print('')
	'''
	
	#set in the _KwargVariablesDict
	if 'PrintDeepInt' not in _KwargVariablesDict:
		_KwargVariablesDict['PrintDeepInt']=0

	#Definition the Local alinea
	PrintLocalAlineaStr=PrintAlineaStr if _KwargVariablesDict['PrintDeepInt']==0 else ""

	#Define
	if type(_Variable).__name__=='Database':
		PrintedVariableStr=_Variable._Database__name
	elif type(_Variable).__name__=='Collection':
		PrintedVariableStr=_Variable._Collection__name
	else:
		PrintedVariableStr=_Variable.__name__ if hasattr(_Variable,__name__) else ""

	#Debug
	'''
	print('l 85 Printer')
	print('type(_Variable).__name__ is ')
	print(type(_Variable).__name__)
	print('PrintedVariableStr is ')
	print(PrintedVariableStr)
	print('')
	'''

	#set
	PrintIdInt=_Variable.PrintIdInt if hasattr(
		_Variable,'PrintIdInt'
	) else id(_Variable)

	#init
	PointerStr=PrintLocalAlineaStr+"<"+PrintedVariableStr+" ("+_Variable.__class__.__name__

	#Check
	if PrintIdBool:
		PointerStr+="), "+str(PrintIdInt)
	else:
		PointerStr+=")"

	#add
	PointerStr+=InfoStr+" >"

	#return
	return PointerStr

def getDictStr(
	_DictatedVariable,**_KwargVariablesDict
	):
	
	#set in the _KwargVariablesDict
	if 'PrintDeepInt' not in _KwargVariablesDict:
		_KwargVariablesDict['PrintDeepInt']=0

	#debug
	'''
	print('Printer l.59 : getDictStr')
	print('_KwargVariablesDict is ',str(_KwargVariablesDict))
	print('')
	'''

	#Global
	global PrintAlineaStr

	#Definition the LocalPrintAlineaStr
	LocalPrintAlineaStr=PrintAlineaStr+"".join(
		[PrintIndentStr]*(_KwargVariablesDict['PrintDeepInt']))

	#Init the DictStr
	DictStr="\n"+LocalPrintAlineaStr+"{ "

	#Scan the Items (integrativ loop)
	if type(_DictatedVariable)!=dict and hasattr(
		_DictatedVariable,"items"
	):
		
		#debug
		'''
		print('l 135 Printer')
		print('_DictatedVariable is ')
		print(_DictatedVariable)
		print('type(_DictatedVariable) is ')
		print(type(_DictatedVariable))
		print('')
		'''
		
		#items
		PrintTuplesList=_DictatedVariable.items()

	else:

		#sort
		PrintTuplesList=sorted(
			_DictatedVariable.iteritems(), key=lambda key_value: key_value[0]
		)

	#Integrativ loop for seriaizing the items
	for __PrintKeyStr,__PrintValueVariable in PrintTuplesList:
	
		#debug
		'''
		print('Printer l.127')
		print('__PrintKeyStr is',__PrintKeyStr)
		print('')
		'''

		#set the begin of the line
		DictStr+="\n"+LocalPrintAlineaStr+PrintDictIndentStr

		#Force the cast into Str
		if type(__PrintKeyStr) not in [unicode,str]:
			__PrintKeyStr=str(__PrintKeyStr)

		#Get the WordStrsList
		WordStrsList=SYS.getWordStrsListWithStr(__PrintKeyStr)

		#Init the PrintValueVariableStr
		PrintValueVariableStr="None"

		#Split the case if it is a pointing variable or not
		if len(WordStrsList)>0:

			#Value is displayed
			"""
			if SYS.getWordStrsListWithStr(__PrintKeyStr)[-1]=="Pointer":
			
				#Pointer Case
				PrintValueVariableStr=getPointerStr(
												__PrintValueVariable,
												**_KwargVariablesDict
											)
			"""
			"""						
			elif ''.join(SYS.getWordStrsListWithStr(__PrintKeyStr)[-2:])=="PointersList":
			
				#debug
				'''
				print('__PrintValueVariable is ',__PrintValueVariable)
				print('')
				'''

				#Pointer Case
				PrintValueVariableStr=str(
						map(
								lambda List:
								getPointerStr(
									List,
									**_KwargVariablesDict),
								__PrintValueVariable
							)
						)  if type(__PrintValueVariable)==list else "None"
			"""
			
		#Special Suffix Cases
		if PrintValueVariableStr=="None":
				
			#debug
			'''
			print('go to represent')
			print('__PrintKeyStr is ',__PrintKeyStr)
			print('id(__PrintValueVariable) is ',id(__PrintValueVariable))
			print('')
			'''

			#Other Cases
			PrintValueVariableStr=getPrintStr(
				__PrintValueVariable,
				**_KwargVariablesDict
			)

		#Key and Value Case
		DictStr+="'"+__PrintKeyStr+"' : "+PrintValueVariableStr

	#Add a last line
	DictStr+="\n"+LocalPrintAlineaStr+"}"

	#debug
	'''
	print('DictStr is ',DictStr)
	print('')
	'''

	#return the DictStr
	return DictStr

def getListStr(_List,**_KwargVariablesDict):	

	#Global
	global PrintAlineaStr

	#set in the _KwargVariablesDict
	if 'PrintDeepInt' not in _KwargVariablesDict:
		_KwargVariablesDict['PrintDeepInt']=0

	#debug
	'''
	print('Printer l.166 : getListStr')
	print('_KwargVariablesDict is ',str(_KwargVariablesDict))
	print('_List is '+str(_List))
	print('')
	'''

	#Init the DictStr
	if type(_List)==list:
		BeginBracketStr='['
		EndBracketStr=']'
	else:
		BeginBracketStr='('
		EndBracketStr=')'

	#Definition the LocalPrintAlineaStr
	LocalPrintAlineaStr=PrintAlineaStr+"".join(
		[PrintIndentStr]*(_KwargVariablesDict['PrintDeepInt']))

	#Do the first Jump
	ListStr="\n"+LocalPrintAlineaStr+BeginBracketStr
	
	#Scan the Items (integrativ loop)
	for ListInt,List in enumerate(_List):
	
		#set the begin of the line
		ListStr+="\n"+LocalPrintAlineaStr+PrintListIndentStr

		#Get the represented version
		PrintValueVariableStr=getPrintStr(
				List,**dict(
					_KwargVariablesDict,
					**{'PrintingAlineaIsBool':False}
				)
			)
			
		#Key and Value Case
		ListStr+=str(ListInt)+" : "+PrintValueVariableStr

	#Add a last line
	ListStr+="\n"+LocalPrintAlineaStr+EndBracketStr

	#return the DictStr
	return ListStr

def getPrintStr(_Variable,**_KwargVariablesDict):

	#Define global
	global PrintAlreadyIdIntsList

	#set in the _KwargVariablesDict
	if 'PrintDeepInt' not in _KwargVariablesDict:
		_KwargVariablesDict['PrintDeepInt']=0

	#debug
	'''
	print('Printer l.213 : getPrintStr')
	#print('_KwargVariablesDict is ',str(_KwargVariablesDict))
	print('_Variable is '+str(_Variable))	
	#print('type(_Variable) is '+str(type(_Variable)))
	#print("hasattr(_Variable,'__repr__') is "+str(hasattr(_Variable,"__repr__")))
	##if hasattr(_Variable,"__repr__"):
	#	print('hasattr(_Variable.__class__,"InspectedOrderedDict") is '+str(
	#		hasattr(_Variable.__class__,"InspectedOrderedDict")))
	#	if hasattr(_Variable.__class__,"InspectedOrderedDict"):
	#		print("_Variable.__class__.InspectedOrderedDict['__repr__']['KwargVariablesListKeyStr'] is "+str(
	#			_Variable.__class__.InspectedOrderedDict['__repr__']['KwargVariablesListKeyStr']))	
	#		print(_Variable.__class__.InspectedOrderedDict['__repr__']['KwargVariablesListKeyStr'])
	print('')
	'''
	
	#None type
	if type(_Variable)==None.__class__:
		return "None"

	#Special mongo database case
	elif type(_Variable).__name__ in ["Database","Series","Collection"]:

		#get
		PrinterStr=getPointerStr(_Variable)

		#return
		return PrinterStr

	#Dict types print
	#if type(_Variable) in [dict,collections.OrderedDict]:
	elif hasattr(_Variable,'items') and type(_Variable)!=type:

		#Increment the deep
		_KwargVariablesDict['PrintDeepInt']+=1

		#debug
		'''
		print('This is a dictated type so get a represent like a dict')
		print('')
		'''

		#id
		PrintIdInt=id(_Variable)

		#debug
		'''
		print('PrintIdInt is ',PrintIdInt)
		print('PrintAlreadyIdIntsList is ',PrintAlreadyIdIntsList)
		print('')
		'''

		#Check if it was already represented
		if PrintIdInt not in PrintAlreadyIdIntsList:

			#Debug
			'''
			print('PrintAlreadyIdIntsList is ',PrintAlreadyIdIntsList)
			print('')
			'''

			#append
			PrintAlreadyIdIntsList.append(PrintIdInt)

			#Return the repr of the _Variable but shifted with the PrintAlineaStr
			PrintStr=getDictStr(
						_Variable,
						**_KwargVariablesDict
			)

		else:

			#Return the circular Str
			PrintStr=PrintCircularStr+getPointerStr(_Variable,**_KwargVariablesDict)

		#Debug
		'''
		print('PrintIdInt is ',PrintIdInt)
		print('PrintStr is ',PrintStr)
		print('')
		'''
		
		#return 
		return PrintStr

	#List types print
	elif type(_Variable) in [list,tuple]:

		#id
		PrintIdInt=id(_Variable)

		#Check if it was already represented
		if PrintIdInt not in PrintAlreadyIdIntsList:

			#debug
			'''
			print('Printer l 389')
			print('This is a listed type so get a represent like a list')
			print('_Variable is ')
			print(_Variable)
			print('map(type,_Variable) is ')
			print(map(type,_Variable))
			print('')
			'''
			
			#append
			PrintAlreadyIdIntsList.append(PrintIdInt)

			#import numpy
			import numpy
			from pandas.core import series

			#Check if it is a List of Objects or Python Types
			if all(
					map(
						lambda __ElementVariable:
						type(__ElementVariable) in [
							float,int,str,unicode,numpy.float64,
						] or type(__ElementVariable)==None.__class__,
						_Variable
						)
				)==False:

				#Increment the deep
				_KwargVariablesDict['PrintDeepInt']+=1

				#debug
				'''
				print('Print a represented version of the list')
				print('')
				'''

				#Return 
				PrintStr=getListStr(_Variable,**_KwargVariablesDict)

			else:

				#debug
				'''
				print('Here just print the list directly')
				print('')
				'''

				#Definition the Local alinea
				PrintLocalAlineaStr=PrintAlineaStr if _KwargVariablesDict['PrintDeepInt']==0 else ""

				#Return 
				PrintStr=PrintLocalAlineaStr+repr(
					_Variable).replace("\n","\n"+PrintLocalAlineaStr)


			#return 
			return PrintStr

		else:

			#Return the circular Str
			return PrintCircularStr+getPointerStr(_Variable,**_KwargVariablesDict)

	#Instance print
	elif type(_Variable).__name__ in ["instancemethod"]:

		#Debug
		'''
		print('Printer l 421')
		print('This is a method ')
		print('_Variable.__name__ is ',_Variable.__name__)
		print('')
		'''

		#Definition the Local alinea
		PrintLocalAlineaStr=PrintAlineaStr if _KwargVariablesDict['PrintDeepInt']==0 else ""
		
		#append
		PrintAlreadyIdIntsList.append(_Variable.im_self)

		#return PrintAlineaStr+"instancemethod"
		PrintStr=PrintLocalAlineaStr
		PrintStr+="< bound method "+_Variable.__name__
		PrintStr+=" of "+str(_Variable.im_self.__class__)
		PrintStr+=" "+str(id(_Variable.im_self))+" >"
		#PrintStr='inst'

		#return
		return PrintStr

	#Str types
	elif type(_Variable) in SYS.StrTypesList:

		#debug
		'''
		print('This is a Str type so get a represent like a Str')
		print('')
		'''

		#Definition the Local alinea
		PrintLocalAlineaStr=PrintAlineaStr if _KwargVariablesDict['PrintDeepInt']==0 else ""

		#Return
		return PrintLocalAlineaStr+_Variable.replace("\n","\n"+PrintLocalAlineaStr)

	#Other
	#elif hasattr(_Variable,"__repr__") and hasattr(
	#	_Variable.__class__,"InspectInspectDict"
	#	) and '__repr__' in _Variable.__class__.InspectInspectDict and _Variable.__class__.InspectInspectDict[
	#	'__repr__']['KwargVariablesListKeyStr']!="":
	elif hasattr(_Variable.__class__,'__mro__'
		) and SYS.PrinterClass in _Variable.__class__.__mro__:

		#debug
		'''
		print('This is a representer so call the repr of it with the _KwargVariablesDict')
		print('type(_Variable) is ',type(_Variable))
		print('id(_Variable) is ',id(_Variable))
		print('')
		'''
		
		#/################/#
		# id CAREFULL !!!! THIS the id from the original object...
		# ...not the copy ones either there are possibilities of circular print calls

		#get
		PrintIdInt=_Variable.PrintIdInt

		#Check if it was already represented
		if PrintIdInt not in PrintAlreadyIdIntsList:

			#append
			PrintAlreadyIdIntsList.append(PrintIdInt)

			#Return the repr of the _Variable but shifted with the PrintAlineaStr
			PrintStr=_Variable.__repr__(**_KwargVariablesDict)

			#return 
			return PrintStr

		else:

			#Return the circular Str
			return PrintCircularStr+getPointerStr(_Variable,**_KwargVariablesDict)

	else:

		#Debug
		'''
		print('This is not identified so call the repr of it')
		print('')
		'''

		#Definition the Local alinea
		PrintLocalAlineaStr=PrintAlineaStr if _KwargVariablesDict[
			'PrintDeepInt']==0 else ""

		#Define 
		PrintIdInt=id(_Variable)

		#Debug
		'''
		print('PrintIdInt is ',PrintIdInt)
		print('PrintAlreadyIdIntsList is ',PrintAlreadyIdIntsList)
		print('')
		'''

		#Check if it was already represented
		if PrintIdInt not in PrintAlreadyIdIntsList:

			#debug
			'''
			print('Printer l 594')
			print('type(_Variable) is ',type(_Variable))
			print('')
			'''
			
			#Append but only for mutables variable
			if type(_Variable) not in [bool,str,int,float]:
				PrintAlreadyIdIntsList.append(PrintIdInt)

			else:

				#debug
				'''
				print('_Variable is ',_Variable)
				print('')
				'''
				pass

			#Return a repr of the _Variable but shifted with the PrintAlineaStr
			PrintStr=PrintLocalAlineaStr+repr(_Variable).replace(
										"\n",
										"\n"+PrintLocalAlineaStr+"".join(
											[
												PrintIndentStr
											]*2
										)
									)

			#return 
			return PrintStr


		else:

			#Return the circular Str
			return PrintLocalAlineaStr+PrintCircularStr+getPointerStr(
				_Variable,**_KwargVariablesDict)

def _print(_Variable,**_KwargVariablesDict):
	print(represent(_Variable,**_KwargVariablesDict))

def represent(_Variable,**_KwargVariablesDict):

	#Definition the global
	global PrintAlineaStr,PrintAlreadyIdIntsList

	#Debug
	'''
	print('Printer l.545')
	print('Reinit the PrintAlreadyIdIntsList')
	print('')
	'''

	#Reinit
	PrintAlreadyIdIntsList=[]

	#Debug
	'''
	print('Printer l.554')
	print('_KwargVariablesDict is ',_KwargVariablesDict)
	print('')
	'''
	
	#Represent without shifting the Strs or not
	if 'PrintingAlineaIsBool' not in _KwargVariablesDict or _KwargVariablesDict['PrintingAlineaIsBool']:
		return getPrintStr(_Variable,**_KwargVariablesDict)
	else:
		PrintedOldAlineaStr=PrintAlineaStr
		PrintAlineaStr=""
		PrintStr=getPrintStr(_Variable,**_KwargVariablesDict)
		PrintAlineaStr=PrintedOldAlineaStr
		return PrintStr

def __main__represent(_PrintStr,**_KwargVariablesDict):
	return represent(
		_PrintStr,
		**dict(_KwargVariablesDict,**{'PrintingAlineaIsBool':False})
	)
def __main__print(_PrintStr,**_KwargVariablesDict):
	return _print(
		_PrintStr,
		**dict(_KwargVariablesDict,**{'PrintingAlineaIsBool':False})
	)
SYS._str = __main__represent
SYS._print = __main__print
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PrinterClass(BaseClass):

	def default_init(self,
						_PrintIdInt=0,
						_PrintStr="",
						_PrintingCopyVariable=None,
						_PrintingInstanceSkipKeyStrsList=None,
						_PrintingInstanceForceKeyStrsList=None,
						_PrintingClassSkipKeyStrsList=[],
						_PrintingClassForceKeyStrsList=[],
						_PrintingBaseBool=True,
						_PrintingNewInstanceBool=True,
						_PrintingNewClassBool=True,
						_PrintingOutBool=True,
						_PrintingSelfBool=False,
						_PrintingInfoStr="",
						_PrintingInstanceForceBaseKeyStrsList=None,
						**_KwargVariablesDict
					):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#id
		self.PrintIdInt=id(self)

		#init
		self.PrintingInstanceSkipKeyStrsList=[]
		self.PrintingInstanceForceKeyStrsList=[]
			
	def do__print(self,**_KwargVariablesDict):

		#Debug
		'''
		print('l 680 _print')
		#print('_KwargVariablesDict is ')
		#print(_KwargVariablesDict)
		print('self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList is ')
		print(self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList)
		print('')
		'''
		
		#/###################/#
		# Check if it is a ReprStr
		# or just a PrintStr

		#Check 
		if self.PrintingSelfBool:

			#Debug
			'''
			print('l 693')
			print('we repr str here')
			print('')
			'''
			
			#print
			self.PrintStr=self.PrintingCopyVariable.getReprStr(
				**_KwargVariablesDict
			)

		else:

			#Debug
			'''
			print('l 705')
			print('we just get print Str here')
			print('')
			'''

			#print
			self.PrintStr=getPrintStr(
					self.PrintingCopyVariable,
					**_KwargVariablesDict
				)
		
		#Check
		if self.PrintingOutBool:
			print(self.PrintStr)

	def __repr__(self,**_KwargVariablesDict):

		#Debug
		'''
		print('l 718 __repr__')
		print('_KwargVariablesDict is ')
		print(_KwargVariablesDict)
		print('')
		'''

		#init a new one
		self.PrintingCopyVariable=self.__class__()

		#loop
		for __ItemTuple in self.__dict__.items():

			#Debug
			'''
			print('Try to copy')
			print(__ItemTuple[0])
			print('')
			'''

			#Check
			if type(__ItemTuple[1]).__name__ not in ['Figure']:

				#Debug
				'''
				print('Ok this is not an annoying type like pyplot Figure')
				print('try a copy')
				print('')
				'''

				#try
				try:

					#copy
					self.PrintingCopyVariable.__dict__[__ItemTuple[0]]=copy.copy(
						__ItemTuple[1]
					)
				except:


					#debug
					#print('Try to copy but FAILED')
					#print(__ItemTuple[0])
					#print('')

					#pass
					pass

			else:

				#Debug
				'''
				print('Ok this is like a pyplot figure... just alias')
				print('')
				'''
				
				#copy
				self.PrintingCopyVariable.__dict__[__ItemTuple[0]]=__ItemTuple[1]
				

		#Debug
		'''
		print('l 764 OK')
		print('type(self.PrintingCopyVariable) is ')
		print(type(self.PrintingCopyVariable))
		print('')
		'''

		#get
		ReprStr=self._print(
			self.PrintingCopyVariable,
			_OutBool=False,
			_SelfBool=True,
			**_KwargVariablesDict
		).PrintStr

		#Debug
		'''
		print('l 763 Printer')
		print('ReprStr is ')
		print(ReprStr)
		'''

		#reset
		self.PrintingSelfBool=False
		self.PrintingOutBool=True

		#return 
		return ReprStr

	def getReprStr(self,**_KwargVariablesDict):

		#Debug
		'''
		print('l 741 getReprStr')
		print('_KwargVariablesDict is ')
		print(_KwargVariablesDict)
		print('')
		'''

		#debug
		'''
		_Variable.debug(('_Variable.__class__',self.__class__,[
				'PrintingKeyStrsList',
				'DefaultBaseKeyStrsList',
				'DefaultSpecificKeyStrsList',
				'PrintedNotSpecificKeyStrsList'
				]))
		'''

		#/###################/#
		# Print the Default Key Strs... form the Instance or the still the Class
		#

		#Debug
		'''
		print('Printer l 846')
		print('self.PrintingInstanceSkipKeyStrsList is ')
		print(self.PrintingInstanceSkipKeyStrsList)
		print('')
		'''
		
		#Check
		if self.PrintingClassSkipKeyStrsList==None:
			self.PrintingClassSkipKeyStrsList=[]
		if self.PrintingInstanceSkipKeyStrsList==None:
			self.PrintingInstanceSkipKeyStrsList=[]

		#filter the skip key strs
		PrintedDefaultSpecificKeyStrsList=SYS._filter(
				lambda __DefaultSpecificKeyStr:
				__DefaultSpecificKeyStr not in list(
					self.PrintingInstanceSkipKeyStrsList
				)+list(
					self.PrintingClassSkipKeyStrsList), 
				self.__class__.DefaultSpecificKeyStrsList
			)

		#Represent the Specific KeyStrs
		PrintTuplesList=map(
					lambda __SpecificKeyStr:
					(
						"<Spe>"+("<Instance>"
						if __SpecificKeyStr in self.__dict__ 
						else (
							"<Instance>_"
							if hasattr(
									self.__class__,__SpecificKeyStr
							) and type(getattr(
								self.__class__,__SpecificKeyStr
							))==property and getattr(
								self.__class__,'_'+__SpecificKeyStr
							)!=getattr(self,'_'+__SpecificKeyStr) and (
							'_'+__SpecificKeyStr not in self.PrintingClassSkipKeyStrsList and __SpecificKeyStr not in self.PrintingInstanceSkipKeyStrsList
							)
							else
							"<Class>"
							)
						)+__SpecificKeyStr,
						getattr(self,__SpecificKeyStr)
					),
					PrintedDefaultSpecificKeyStrsList
			)

		#/###################/#
		# Print the Default Base Key Strs... form the Instance or the still the Class
		#

		#Represent the BaseKeyStrs
		if self.PrintingBaseBool:
			
			#Debug
			'''
			print('Printer l 723')
			print('We print the bases')
			print('self.__class__.DefaultBaseKeyStrsList is ')
			print(self.__class__.DefaultBaseKeyStrsList)
			print('')
			'''

			#filter remove
			PrintedDefaultBaseKeyStrsList=SYS._filter(
					lambda __DefaultSpecificKeyStr:
					__DefaultSpecificKeyStr not in list(
						self.PrintingInstanceSkipKeyStrsList
					)+list(self.PrintingClassSkipKeyStrsList), 
					self.__class__.DefaultBaseKeyStrsList
				)

			#filter add
			if self.PrintingInstanceForceBaseKeyStrsList!=None:

				#add
				PrintedDefaultBaseKeyStrsList+=self.PrintingInstanceForceBaseKeyStrsList
			
			#map	
			PrintTuplesList+=map(
									lambda __BaseKeyStr:
									(
										"<Base>"+("<Instance>"
										if __BaseKeyStr in self.__dict__
										else "<Class>"
										)+__BaseKeyStr
										,
										getattr(self,__BaseKeyStr)
									),
									PrintedDefaultBaseKeyStrsList
								)

		#/###################/#
		# Print the New key strs in the instance
		#

		#print the NewInstanceKeyStrs in the __dict__
		if self.PrintingNewInstanceBool:
			
			#filter
			PrintedNewInstanceTuplesList=SYS._filter(
				lambda __NewItemTuple:
				__NewItemTuple[0
				] not in self.__class__.DefaultSpecificKeyStrsList+self.__class__.DefaultBaseKeyStrsList,
				self.__dict__.items()
			)

			#filter
			PrintedNewInstanceTuplesList=SYS._filter(
					lambda __PrintedNewInstanceTuple:
					__PrintedNewInstanceTuple[0] not in list(
						self.PrintingInstanceSkipKeyStrsList)+list(
						self.PrintingClassSkipKeyStrsList),
					PrintedNewInstanceTuplesList
				)

			#map
			PrintTuplesList+=map(
				lambda __NewItemTuple:
				(
					"<New><Instance>"+__NewItemTuple[0],
					__NewItemTuple[1]
				),
				PrintedNewInstanceTuplesList
			)

		#/###################/#
		# Print the New key strs in the class
		#

		#Represent the NewClassKeyStrs in the _self.__class____.__dict__
		if self.PrintingNewClassBool:


			#filter
			PrintedNewClassKeyStrsList=SYS._filter(
					lambda __KeyStr:
					__KeyStr not in self.__class__.KeyStrsList and __KeyStr not in self.__dict__,
					SYS.getKeyStrsListWithClass(
						self.__class__
					)
				)

			#filter
			PrintedNewClassKeyStrsList=SYS._filter(
					lambda __NewClassKeyStr:
					__NewClassKeyStr not in list(
					self.PrintingInstanceSkipKeyStrsList)+list(
					self.PrintingClassSkipKeyStrsList),
					PrintedNewClassKeyStrsList
				)

			#filter
			PrintTuplesList+=map(
				lambda __NewKeyStr:
				(
					"<New><Class>"+__NewKeyStr,
					self.__class__.__dict__[__NewKeyStr]
				),
				PrintedNewClassKeyStrsList
			)
		
		#/###################/#
		# Print force key strs
		#

		#Debug
		'''
		print('Printer l 811')
		print('We add some forced Key Strs')
		print('')
		'''
		
		#Check
		if self.PrintingInstanceForceKeyStrsList==None:
			self.PrintingInstanceForceKeyStrsList=[]

		#map
		PrintTuplesList+=map(
				lambda __PrintingKeyStr:
				(
					"<Spe><Instance>"+__PrintingKeyStr,
					self.__dict__[__PrintingKeyStr]
				) 
				if __PrintingKeyStr in self.__dict__ and __PrintingKeyStr in self.__class__.DefaultSpecificKeyStrsList
				else(
						(
							"<Base><Instance>"+__PrintingKeyStr,
							self.__dict__[__PrintingKeyStr]
						) 
						if __PrintingKeyStr in self.__dict__ and __PrintingKeyStr in self.__class__.DefaultBaseKeyStrsList
						else
						(
							(
								"<Base><Class>"+__PrintingKeyStr,
								getattr(self,__PrintingKeyStr)
							)
							if __PrintingKeyStr not in self.__dict__
							else
							(
								"<New><Instance>"+__PrintingKeyStr,
								self.__dict__[__PrintingKeyStr]
							)
						)
				),
				list(
					self.PrintingInstanceForceKeyStrsList
				)+list(self.PrintingClassForceKeyStrsList)
			)
					
		#Append
		global PrintAlreadyIdIntsList

		#debug
		'''
		print('Printer l.629')
		print('id(self) is ',id(self))
		print('self not in PrintAlreadyIdIntsList is ',str(
			self not in PrintAlreadyIdIntsList))
		print('')
		'''

		#define the PrintStr
		self.PrintStr=getPointerStr(
					self,
					**_KwargVariablesDict
				)+getPrintStr(
					dict(PrintTuplesList),
					**_KwargVariablesDict
				)

		#return
		return self.PrintStr

	def forcePrint(self,_KeyStrsList,_ClassStr):

		#append
		if self.__class__.__name__==_ClassStr:

			#Check
			if self.PrintingCopyVariable.PrintingInstanceForceKeyStrsList==None:

				#alias
				self.PrintingCopyVariable.PrintingInstanceForceKeyStrsList=_KeyStrsList
			else:

				#extend
				self.PrintingCopyVariable.PrintingInstanceForceKeyStrsList.extend(_KeyStrsList)

		else:

			#Check
			if self.PrintingCopyVariable.PrintingInstanceForceBaseKeyStrsList==None:

				#alias
				self.PrintingCopyVariable.PrintingInstanceForceBaseKeyStrsList=_KeyStrsList
			
			else:

				#extend
				self.PrintingCopyVariable.PrintingInstanceForceBaseKeyStrsList.extend(_KeyStrsList)
		
#</DefineClass>

#<DefinePrint>
PrinterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'DefaultInitBool',
		'DoUnitsInt',
		'StructuresOrderedDict',
		'PrintStr',
		'PrintIdInt',
		'PrintingCopyVariable',
		'PrintingInstanceSkipKeyStrsList',
		'PrintingInstanceForceKeyStrsList',
		'PrintingClassSkipKeyStrsList',
		'PrintingClassForceKeyStrsList',
		'PrintingBaseBool',
		'PrintingNewInstanceBool',
		'PrintingNewClassBool',
		'PrintingOutBool',
		'PrintingSelfBool',
		'PrintingInfoStr',
		'PrintingInstanceForceBaseKeyStrsList'
	]
)
#</DefinePrint>