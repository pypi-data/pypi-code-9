# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Observer...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Tester"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import copy
import inspect
#</ImportSpecificModules>

#<DefineFunctions>
def observe(_InstanceVariable,**_KwargVariablesDict):
	return _InstanceVariable
#</DefineFunctions>

#<DefineClass>
@DecorationClass()
class ObserverClass(BaseClass):
	
	def default_init(self,
					_ObservingIsBool=False,
					_ObservingWrapMethodStr="",	
					_ObservedWrapUnboundMethod=None,		
					_ObservedWrapMethodStr="",	   			
					**_KwargVariablesDict
				):

		#Call the init parent method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#debug
		'''
		print('Observer l.54 __call__ method')
		print('_Class is ',_Class)
		print('')
		'''
		
		#Call the parent init method
		BaseClass.__call__(self,_Class)

		#observe
		self.observe()

		#Return
		return _Class

	def do_observe(self):

		#Check
		if self.ObservingIsBool:

			#Debug
			'''
			print('Observer l.75')
			print('self.ObservingWrapMethodStr is')
			print(self.ObservingWrapMethodStr)
			print('')
			'''

			#Get
			self.ObservedWrapUnboundMethod=getattr(
				self.DoClass,
				self.ObservingWrapMethodStr
			) if self.ObservingWrapMethodStr!="" else observe

			#Debug
			'''
			print('Observer l 86')
			print('self.ObservedWrapUnboundMethod is ',self.ObservedWrapUnboundMethod)
			print('')
			'''
			
			#Define Check for not pointing a circular function...
			if self.ObservingWrapMethodStr!=self.ObservedWrapUnboundMethod.__name__:
				self.ObservedWrapMethodStr=self.ObservedWrapUnboundMethod.__name__
			else:
				self.ObservedWrapMethodStr=self.ObservingWrapMethodStr
			
			#Debug
			'''
			print('Observer l.85')
			print('self.ObservingWrapMethodStr is')
			print(self.ObservingWrapMethodStr)
			print('')
			'''

			#Return self
			#return self

#</DefineClass>

