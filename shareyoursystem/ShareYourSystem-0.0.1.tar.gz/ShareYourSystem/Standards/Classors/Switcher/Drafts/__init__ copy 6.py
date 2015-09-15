# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Switcher 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Resetter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
import inspect
import six

from ShareYourSystem.Standards.Classors import Doer,Observer
#</ImportSpecificModules>

#<DefineLocals>
SwitchingDecorationPrefixStr="switch_"
#</DefineLocals>

#<DefineFunctions>
def switch(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#Debug
	'''
	print('l 67')
	print('In the switch function ')
	print('_KwargVariablesDict is ')
	print(_KwargVariablesDict)
	print('')
	'''

	"""
	#alias
	FuncDict=switch.__dict__

	#Debug
	'''
	print('l 52')
	print('In the switch function ')
	print('FuncDict is ')
	print(FuncDict)
	print('')
	'''
	"""

	#Check
	if hasattr(_InstanceVariable,_KwargVariablesDict['WatchDoBoolKeyStr']):

		#get
		WatchDoBool=getattr(
				_InstanceVariable,
				_KwargVariablesDict['WatchDoBoolKeyStr']
				)

		#Switch
		if WatchDoBool:
			return _InstanceVariable
	
	
	#get the wrapped method
	WrapUnboundMethod=getattr(
		getattr(
			SYS,
			_KwargVariablesDict['BindDoClassStr']
		),
		_KwargVariablesDict['BindObserveWrapMethodStr']
	)

	#del
	map(
			lambda __KeyStr:
			_KwargVariablesDict.__delitem__(__KeyStr),
			['BindObserveWrapMethodStr','BindDoClassStr','WatchDoBoolKeyStr']
		)


	#Call
	return WrapUnboundMethod(
		_InstanceVariable,
		*_LiargVariablesList,
		**_KwargVariablesDict
	)

"""
def SwitchFunction(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#Get
	SwitchMethodStr=_KwargVariablesDict['SwitchMethodStr']
	DoMethodStr=SwitchMethodStr.split('_')[-1]
	DoStr=SwitchMethodStr[0].upper()+SwitchMethodStr[1:]
	SwitchDoBoolKeyStr='Watch'+DoStr+'Bool'
	SwitchClassStr=_KwargVariablesDict['SwitchClassStr']
	SwitchClass=getattr(SYS,SwitchClassStr)
	SwitchUnboundMethod=getattr(
		SwitchClass,
		SwitchMethodStr
	)
	del _KwargVariablesDict['SwitchMethodStr']
	del _KwargVariablesDict['SwitchClassStr']
	
	#Debug
	print('l 52 Switcher')
	print('We are in the SwitchFunction')
	print('SwitchMethodStr is ',SwitchMethodStr)
	print('SwitchClass is ',SwitchClass)
	print('SwitchDoBoolKeyStr is ',SwitchDoBoolKeyStr)
	print('SwitchUnboundMethod is ',SwitchUnboundMethod)
	print('')
	
	#Check
	if hasattr(_InstanceVariable,SwitchDoBoolKeyStr)==False:
		_InstanceVariable.__setattr__(
			SwitchDoBoolKeyStr,
			False
		)

	#Debug
	'''
	print('l 62 Switcher)
	print('We are in the SwitchedNewFunction')
	'''
	
	#Debug
	'''
	print('l 68 Switcher')
	print('We are in the SwitchedNewFunction')
	print('SwitchUnboundMethod is ',SwitchUnboundMethod)
	print('')
	'''

	#Check
	if getattr(_InstanceVariable,SwitchDoBoolKeyStr)==False:

		#call
		return SwitchUnboundMethod(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict)

	else:

		#return InstanceVariable
		return _InstanceVariable
"""
#<DefineFunction>

#<DefineClass>
@DecorationClass()
class SwitcherClass(BaseClass):

	#Definition 
	RepresentingKeyStrsList=[	
		'SwitchingIsBool',
		'SwitchedWrapMethodStr'	
	]

	def default_init(self,
						_SwitchingIsBool=False,
						_SwitchedWrapMethodStr="",
						**_KwargVariablesDict
				):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#Call the parent method
		BaseClass.__call__(self,_Class)

		#switch
		self.switch()

		#Return
		return _Class

	def do_switch(self):

		#Check
		if self.SwitchingIsBool:

			#Debug
			print('l 162 Switcher')
			print('self.ObservingWrapMethodStr is '+self.ObservingWrapMethodStr)
			print('')

			#watch first
			self.SwitchedWrapMethodStr=self.ObservingWrapMethodStr
			self.watch(True)

			#Debug
			print('Watcher l 170')
			print('self.WatchedDecorationMethodStr is ',self.WatchedDecorationMethodStr)
			print('')

			#first bind
			self.bind(
						_DecorationUnboundMethod=switch,
						_ItemTuplesList=[('WatchDoBoolKeyStr',self.WatchedDoBoolKeyStr)],
						**{'ObservingWrapMethodStr':self.WatchedDecorationMethodStr}
					)

			#Now make the amalgam
			setattr(
					self.DoClass,
					self.SwitchedWrapMethodStr,
					getattr(
						self.DoClass,
						self.BindedDecorationMethodStr
					)
				)



			"""
			#Debug
			'''
			print('l 141 Switcher')
			print('We are switching here')
			print('self.SwitchingMethodStr is ',self.SwitchingMethodStr)
			print('')
			'''

			#get
			self.SwitchedUnboundMethod=getattr(
								self.DoClass,
								self.SwitchingMethodStr
							)
			print(self.SwitchedUnboundMethod)
			if self.SwitchedUnboundMethod.__name__!=self.SwitchingMethodStr:
				self.SwitchedUnboundMethod=getattr(
					self.DoClass,
					self.SwitchedUnboundMethod.__name__
			)
			self.SwitchedWrapMethodStr=self.SwitchedUnboundMethod.__name__

			#debug
			'''
			print('self.SwitchedUnboundMethod is ')
			print(self.SwitchedUnboundMethod)
			print('')
			'''

			#set the new
			self.SwitchedDecorateMethodStr=SwitchingDecorationPrefixStr+self.SwitchedWrapMethodStr

			#Define
			SwitchedExecStr='def '+self.SwitchedMethodStr+'(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):'
			SwitchedExecStr+='\n\treturn SwitchFunction(_InstanceVariable,*_LiargVariablesList'
			SwitchedExecStr+=',**dict({\'SwitchMethodStr\':\''+self.SwitchingMethodStr+'\',\'SwitchClassStr\':\''+self.DoClass.__name__+'\'},**_KwargVariablesDict))\n' 

			#Debug
			'''
			print('l 152 Switcher')
			print('SwitchedExecStr is ')
			print(SwitchedExecStr)
			print('')
			'''

			#exec
			six.exec_(SwitchedExecStr)

			#Set in the class
			setattr(
						self.DoClass,
						self.SwitchingMethodStr,
						locals()[self.SwitchedMethodStr]
				)
			"""

#</DefineClass>

