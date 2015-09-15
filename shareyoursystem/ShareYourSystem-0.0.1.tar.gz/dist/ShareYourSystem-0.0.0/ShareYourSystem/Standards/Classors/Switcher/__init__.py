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
import copy
from ShareYourSystem.Standards.Classors import Doer,Observer
#</ImportSpecificModules>

#<DefineFunctions>
def setSwitch(
			_InstanceVariable,
			_DoMethodVariable=None,
			_DoerClassVariable=None,
			_HookVariable=None
		):

	#Debug
	'''
	print('l 31 setSwitch')
	print('_DoerVariable is ',_DoerVariable)
	print('_DoVariable is ',_DoVariable)
	print('_HookVariable is ',_HookVariable)
	#print('_InstanceVariable.__class__.NameStr is ',_InstanceVariable.__class__.NameStr)
	print('')
	'''
	
	#/#################/#
	# Adapt the shape of the do method str to switch
	#

	#Check
	if type(_DoMethodVariable)!=list:

		#Check
		if _DoMethodVariable==None:

			#/#################/#
			# Give all the do method str
			#

			#alias
			#DoMethodStrsList=_InstanceVariable.DoMethodStrsList

			#/#################/#
			# Give just the last DoMethodStr
			#

			#Check
			if _InstanceVariable.__class__.DoMethodStr in _InstanceVariable.__class__.SwitchMethodDict:
			
				#listify
				DoMethodStrsList=[_InstanceVariable.__class__.DoMethodStr]

			else:

				#listify
				DoMethodStrsList=[]

		else:
		
			#listify
			DoMethodStrsList=[_DoMethodVariable]


	else:

		#just alias
		DoMethodStrsList=_DoMethodVariable

	#/#################/#
	# Adapt the shape of the mro doer to switch
	#

	#get
	DoerClassesList=SYS.GetList(_DoerClassVariable)

	#Debug
	'''
	print('l 94 Switcher')
	print('_DoerClassVariable is')
	print(_DoerClassVariable)
	print('DoerClassesList is')
	print(DoerClassesList)
	print('')
	'''

	#Check
	if _DoerClassVariable==None:

		#/#################/#
		# by default this is all the mro doer that have all the switch do method
		# so do the intersection

		#Check
		if len(DoMethodStrsList)>0:

			#intersection
			DoerClassesList=list(
				set.intersection(*
					map(
						lambda __DoMethodStr:
						set(_InstanceVariable.__class__.SwitchMethodDict[__DoMethodStr]),
						DoMethodStrsList
					)
				)
			)

		else:

			#init
			DoerClassesList=[]

	#/#################/#
	# Adapt the shape of the hook strs
	#

	#Check
	if type(_HookVariable)!=list:
		if _HookVariable==None:
			HookStrsList=['Before','After']
		else:
			HookStrsList=[_HookVariable]
	else:
		HookStrsList=_HookVariable


	#/#################/#
	# Now map the switch
	#

	#Debug
	'''
	print('l 139 Switcher')
	#print('_InstanceVariable is ')
	#print(_InstanceVariable)
	print('DoMethodStrsList is')
	print(DoMethodStrsList)
	print('DoerClassesList is ')
	print(DoerClassesList)
	print('HookStrsList is ')
	print(HookStrsList)
	print('')
	'''

	#map
	map(
		lambda __HookStr:
		map(
			lambda __DoerClass:
			map(
					lambda __DoMethodStr:
					_InstanceVariable.__setattr__(
						'Watch'+__HookStr+__DoMethodStr[0].upper(
							)+__DoMethodStr[1:]+'With'+__DoerClass.NameStr+'Bool',
						False
					),
					DoMethodStrsList,
				),
			DoerClassesList
			),
		HookStrsList
		)

	#Debug
	'''
	print('l 170 Switcher')
	print('End of setSwitch')
	print('')
	'''

	#return 
	return _InstanceVariable
	
def switch(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#Debug
	'''
	print('l 196 Switcher')
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
	if hasattr(_InstanceVariable,_KwargVariablesDict['WatchBeforeDoBoolKeyStr']):

		#Debug
		'''
		print('Switcher l 201')
		print('Check for a WatchBeforeDoBoolKeyStr')
		print("_KwargVariablesDict['WatchBeforeDoBoolKeyStr'] is ")
		print(_KwargVariablesDict['WatchBeforeDoBoolKeyStr'])
		print('')
		'''
		
		#get
		WatchDoBool=getattr(
				_InstanceVariable,
				_KwargVariablesDict['WatchBeforeDoBoolKeyStr']
			)

		#Debug
		'''
		print('Switcher l 236')
		print('WatchDoBool is')
		print(WatchDoBool)
		'''

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
			[
				'BindObserveWrapMethodStr',
				'BindDoClassStr',
				'WatchBeforeDoBoolKeyStr'
			]
		)

	#Call
	return WrapUnboundMethod(
		_InstanceVariable,
		*_LiargVariablesList,
		**_KwargVariablesDict
	)

def getSwitch(_InstanceVariable,_MethodVariable=None):

	#Check
	if _MethodVariable==None:
		SwitchItemTuplesList=_InstanceVariable.SwitchMethodDict.items()
	elif type(_MethodVariable) in [list,tuple]:
		SwitchItemTuplesList=map(
			lambda __MethodStr:
			(
				__MethodStr,
				_InstanceVariable.SwitchMethodDict[__MethodStr]
			),
			_MethodVariable
		)
	else:
		SwitchItemTuplesList=[
			(
				_MethodVariable,
				_InstanceVariable.SwitchMethodDict[_MethodVariable]
			)
		]
		

	#Debug
	'''
	print('getSwitch l 266')
	print('_MethodVariable is ')
	print(_MethodVariable)
	print('SwitchItemTuplesList is ')
	print(SwitchItemTuplesList)
	print('')
	'''

	#return 
	WatchKeyStrsList=SYS.flat(
		SYS.flat(
			map(
				lambda __SwitchItemTuple:
				map(
					lambda __ClassStr:
					map(
						lambda __HookStr:
						'Watch'+__HookStr+SYS.getUpperWordStr(
							__SwitchItemTuple[0]
							)+'With'+SYS.getNameStrWithClassStr(
							__ClassStr
						)+'Bool',
						['Before','After']
					),
					map(lambda __Class:__Class.__name__,__SwitchItemTuple[1])
				),
				SwitchItemTuplesList
			)
		)
	)

	#Debug
	'''
	print('getSwitch l 300')
	print('WatchKeyStrsList is ')
	print(WatchKeyStrsList)
	print('WatchKeyStrsList is ')
	print(WatchKeyStrsList)
	print('')
	'''

	#return
	return dict(
				zip(
					WatchKeyStrsList,
					map(
						lambda __WatchKeyStr:
						getattr(_InstanceVariable,__WatchKeyStr),
						WatchKeyStrsList
					)
				)
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

			#alias
			SwitchedClass=self.DoClass

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
						[('WatchBeforeDoBoolKeyStr',self.WatchedBeforeDoBoolKeyStr)],
						**{'ObservingWrapMethodStr':self.WatchedDecorationMethodStr}
					)

			#Define
			SwitchedDecorationUnboundMethod=getattr(
						SwitchedClass,
						self.BindedDecorationMethodStr
					)

			#Now make the amalgam
			setattr(
					SwitchedClass,
					self.SwitchingWrapMethodStr,
					SwitchedDecorationUnboundMethod
				)

			#/##################/#
			# Set maybe for the first time
			# the setSwitch and the getSwitch
			
			#Check
			if hasattr(SwitchedClass,'setSwitch')==False:

				#set
				setattr(
						SwitchedClass,
						setSwitch.__name__,
						setSwitch
					)

				#get the unbound
				setSwitchUnboundMethod=getattr(
					SwitchedClass,
					setSwitch.__name__
				)

				#add in the inspect
				SwitchedClass.InspectMethodDict[setSwitch.__name__]=setSwitchUnboundMethod
				SwitchedClass.InspectInspectDict[setSwitch.__name__]=SYS.InspectDict(
					setSwitchUnboundMethod
				)

				#set
				self.setMethod(
					getSwitch.__name__,
					getSwitch
				)

			#/##################/#
			# Init the SwitchMethodDict
			#

			#Check
			if hasattr(SwitchedClass,'SwitchMethodDict')==False:

				#Debug
				'''
				print('Switcher l 345')
				print('SwitchedClass is ')
				print(SwitchedClass)
				print('we init a SwitchMethodDict')
				print('')
				'''

				#Check
				if hasattr(SwitchedClass.__bases__[0],'SwitchMethodDict'):

					#Debug
					print('Switcher l 488')
					print('SwitchedClass is ')
					print(SwitchedClass)
					print('SwitchedClass.__bases__[0] is ')
					print(SwitchedClass.__bases__[0])
					print('')

					#copy
					SwitchedClass.SwitchMethodDict=copy.copy(
						SwitchedClass.__bases__[0].SwitchMethodDict
					)

				else:

					#init
					SwitchedClass.SwitchMethodDict={
						self.SwitchingWrapMethodStr:[SwitchedClass]
					}
				
			else:

				#/##################/#
				# add
				#
	
				#Debug
				'''
				print('Switcher l 514')
				print('SwitchedClass is ')
				print(SwitchedClass)
				print('there is already a SwitchMethodDict')
				print('self.SwitchingWrapMethodStr  is ')
				print(self.SwitchingWrapMethodStr)
				print('SwitchedClass.SwitchMethodDict is ')
				print(SwitchedClass.SwitchMethodDict)
				print('')
				'''
				
				#copy
				SwitchedClass.SwitchMethodDict=copy.copy(
					SwitchedClass.SwitchMethodDict
				)

				#update
				if self.SwitchingWrapMethodStr in self.DoClass.SwitchMethodDict:
					SwitchedClass.SwitchMethodDict[
						self.SwitchingWrapMethodStr
					].append(SwitchedClass)
				else:
					SwitchedClass.SwitchMethodDict[
						self.SwitchingWrapMethodStr
					]=[SwitchedClass]

			#Add to the KeyStrsList
			SwitchedClass.KeyStrsList+=[
									'SwitchMethodDict'
								]



#</DefineClass>

