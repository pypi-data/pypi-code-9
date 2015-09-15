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
WatchingPrefixStr="Watch"
#</DefineLocals>

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



#<DefineClass>
@DecorationClass()
class WatcherClass(BaseClass):

	#Definition 
	RepresentingKeyStrsList=[
							'WatchingMethodStr', 	
							'WatchedDoBoolKeyStr'			
	]

	def default_init(self,
						_WatchingMethodStr="", 	
						_WatchedDoBoolKeyStr="",					
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

		#print
		'''
		print('l 66 Watcher')
		print('self.DoClass.DoMethodStr is '+self.DoClass.DoMethodStr)
		print('')
		'''

		#Check
		if self.WatchingMethodStr=="":
			self.WatchingMethodStr=self.DoClass.DoMethodStr

		#Debug
		'''
		print('l 76 Watcher')
		print('self.WatchingMethodStr is ',self.WatchingMethodStr)
		print('')
		'''
		
		#Define
		WatchedDoneStr=self.WatchingMethodStr
		self.WatchedDoBoolKeyStr=WatchingPrefixStr+WatchedDoneStr[0].upper()+WatchedDoneStr[1:]+'Bool'

		#Debug
		'''
		print('l 76 Watcher')
		print('self.WatchedDoBoolKeyStr is ',self.WatchedDoBoolKeyStr)
		print('')
		'''

		#Define
		def WatchedNewFunction(*_LiargVariablesList,**_KwargVariablesDict):

			#Define
			InstanceVariable=_LiargVariablesList[0]

			#Set to the instance
			InstanceVariable.__setattr__(self.WatchedDoBoolKeyStr,True)

			#Return 
			return InstanceVariable

		#Define
		WatchedUnboundMethodStr='Watch'+WatchedDoneStr

		#set
		setattr(
					self.DoClass,
					WatchedUnboundMethodStr,
					WatchedNewFunction
				)

		#bind
		self.bind(
					WatchedUnboundMethodStr,
					'Before',
					**{'ObservingMethodStr':self.WatchingMethodStr}
				)


#</DefineClass>
