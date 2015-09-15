# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Watcher 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Binder"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
import copy

from ShareYourSystem.Standards.Classors import Doer,Observer,Representer
#</ImportSpecificModules>

#<DefineLocals>
WatchingPrefixKeyStr="Watch"
#</DefineLocals>

#<SetRepresent>
def getIsBoolWithItemTupleAndKeyStr(_ItemTuple,_KeyStr):

	#Debug
	'''
	print('Watcher l 35')
	print('_ItemTuple is ',_ItemTuple)
	print('_KeyStr is ',_KeyStr)
	print('')
	'''
	
	#Return
	return _ItemTuple[0].split('>')[-1].startswith(_KeyStr)
OldRepresentFunction=copy.copy(Representer.represent)
def represent(_Variable,**_KwargVariablesDict):
	return OldRepresentFunction(
		_Variable,
		**dict(
			_KwargVariablesDict,
			**{
				'RepresentingNotConcludeTuplesList':
				[(getIsBoolWithItemTupleAndKeyStr,'_Watch')]
			}
		)
	)
represent.__name__="Watcher@represent"
Representer.represent=represent
#</SetRepresent>

#<DefineFunctions>
def watch(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#Debug
	'''
	print('l 67')
	print('In the watch function ')
	print('_KwargVariablesDict is ')
	print(_KwargVariablesDict)
	print('')
	'''

	#alias
	FuncDict=_InstanceVariable.__class__.watch.__dict__

	#Debug
	'''
	print('l 79')
	print('In the watch function ')
	print('FuncDict is ')
	print(FuncDict)
	print('')
	'''

	#Set in the _InstanceVariable
	_InstanceVariable.__setattr__(
			FuncDict['WatchDoBoolKeyStr'],
			True
		)

	#get the wrapped method
	WrapUnboundMethod=getattr(
		getattr(
			SYS,
			FuncDict['BindDoClassStr']
		),
		FuncDict['BindObserveWrapMethodStr']
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
class WatcherClass(BaseClass):

	#Definition 
	RepresentingKeyStrsList=[	
		'WatchingIsBool',	
		'WatchedDoBoolKeyStr',
		'WatchedDecorationMethodStr'
	]

	def default_init(self,		
						_WatchingIsBool=False,
						_WatchedDoBoolKeyStr="",
						_WatchedDecorationMethodStr="",		
						**_KwargVariablesDict
				):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#Call the parent method
		Observer.ObserverClass.__bases__[0].__call__(self,_Class)

		#Watch
		self.watch()

		#Return
		return _Class

	def do_watch(self):

		#Check
		if self.WatchingIsBool:

			#Debug
			print('l 133 Watcher')
			print('self.ObservingWrapMethodStr is '+self.ObservingWrapMethodStr)
			print('')

			#observe first
			self.observe(True)

			#Define
			WatchedDoMethodStr=self.ObservingWrapMethodStr
			WatchedDoStr=WatchedDoMethodStr[0].upper()+WatchedDoMethodStr[1:]
			self.WatchedDoBoolKeyStr=WatchingPrefixKeyStr+WatchedDoStr+'Bool'

			#Debug
			print('l 145 Watcher')
			print('WatchedDoMethodStr is ',WatchedDoMethodStr)
			print('WatchedDoStr is ',WatchedDoStr)
			print('self.WatchedDoBoolKeyStr is ',self.WatchedDoBoolKeyStr)
			print('')

			#first bind
			self.bind(
						True,
						_DecorationUnboundMethod=watch,
						_ItemTuplesList=[('WatchDoBoolKeyStr',self.WatchedDoBoolKeyStr)],
						**{'ObservingWrapMethodStr':self.ObservedWrapMethodStr}
					)

			#set
			self.WatchedDecorationMethodStr=self.BindedDecorationMethodStr

			#Now make the amalgam
			setattr(
					self.DoClass,
					WatchedDoMethodStr,
					getattr(
						self.DoClass,
						self.BindedDecorationMethodStr
					)
				)
#</DefineClass>
