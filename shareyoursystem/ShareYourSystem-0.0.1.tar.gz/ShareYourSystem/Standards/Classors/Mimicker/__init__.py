# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Mimicker...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Switcher"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors import Doer
import six
#</ImportSpecificModules>

#<DefineLocals>
MimickingWrapPrefixStr="mimic_"
MimickingDecorationPrefixStr=""
MimickingDecorationTagStr="superMimic"
MimickingDecorationSuffixStr="_"
#</DefineLocals>

#<DefineFunctions>
def mimic(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#Set
	MimicMethodStr=_KwargVariablesDict['MimicMethodStr']
	MimicClassStr=_KwargVariablesDict['MimicClassStr']
	MimicClass=getattr(SYS,MimicClassStr)
	MimicUnBoundMethod=getattr(
		MimicClass,
		MimicMethodStr
	)
	BaseClassStr=_KwargVariablesDict['BaseClassStr']
	BaseClass=getattr(SYS,BaseClassStr)
	del _KwargVariablesDict['MimicMethodStr']
	del _KwargVariablesDict['MimicClassStr']
	del _KwargVariablesDict['BaseClassStr']
	
	#Debug
	'''
	print('Mimicker l.48 inside of the function mimic')
	#print('_InstanceVariable is ',_InstanceVariable)
	print('_LiargVariablesList is ',_LiargVariablesList)
	print('_KwargVariablesDict is ',_KwargVariablesDict)
	print('')
	'''

	if len(_KwargVariablesDict)>0:

		#group by
		[
			MimicTempAttributeItemTuplesList,
			MimicTempNotAttributeItemTuplesList
		]=SYS.groupby(
			lambda __KwargItemTuple:
			hasattr(_InstanceVariable,__KwargItemTuple[0]),
			_KwargVariablesDict.items()
		)

		#Debug
		'''
		print('MimicTempAttributeItemTuplesList is ',MimicTempAttributeItemTuplesList)
		print('MimicTempNotItemTuplesList is ',MimicTempNotItemTuplesList)
		print('')
		'''

		#set in the instance the corresponding kwarged arguments
		map(	
				lambda __MimicTempAttributeItemTuple:
				#set direct explicit attributes
				_InstanceVariable.__setattr__(*__MimicTempAttributeItemTuple),
				MimicTempAttributeItemTuplesList
			)

		#Define
		MimicKwargDict=dict(MimicTempNotAttributeItemTuplesList)

	else:

		#Define
		MimicKwargDict={}

	#Init
	MimicOutputVariable=None

	#Debug
	'''
	print('Mimicker l.96 inside of the function mimic')
	print('MimicClass is ',MimicClass)
	print('MimicMethodStr is ',MimicMethodStr)
	print('MimicUnBoundMethod is ',MimicUnBoundMethod)
	print('')
	'''
	
	#call the Mimicked function
	if len(MimicKwargDict)>0:
		MimicOutputVariable=MimicUnBoundMethod(
							_InstanceVariable,
							*_LiargVariablesList,
							**MimicKwargDict
						)
	else:
		MimicOutputVariable=MimicUnBoundMethod(
				_InstanceVariable,
				*_LiargVariablesList
			)

	#Debug
	'''
	print('Mimicker l.117 inside of the function mimic')
	print('MimicOutputVariable is ',MimicOutputVariable)
	print('')
	'''

	#Check
	if BaseClass.DoingGetBool==False:

		#Return 
		return _InstanceVariable
	
	else:

		#Return the 
		return MimicOutputVariable
#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class MimickerClass(BaseClass):
	
	#Definition 
	RepresentingKeyStrsList=[
		'MimickingDoMethodStr',
		'MimickedWrapMethodStr'
	]

	def default_init(self,	
					_MimickingDoMethodStr="",
					_MimickedWrapMethodStr="",	   			
					**_KwargVariablesDict
				):

		#Call the init parent method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#Call the parent init method
		BaseClass.__call__(self,_Class)

		#mimic
		self.mimic()

		#Return
		return _Class

	def do_mimic(self):
			
		#Debug
		'''
		print('l 174 Mimicker')
		print('self.MimickingDoMethodStr is ',self.MimickingDoMethodStr)
		print('')
		'''

		#Check
		if self.MimickingDoMethodStr!="":

			#observe
			self.observe(True,self.MimickingDoMethodStr)

			#set
			self.MimickedWrapMethodStr=MimickingWrapPrefixStr+self.MimickingDoMethodStr

			#Debug
			'''
			print('l 75 Mimicker ')
			print('self.MimickedWrapMethodStr is ',self.MimickedWrapMethodStr)
			print('')
			'''

			#Define
			MimickedDoStr=SYS.getUpperWordStr(
				self.MimickingDoMethodStr
			)
			MimickedDoerStr=Doer.DoStrToDoerStrOrderedDict[MimickedDoStr]

			#Debug
			'''
			print('l 84 Mimicker ')
			print('MimickedDoStr is ',MimickedDoStr)
			print('MimickedDoerStr is ',MimickedDoerStr)
			print('MimickedBaseModule is ',MimickedBaseModule)
			print('')
			'''

			#Definitions
			MimickedBaseClass=getattr(
				SYS,
				SYS.getClassStrWithNameStr(MimickedDoerStr)
			)

			#get
			MimickedDoExecStr=getattr(
				MimickedBaseClass,
				'Do'+MimickedBaseClass.NameStr+'ExecStr'
			)

			#debug
			'''
			print('l 206 Mimicker')
			print('MimickedDoExecStr is ')
			print(MimickedDoExecStr)
			print('')
			'''

			#replace
			MimickedDecorationMethodStr=MimickingDecorationPrefixStr+MimickingDecorationTagStr+MimickingDecorationSuffixStr
			MimickedDecorationMethodStr+=self.ObservedWrapMethodStr

			#Debug
			'''
			print('l 232 Mimicker')
			print('MimickedDecorationMethodStr is '+MimickedDecorationMethodStr)
			print('')
			'''
			
			#replace
			MimickedExecStr='def '+MimickedDecorationMethodStr+'('+'('.join(
				MimickedDoExecStr.split('(')[1:]
			)

			#Debug
			'''
			print('l 208 Mimicker')
			print('MimickedExecStr is ')
			print(MimickedExecStr)
			print('')
			'''
			
			#Add to the ImitatedDoneExecStr
			MimickedExecStr+='\n\treturn mimic(_InstanceVariable,*_LiargVariablesList,'
			MimickedExecStr+='**dict({\'MimicMethodStr\':\''+self.MimickedWrapMethodStr+'\','
			MimickedExecStr+='\'MimicClassStr\':\''+self.DoClass.__name__+'\','
			MimickedExecStr+='\'BaseClassStr\':\''+MimickedBaseClass.__name__+'\''
			MimickedExecStr+='},**_KwargVariablesDict))'
			
			#Debug
			'''
			print('l 223 Mimicker')
			print('MimickedExecStr is ')
			print(MimickedExecStr)
			print('')
			'''
			
			#exec
			six.exec_(MimickedExecStr)

			#set
			self.MimickedDecorationUnboundMethod=locals()[MimickedDecorationMethodStr]

			#set in the __class__
			self.setMethod(
						MimickedDecorationMethodStr,
						self.MimickedDecorationUnboundMethod
					)

			#make the amalgam
			self.setMethod(
						self.MimickingDoMethodStr,
						self.MimickedDecorationUnboundMethod
					)

			#set a pointer to the fundamental class
			self.MimickedDecorationUnboundMethod.BaseDoClass=MimickedBaseClass
		
#</DefineClass>

