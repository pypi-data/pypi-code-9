# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Merger instances help for reloading rowed variables from
different tables but with different shaping variables. 
The results is a list of rowed items from merged tables.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Shaper"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
Shaper=BaseModule
from ShareYourSystem.Standards.Modelers import Tabler,Rower,Recoverer
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class MergerClass(BaseClass):
	
	def default_init(self,
					_MergingConditionVariable=None, 		
					_MergedRowedDictsList=None,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_merge(self):

		#Check
		if self.ModelingHdfBool:

			#debug
			'''
			self.debug(
						('self.',self,[
											'ModeledKeyStr',
											'MergingConditionVariable',
											'TabularedTableKeyStrsList'
										])
					)
			'''

			#Debug
			'''
			print(

					map(
								lambda __TabularedKeyStr:
							__TabularedKeyStr.split(Shaper.ShapingJoiningStr),
							self.TabularedTableKeyStrsList
						)
				)
			'''
			
			#Bind with MergedShapingDictsList setting
			MergedShapingDictsList=map(
									lambda __StrsList:
									dict(
										map(
												lambda __ShapingStr:
												SYS.getUnSerializedTuple(
													self.NodePointDeriveNoder,
													__ShapingStr.split(
														Shaper.ShapingTuplingStr
													)
												)
												#Remove the suffix and the prefix
												,__StrsList[1:-1] if len(__StrsList)>2 else []
											)
									),
									map(
										lambda __TabularedKeyStr:
										__TabularedKeyStr.split(Shaper.ShapingJoiningStr),
										self.TabularedTableKeyStrsList
									)
							)

			#debug
			'''
			self.debug('MergedShapingDictsList is '+str(MergedShapingDictsList))
			'''

			#Bind with MergedFilteredShapingDictsList
			MergedFilteredShapingDictsList=SYS.where(
										MergedShapingDictsList,
										self.MergingConditionVariable
										)

			#debug
			'''
			self.debug('MergedFilteredShapingDictsList is '+str(MergedFilteredShapingDictsList))
			'''

			#Bind with MergedTablesList setting
			MergedTablesList=SYS.filterNone(
										map(
												lambda __Table,__MergedFilteredShapingDict:
												__Table
												if __MergedFilteredShapingDict!=None
												else None,
												self.TabularedTablesOrderedDict.values(),
												MergedFilteredShapingDictsList
										))
									
			MergedRowedDictsListsList=map(
					lambda __MergedTable:
					map(
							lambda __RowedDict:
							dict(__RowedDict,**{
									'TabledInt':int(
													__MergedTable.name.split(Tabler.TablingOrderStr)[1]
												)
								}
							),
							Rower.getRowedDictsListWithTable(__MergedTable)
						),
					MergedTablesList
				)

			#debug
			'''
			self.debug('MergedRowedDictsListsList is '+str(MergedRowedDictsListsList))
			'''
			
			#Reduce
			if len(MergedRowedDictsListsList)>0:
				self.MergedRowedDictsList=reduce(operator.__add__,MergedRowedDictsListsList)

	def mimic_find(self):

		#merge first
		self.merge()

		#Bound the FoundRowDictsList with the MergedRowedDictsList one
		self.FoundRowDictsList=self.MergedRowedDictsList

		#find then
		BaseClass.find(self)

#</DefineClass>

#</DefinePrint>
MergerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'MergingConditionVariable',									
		'MergedRowedDictsList'
	]
)
#<DefinePrint>
