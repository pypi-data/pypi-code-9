# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Binder...

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Observer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Observer=BaseModule
import six
#</ImportSpecificModules>

#<DefineLocals>
BindingDecorationPrefixStr=""
BindingDecorationSuffixStr="_"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class BinderClass(BaseClass):
	
	#Definition 
	RepresentingKeyStrsList=[
							'BindingIsBool',
							'BindingDecorationUnboundMethod',
							'BindingDecorationMethodStr',
							'BindingDecorationTagStr',
							'BindingItemTuplesList',
							'BindedDecorationMethodStr'
						]

	def default_init(self,
					_BindingIsBool=False,
					_BindingDecorationUnboundMethod=None,
					_BindingDecorationMethodStr='',
					_BindingDecorationTagStr="",
					_BindingItemTuplesList=None,
					_BindedDecorationMethodStr="",					   			
					**_KwargVariablesDict
				):

		#Call the init parent method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#Call the parent method
		Observer.ObserverClass.__bases__[0].__call__(self,_Class)

		#bind
		self.bind()

		#Return
		return _Class

	def do_bind(self):

		#Check
		if self.BindingIsBool:

			#Check
			if self.BindingDecorationUnboundMethod!=None or self.BindingDecorationMethodStr!="":

				#Debug
				'''
				print('l 73 Binder')
				print('we observe first')
				print('')
				'''
				
				#observe without linking
				self.observe(True)

				#Debug
				'''
				print('l 81 Binder')
				print('self.ObservingWrapMethodStr is ',self.ObservingWrapMethodStr)
				print('self.ObservedWrapMethodStr is ',self.ObservedWrapMethodStr)
				print('')
				'''

				#Check
				if self.BindingDecorationUnboundMethod==None:

					#Get
					self.BindingDecorationUnboundMethod=getattr(
						self.DoClass,
						self.BindingDecorationMethodStr
					)

				else:

					#set
					self.BindingDecorationMethodStr=self.BindingDecorationUnboundMethod.__name__

				#Debug
				'''
				print('Binder l.90')
				print('self.BindingDecorationUnboundMethod is')
				print(self.BindingDecorationUnboundMethod)
				print('')
				'''

				#Check
				if self.BindingDecorationTagStr=="":
					self.BindingDecorationTagStr=self.BindingDecorationMethodStr

				#set the new
				self.BindedDecorationMethodStr=BindingDecorationPrefixStr+self.BindingDecorationTagStr+BindingDecorationSuffixStr
				self.BindedDecorationMethodStr+=self.ObservingWrapMethodStr
				
				#Debug
				'''
				print('Binder l.102')
				print('self.BindedDecorationMethodStr is')
				print(self.BindedDecorationMethodStr)
				print('')
				'''

				#set to the class the BindingDecorationMethod
				setattr(
						self.DoClass,
						self.BindingDecorationMethodStr,
						self.BindingDecorationUnboundMethod
					)

				#Define
				BindedExecStr='def '+self.BindedDecorationMethodStr+'(_InstanceVariable,*_LiargVariablesList'
				BindedExecStr+=',**_KwargVariablesDict):'
				BindedExecStr+='\n\treturn _InstanceVariable.__class__.'+self.BindingDecorationMethodStr
				BindedExecStr+='(_InstanceVariable,*_LiargVariablesList'

				#Add
				self.BindingItemTuplesList+=[
					('BindObserveWrapMethodStr',self.ObservingWrapMethodStr),
					('BindDoClassStr',self.DoClass.__name__),
				]
				self.BindedItemTuplesList=','.join(
					map(
						lambda __BindingItemTuple:
						"'"+__BindingItemTuple[0]+"':'"+str(__BindingItemTuple[1])+"'",
						self.BindingItemTuplesList
					)
				)
				BindedExecStr+=',**dict({'
				BindedExecStr+=self.BindedItemTuplesList
				BindedExecStr+='},**_KwargVariablesDict))\n' 
					
				#exec
				six.exec_(BindedExecStr)

				#set to the class the BindingDecorationMethod
				setattr(
						self.DoClass,
						self.BindedDecorationMethodStr,
						locals()[self.BindedDecorationMethodStr]
					)


				#Return self
				#return self

#</DefineClass>

