# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Attester helps for outputing and writing
AttestingPrefixStrs that are a succession of well-shaped
prints in the console from an defined attesting function.
This environment helps for displaying nicer exampling 
python codes in Readme and also contributing to unittests
of the modules.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Propertiser"
DecorationModuleStr=BaseModuleStr
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
import sys
from ShareYourSystem.Standards.Interfacers import Printer
#</ImportSpecificModules>

#<DefineLocals>
AttestingPrefixStr='attest_'
AttestingBeginStr='\n\n*****Start of the Attest *****\n\n'
AttestingJumpStr='\n\n------\n\n'
AttestingEndStr='\n\n*****End of the Attest *****\n\n'
#</DefineLocals>

#<DefineFunctions>
def writeAttestedStrWithFolderPathStrAndMethodStrAndAttestVariable(
	_FolderPathStr,_MethodStr,_AttestVariable):

	#Bind with TestedStr setting
	Printer.PrintIdBool=False
	AttestedStr=Printer.getPrintStr(_AttestVariable)
	Printer.PrintIdBool=True

	#Debug
	'''
	print('l 52 Attester')
	print('_FolderPathStr is ',_FolderPathStr)
	print('')
	'''

	#Check that there is a Folder Tests
	if os.path.isdir(_FolderPathStr)==False:
		os.popen('mkdir '+_FolderPathStr)
	elif os.popen("ls "+_FolderPathStr).read()!="":
		os.popen("cd "+_FolderPathStr+";rm *")

	#Write the TestedStr
	File=open(_FolderPathStr+_MethodStr+'.txt','w')
	File.write(AttestedStr)
	File.close()

def getAttestedStrWithStrsList(_StrsList):

	#Definition globals
	global AttestingBeginStr,AttestingJumpStr,AttestingEndStr

	#Reinit the alinea
	Printer.RepresentedAlineaStr=""
	Printer.RepresentedAlreadyVariablesList=[]

	#Init AttestedStr
	AttestedStr=AttestingBeginStr

	#Add attested Strs
	AttestedStr+=AttestingJumpStr.join(
		map(
			lambda __Str:
			Printer.represent(str(__Str),**{'PrintAlineaIsBool':False}),
			_StrsList
		)
	)

	#End the AttestedStr
	AttestedStr+=AttestingEndStr
	
	#Return
	return AttestedStr

#Definition an attest function for the classing class
def setAttest(_InstanceVariable,_AttestFolderPathStr="",**_KwargVariablesDict):

	#Debug
	'''
	print('l 92 Attester setAttest')
	print('_AttestFolderPathStr is ',_AttestFolderPathStr)
	print('')
	'''
	
	#Set
	if _AttestFolderPathStr=="": 	
		_AttestFolderPathStr=_InstanceVariable.__class__.DeriveClassor.AttestingFolderPathStr
	_InstanceVariable.__class__.DeriveClassor.AttestingFolderPathStr=_AttestFolderPathStr

	#Write the TestedStr made by each function and append an equivalent test method into the test ordered dict
	map(
			lambda __AttestedUnboundMethod:
			writeAttestedStrWithFolderPathStrAndMethodStrAndAttestVariable(
				_AttestFolderPathStr,
				__AttestedUnboundMethod.__name__,
				__AttestedUnboundMethod(_InstanceVariable)
			),
			_InstanceVariable.__class__.DeriveClassor.AttestedUnboundMethodsList
		)
#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class AttesterClass(BaseClass):

	#Definition
	PrintKeyStrsList=[
							'AttestingFolderPathStr',
							'AttestedMethodStrsList'
						]

	def default_init(self,
						_AttestingFolderPathStr="",
						_AttestedMethodStrsList=None,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#debug
		'''
		print('Attester l.143 __call__ method')
		print('_Class is ',_Class)
		print('')
		'''
		
		#Call the parent init method
		BaseClass.__call__(self,_Class)

		#Represent
		self.attest()

		#Return
		return _Class

	def do_attest(self):

		#set the TestedFolderPathStr
		if self.AttestingFolderPathStr=="":

			#In the gl
			self.AttestingFolderPathStr=SYS.PythonlogyLocalFolderPathStr+self.DoClass.__module__.replace(
				'.','/')+'/Attests/'

		#debug
		'''
		print('self.ClassedModule is ',self.ClassedModule)
		print('')
		'''

		#set the AttestedMethodStrsList
		self.AttestedMethodStrsList=SYS._filter(
				lambda __AttributeKeyStr:
				__AttributeKeyStr.startswith(AttestingPrefixStr),
				dir(self.DoClass)
			)

		#set
		self.AttestedUnboundMethodsList=map(
			lambda __AttestedMethodStr:
			getattr(self.DoClass,__AttestedMethodStr),
			self.AttestedMethodStrsList
		)

		#debug
		'''
		print('self.AttestedMethodStrsList is '+str(self.AttestedMethodStrsList))
		print('')
		'''

		#set
		if hasattr(self.DoClass,'setAttest')==False:
			setattr(
				self.DoClass,
				setAttest.__name__,
				setAttest
			)

		#Return self
		#return self
		
#</DefineClass>

#link
SYS._attest=lambda _StrsList:SYS._print(getAttestedStrWithStrsList(_StrsList))

#Set
AttesterClass.DeriveClassor.AttestingFolderPathStr=SYS.PythonlogyLocalFolderPathStr+AttesterClass.__module__.replace(
'.','/')+'/Attests/'

