# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Storer instances

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Controllers.Organizer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Modelers import Hierarchizer
from ShareYourSystem.Standards.Noders import Noder
import operator
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class StorerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								'StoringOrganizeIsBool'
							]

	def default_init(self,
						_StoringOrganizeIsBool=False,
						_StoringInsertIsBool=True,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_store(self):

		#Check
		if self.StoringOrganizeIsBool==False:

			#organize
			self.organize()

			#Walk
			self.walk(
				{
					'AfterUpdateList':[
						(
							'organize',
							SYS.ApplyDictClass({'LiargVariablesList':[]})
						)
					],
					'GatherVariablesList':[self.OrganizedComponentsGetStr]
				}
			)

			#structure
			self.structure(
					[self.OrganizingComponentsCollectionStr]
				)

			#network
			self.network(
					**{
						'VisitingCollectionStrsList':[
							self.OrganizingModelsCollectionStr,
							self.OrganizingComponentsCollectionStr
						],
						'RecruitingConcludeConditionVariable':[
							(
								'MroClassesList',
								operator.contains,Hierarchizer.HierarchizerClass
							)
						]
					}
				)

			#set
			self.StoringOrganizeIsBool=True

		#Check
		if self.StoringInsertIsBool:

			#Walk
			self.walk(
				{
					'AfterUpdateList':[
						(
							'callDo',
							SYS.ApplyDictClass(
								{'LiargVariablesList':[]}
							)
						)
					],
					'GatherVariablesList':[self.OrganizedComponentsGetStr]
				}
			)

			#debug
			'''
			self.debug(('self.',self,['OrganizedTopDeriveDatabaserVariable']))
			'''

			#insert
			self.OrganizedTopDeriveDatabaserVariable.insert()	
		
#</DefineClass>

