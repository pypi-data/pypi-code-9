# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Classer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Mimicker"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Tester"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
Mimicker=BaseModule
from ShareYourSystem.Standards.Classors import Propertiser
import collections
#</ImportSpecificModules>

#<Define_Class>
@DecorationClass()
class ClasserClass(BaseClass):

	def default_init(self,	
						_ClassingSwitchMethodStrsList=None,	
						_ClassingWatchMethodStrsList=None,
						_ClassingStructureVariable=None,
						**_KwargVariablesDict
				):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#Call the parent method
		Mimicker.MimickerClass.__bases__[0].__call__(self,_Class)

		#class
		self._class()

		#Return
		return _Class

	def do__class(self):

		#Definition the MethodsList
		ClassedFunctionsList=SYS._filter(
			lambda __ListedVariable:
				type(__ListedVariable).__name__=="function"
				if hasattr(__ListedVariable,'__name__')
				else False,
				self.DoClass.__dict__.values()
		)

		#debug
		'''
		print('l 66 Classer')
		print("ClassedFunctionsList is ",WatchedFunctionsList)
		print('Set all the mimick methods')
		print('')
		'''

		#/###################/#
		# Mimic all that you can find 
		#

		#Get all the hooking methods
		ClassedMimickFunctionsList=SYS._filter(
			lambda __ListedVariable:
			__ListedVariable.__name__.startswith(
					Mimicker.MimickingWrapPrefixStr
			)
			if hasattr(__ListedVariable,'__name__')
			else False,
			ClassedFunctionsList
		)

		#debug
		'''
		print('l 82 Classer')
		print("ClassedMimickFunctionsList is ",ClassedMimickFunctionsList)
		print('')
		'''

		#map
		map(	
				lambda __ClassedMimickFunction:
				self.mimic(
					Mimicker.MimickingWrapPrefixStr.join(
						__ClassedMimickFunction.__name__.split(
							Mimicker.MimickingWrapPrefixStr)[1:]
						)
				),
				ClassedMimickFunctionsList
			)

		#/###################/#
		# Set the watch methods 
		#

		#debug
		'''
		print('l 104 Classer')
		print('set the watch functions')
		print('self.ClassingWatchMethodStrsList is ',self.ClassingWatchMethodStrsList)
		print('self.DoClass.DoMethodStr is ',self.DoClass.DoMethodStr)
		print('')
		'''
		
		#map
		map(	
				lambda __ClassingWatchUnboundMethodStr:
				self.watch(
					True,
					**{'ObservingWrapMethodStr':__ClassingWatchUnboundMethodStr}
				),
				self.ClassingWatchMethodStrsList
			)

		#/###################/#
		# Set the switch methods 
		#

		#debug
		'''
		print('l 104 Classer')
		print('set the switch functions')
		print('self.ClassingSwitchMethodStrsList is ',self.ClassingSwitchMethodStrsList)
		print('self.DoClass.DoMethodStr is ',self.DoClass.DoMethodStr)
		print('')
		'''
		
		#map
		map(	
				lambda __ClassingSwitchUnboundMethodStr:
				self.switch(
					True,
					__ClassingSwitchUnboundMethodStr
				),
				self.ClassingSwitchMethodStrsList
			)

		#/###################/#
		# Check for overriden propertize_ methods 
		#

		#Debug
		'''
		print('Classer l 125')
		print('Check for overriden propertize_ methods ')
		print('self.DoClass.InspectMethodDict')
		print(self.DoClass.InspectMethodDict)
		print('')
		'''

		#filter
		ClassedPropertyNewMethodDict=dict(
			SYS._filter(
				lambda __MethodItemTuple:
				__MethodItemTuple[0].startswith(
						Propertiser.PropertyPrefixStr
					) and (
					SYS.getNewMethodBool(self.DoClass,__MethodItemTuple[0])
					#getattr(
					#	self.DoClass.__bases__[0],
					#	__MethodItemTuple[0]
					#)!=__MethodItemTuple[1]
					#if hasattr(self.DoClass.__bases__[0],
					#	__MethodItemTuple[0]
					#) else True
				),
				self.DoClass.InspectMethodDict.items()
			)
		)

		#Debug
		'''
		print('Classer l 147')
		print('self.DoClass is ')
		print(self.DoClass)
		print('ClassedPropertyNewMethodDict is')
		print(SYS.indent(ClassedPropertyNewMethodDict))
		print('')
		'''
		
		#map
		ClassedPropertyKeyStrsList=map(
				lambda __PropertizedKeyStr:
				SYS.deprefix(
					__PropertizedKeyStr,
					Propertiser.PropertyPrefixStr
				)[3:],
				ClassedPropertyNewMethodDict.keys()
			)

		#map reset the properties
		map(
				lambda __PropertyKeyStr:
				setattr(
						self.DoClass,
						__PropertyKeyStr,
						property(
								getattr(
									self.DoClass,
									Propertiser.PropertyPrefixStr+'get'+__PropertyKeyStr
								),
								getattr(
									self.DoClass,
									Propertiser.PropertyPrefixStr+'set'+__PropertyKeyStr
								),
								getattr(
									self.DoClass,
									Propertiser.PropertyPrefixStr+'del'+__PropertyKeyStr
								)
							)
					),
				ClassedPropertyKeyStrsList
			)

		#/###################/#
		# Set maybe a structure 
		#

		#Check
		if hasattr(self.DoClass,"StructuresOrderedDict")==False:
			self.DoClass.StructuresOrderedDict = collections.OrderedDict()

		#Check
		if self.ClassingStructureVariable!=None:

			#Debug
			'''
			print("Before")
			print(id(self.DoClass.StructuresOrderedDict))
			print("self.DoClass is ")
			print(self.DoClass)
			print("self.DoClass.StructuresOrderedDict is ")
			print(self.DoClass.StructuresOrderedDict)
			#print("ClassesDict is ")
			#SYS._print(ClassesDict)
			print("")
			'''

			#Check
			if hasattr(
					self.ClassingStructureVariable,'items'
				):
				ClassedStructureVariable=self.ClassingStructureVariable.items()
			else:
				ClassedStructureVariable=self.ClassingStructureVariable

			#debug
			'''
			print('Classer l 241')
			print('We structure here')
			print('self.ClassingStructureVariable is ')
			print(self.ClassingStructureVariable)
			print('')
			'''

			#map add the sing plurals
			map(
				lambda __ItemTuple:
				SYS.addSingPlural(
					*__ItemTuple
				),
				ClassedStructureVariable
			)

			#Define a class
			class StructureClass(SYS.StructurerClass):pass
			StructureClass.__name__ = SYS.getClassStrWithNameStr(
				self.DoClass.NameStr+'sStructurer'
			)
			StructureClass.ManagingValueClass = self.DoClass

			#set
			setattr(
				self.Module,
				StructureClass.__name__,
				StructureClass
			)

			#dict
			ClassesDict=dict(
					map(
						lambda __ItemTuple:
						(__ItemTuple[1],StructureClass),
						ClassedStructureVariable
					)
				)

			#map
			if self.DoClass.TeamingClassesDict==None:
				self.DoClass.TeamingClassesDict = dict() 
			self.DoClass.TeamingClassesDict.update(
				ClassesDict
			)

			
			#set
			DoMethodStr = self.DoClass.DoStr[0].lower()+self.DoClass.DoStr[1:]

			#update
			self.DoClass.StructuresOrderedDict[
				DoMethodStr
			] = ClassesDict

			#Debug
			'''
			print(id(self.DoClass.StructuresOrderedDict))
			print("self.DoClass is ")
			print(self.DoClass)
			print("self.DoClass.StructuresOrderedDict is ")
			print(self.DoClass.StructuresOrderedDict)
			print("ClassesDict is ")
			SYS._print(ClassesDict)
			print("DoMethodStr is ")
			print(DoMethodStr)
			print("")
			'''


#</DefineClass>

