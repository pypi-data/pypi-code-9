# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Debugger from a DebuggerClass instance has a debug function
that prints in the console a state (to be defined) 
of the environnement. This print can be indented with 
the number of function frames from  which the process
has passed through, for a nicer visualisation of the 
kind of hooked functions. More options in the display
can be possible like the number of the line in the corresponding
code or the pick of KeyStrs helping for precising the 
debugging instance identity.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Printer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Doer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import inspect
Printer=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
if hasattr(SYS,'DebugPrintBool')==False:
	SYS.DebugPrintBool=True
DebugStartStr='\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n'
DebugEndStr='\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n'
DebugElementStr='    '
DebugIsStr=' is '
DebugHeadPrefixStr='////////////////////////////////\n'
DebugHeadSuffixStr='\n////////////////////////////////\n\n'
DebugWhoStr='\n*****\n'

def getDebuggedListWithFrame(_Frame):

	#Definition the FilePathStr
	FilePathStr='/'.join(_Frame.f_code.co_filename.split('/')[-2:])

	#Return 
	return [FilePathStr,_Frame.f_code.co_name]

def getDebuggedStrWithPrintVariable(_PrintVariable):

	#Type
	Type=type(_PrintVariable)

	#Debug
	'''
	print('l 62 Debugger')
	print('Type is ',Type)
	print('SYS.StrTypesList is ',SYS.StrTypesList)
	print('')
	'''
	
	#set the DebuggedStr with the _PrintVariable
	if type(_PrintVariable) in SYS.StrTypesList:
		return _PrintVariable
	elif type(_PrintVariable)==tuple:

		#Check for an end
		if len(_PrintVariable)>3:
			DebuggedEndStr=_PrintVariable[3]
		else:
			DebuggedEndStr=""

		#join
		DebuggedStr='\n'.join(
		map(
				lambda __KeyStr:
				_PrintVariable[0]+__KeyStr+DebuggedEndStr+' is '+SYS._str(
					_PrintVariable[1][__KeyStr] if type(
						_PrintVariable[1]
					) in [collections.OrderedDict,dict]
					else getattr(
							_PrintVariable[1],
							__KeyStr
						) 
					if hasattr(_PrintVariable[1],__KeyStr) 
					else "WARNING : No attribute like this"
				,**{
						'RepresentingAlineaIsBool':False
					}),
				_PrintVariable[2]
			)
		)+'\n'

		#return
		return DebuggedStr

	elif type(_PrintVariable)==list:
		return '\n'.join(map(getDebuggedStrWithPrintVariable,_PrintVariable))

	else:

		#return
		return str(_PrintVariable)
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class DebuggerClass(BaseClass):
	
	def default_init(self,
						_DebuggingPrintStr="",
						_DebuggingIdentityBool=True,
						_DebuggingFrameBool=True,
						_DebuggingBacksInt=1,												
						_DebuggingNotFrameFunctionStrsList=[
							"AlertedFunction",
							"ArgumentedFunction",
							"TriggeredFunction",
							"HookedFunction",
							"SwitchedFunction",
							"<lambda>",
							"DoerFunction",
							"initDo",
							"ImitaterFunction",
							"imitateDo",
							"superDo_debug",
							"do",
							"watch",
							"switch",
							"mimic"
						],
						_DebuggingNotFrameCodeStrsList=[
							"<string>"
						],
						_DebuggingIsBool=True, 													
						_DebuggedFramesList=None, 
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_debug(self):

		'''
		#Special keywords args
		if self.DebuggingPrintVariable=='<DoingVariables>':
			self.debug(('self.',self,self.__class__.DoingAttributeVariablesOrderedDict.keys()))
		'''

		#Debug
		'''
		print(
				'Debugger l 170'
			)
		print('Start debug')
		print('self.DebuggingIsBool is '+str(self.DebuggingIsBool))
		print('')
		'''
		
		#Check
		if self.DebuggingIsBool:

			#debug
			'''
			print('Debugger debug method')
			print('DebuggedCurrentFrame is ',DebuggedCurrentFrame)
			print('self.DebuggedFramesList is ',self.DebuggedFramesList)
			print('')
			'''

			#Definition the DebuggedCurrentFrame
			DebuggedCurrentFrame=inspect.currentframe()
			for __BackInt in xrange(self.DebuggingBacksInt):
				DebuggedCurrentFrame=DebuggedCurrentFrame.f_back

			#Init the DebuggedStr
			DebuggedStr=DebugStartStr

			#Append maybe for the first time
			DebuggedDecorationBool=False
			if len(self.DebuggedFramesList
				)==0 or DebuggedCurrentFrame!=self.DebuggedFramesList[0]:

				#debug
				'''
				print('This is the first frame ')
				print('')
				'''

				#Build the DebuggedBackFramesList
				DebuggedBackFramesList=[]
				DebuggedBackFrame=DebuggedCurrentFrame
				while DebuggedBackFrame.f_back!=None:
					#if hasattr(self,DebuggedBackFrame.f_back.f_code.co_name):

					#debug
					'''
					print("DebuggedCurrentFrame.f_code.co_name is ",DebuggedCurrentFrame.f_code.co_name)
					print("DebuggedBackFrame.f_back.f_code.co_name is ",DebuggedBackFrame.f_back.f_code.co_name)
					print('')
					'''

					#Append
					if DebuggedBackFrame.f_back.f_code.co_name in self.DebuggingNotFrameFunctionStrsList or DebuggedBackFrame.f_back.f_code.co_filename.split('/')[-1] in self.DebuggingNotFrameCodeStrsList:
						DebuggedDecorationBool=True
					else:
						DebuggedBackFramesList.append(DebuggedBackFrame.f_back)
					DebuggedBackFrame=DebuggedBackFrame.f_back

				#Reduce the DebuggedBackFramesList with the DebuggedCurrentFrame
				self.DebuggedFramesList=[DebuggedCurrentFrame]+DebuggedBackFramesList

				#Debug
				'''
				print('DebuggedCurrentFrame.f_code.co_name is ',DebuggedCurrentFrame.f_code.co_name)
				print('')
				'''

				#set
				CodeStr= DebuggedCurrentFrame.f_code.co_filename.split('/')[-1]

				#Shift maybe
				if DebuggedCurrentFrame.f_code.co_name in self.DebuggingNotFrameFunctionStrsList or CodeStr in self.DebuggingNotFrameCodeStrsList:
					self.DebuggedFramesList=self.DebuggedFramesList[1:]
					DebuggedCurrentFrame=self.DebuggedFramesList[0] 

				#set the DebuggedBackFrameStr
				DebuggedBackFrameStr='\nFrom '+' | '.join(
						map(
							lambda __InspectedList:
							' '.join(__InspectedList),
							map(getDebuggedListWithFrame,DebuggedBackFramesList)
						)
					)

				#Check
				if self.DebuggingFrameBool:

					#Add the name of the function or method
					DebuggedStr+=DebugHeadPrefixStr+" ".join(
								[
									'/'.join(DebuggedCurrentFrame.f_code.co_filename.split('/')[-2:]),
									DebuggedCurrentFrame.f_code.co_name
								]
								)+DebuggedBackFrameStr+DebugHeadSuffixStr

			#Update the RepresentingDict
			Printer.PrintAlineaStr=''.join(
				[DebugElementStr]*(len(self.DebuggedFramesList)-1))

			#debug
			'''
			print('self.DebuggedAlineaStr is ',self.DebuggedAlineaStr)
			print('self.DebuggingRepresentingDict is ',self.DebuggingRepresentingDict)
			print('')
			'''

			#Add the lineno
			DebuggedStr+='l.'+str(DebuggedCurrentFrame.f_lineno)+' : '

			#Add some features to identify the instance
			if self.DebuggingIdentityBool:

				#add
				DebuggedStr+=DebugWhoStr+'I am with '+str(
					SYS._filter(
								lambda __ItemTuple:
								__ItemTuple[0].endswith('TagStr'),
								#and __ItemTuple[0] not in self.__class__.DefaultBaseKeyStrsList
								#			+self.__class__.DefaultSpecificKeyStrsList,
								self.__dict__.items()
							)
					)+", "+str(self.PrintIdInt)+" "+DebugWhoStr

			#Add the DebuggedStr from the debugging variable
			DebuggedStr+=getDebuggedStrWithPrintVariable(
				self.DebuggingPrintStr)

			#add the end
			DebuggedStr+=DebugEndStr
				
			#Print
			if SYS.DebugPrintBool:

				#_print
				self._print(
							str(DebuggedStr)+Printer.PrintAlineaStr,
							**{
								#'RepresentedDeepInt':1
							}
						)

#</DefineClass>

#<DefinePrint>
DebuggerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'DebuggingPrintStr',
		'DebuggingIdentityBool',
		'DebuggingFrameBool',
		'DebuggingBacksInt',								
		'DebuggingNotFrameFunctionStrsList',
		'DebuggingNotFrameCodeStrsList',
		'DebuggingIsBool', 													
		'DebuggedFramesList'
	]
)
#</DefinePrint>
