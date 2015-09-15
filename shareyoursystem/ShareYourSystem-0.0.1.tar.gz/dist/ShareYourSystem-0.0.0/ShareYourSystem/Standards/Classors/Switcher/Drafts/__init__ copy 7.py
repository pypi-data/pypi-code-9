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
BaseModuleStr="ShareYourSystem.Standards.Classors.Watcher"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
import inspect
import six
from ShareYourSystem.Standards.Classors import Doer,Observer
#</ImportSpecificModules>

#<DefineFunctions>
def switch(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#Debug
	'''
	print('l 35')
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
#<DefineFunction>

#<DefineClass>
@DecorationClass()
class SwitcherClass(BaseClass):

	#Definition 
	RepresentingKeyStrsList=[	
		'SwitchingIsBool',
		'SwitchingWrapMethodStr'
	]

	def default_init(self,
						_SwitchingIsBool=False,
						_SwitchingWrapMethodStr="",
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
			'''
			print('l 195 Switcher')
			print('self.SwitchingWrapMethodStr is '+self.SwitchingWrapMethodStr)
			print('')
			'''

			#watch first
			self.watch(
						True,
						**{'ObservingWrapMethodStr':self.SwitchingWrapMethodStr}
					)

			#Debug
			'''
			print('l 204 Switcher')
			print('self.WatchedDecorationMethodStr is ',self.WatchedDecorationMethodStr)
			print('')
			'''
			
			#first bind
			self.bind(
						True,
						switch,
						"",
						switch.__name__,
						[('WatchDoBoolKeyStr',self.WatchedDoBoolKeyStr)],
						**{'ObservingWrapMethodStr':self.WatchedDecorationMethodStr}
					)

			#Now make the amalgam
			setattr(
					self.DoClass,
					self.SwitchingWrapMethodStr,
					getattr(
						self.DoClass,
						self.BindedDecorationMethodStr
					)
				)
#</DefineClass>

