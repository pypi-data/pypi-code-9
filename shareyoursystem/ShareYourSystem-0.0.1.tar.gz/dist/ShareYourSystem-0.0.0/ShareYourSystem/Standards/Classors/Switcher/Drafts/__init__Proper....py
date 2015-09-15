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
from ShareYourSystem.Standards.Classors import Doer,Observer
#</ImportSpecificModules>

#<DefineFunctions>
def getWatchBool(_InstanceVariable,**_KwargVariablesDict):

	#get and return
	return getattr(_InstanceVariable,'_'+_KwargVariablesDict['WatchDoBoolKeyStr'])

def setWatchBool(_InstanceVariable,_ValueVariable,**_KwargVariablesDict):

	#Debug
	'''
	print('l 37 Switcher')
	print('We are in the setWatchBool')
	print('_KwargVariablesDict is ')
	print(_KwargVariablesDict)
	print('')
	'''
	
	#Alias
	HideSwitchDoBoolKeyStr='_'+_KwargVariablesDict['WatchDoBoolKeyStr']

	#set
	_InstanceVariable.__setattr__(
		HideSwitchDoBoolKeyStr,
		_ValueVariable
		)

	#set
	_InstanceVariable.__setattr__(
		_KwargVariablesDict['SwitchDoBoolKeyStr'],
		_ValueVariable
		)

def delWatchBool(_InstanceVariable,**_KwargVariablesDict):

	#delete
	_InstanceVariable.__delattr__('_'+_KwargVariablesDict['SwitchDoBoolKeyStr'])

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
	if hasattr(_InstanceVariable,_KwargVariablesDict['SwitchDoBoolKeyStr']):

		#get
		WatchDoBool=getattr(
				_InstanceVariable,
				_KwargVariablesDict['SwitchDoBoolKeyStr']
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
			['BindObserveWrapMethodStr','BindDoClassStr','SwitchDoBoolKeyStr']
		)

	#Call
	return WrapUnboundMethod(
		_InstanceVariable,
		*_LiargVariablesList,
		**_KwargVariablesDict
	)
#</DefineFunctions>

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
		Observer.ObserverClass.__bases__[0].__call__(self,_Class)

		#reset
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

			#set to the class
			self.DoClass.SwitchDoBoolKeyStr='Switch'+'Watch'.join(
				self.WatchedDoBoolKeyStr.split('Watch')[1:]
			)

			#Debug
			'''
			print('Switcher l 125')
			print('self.WatchedDoBoolKeyStr is ',self.WatchedDoBoolKeyStr)
			print('self.DoClass.SwitchDoBoolKeyStr is ',self.DoClass.SwitchDoBoolKeyStr)
			print('Now we bind')
			'''
			
			#map binds
			SwitchtedBindDecorationUnboundMethodsList=map(
					lambda __Function:
					self.bind(
								True,
								__Function,
								"",
								__Function.__name__+'With'+self.DoClass.NameStr,
								[
									('SwitchDoBoolKeyStr',self.DoClass.SwitchDoBoolKeyStr),
									('WatchDoBoolKeyStr',self.WatchedDoBoolKeyStr),
								],
								**{'ObservingWrapMethodStr':""}
						).BindedDecorationUnboundMethod,
					[getWatchBool,setWatchBool,delWatchBool]
				)

			#Set
			setattr(
						self.DoClass,
						self.DoClass.SwitchDoBoolKeyStr,
						property(
							*SwitchtedBindDecorationUnboundMethodsList
						)
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
						[('SwitchDoBoolKeyStr',self.DoClass.SwitchDoBoolKeyStr)],
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

			#Add to the KeyStrsList
			self.DoClass.KeyStrsList+=[
										self.DoClass.SwitchDoBoolKeyStr,
										'SwitchDoBoolKeyStr'
									]
#</DefineClass>

