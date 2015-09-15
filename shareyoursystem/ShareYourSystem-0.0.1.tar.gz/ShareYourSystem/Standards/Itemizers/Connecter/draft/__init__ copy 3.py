# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Pointer 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Parenter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Itemizers import Pather,Teamer,Manager,Parenter
#</ImportSpecificModules>

#<DefineLocals>
PointPrefixStr="*"
PointToStr="->"
PointBackStr="<->"
PointBackPrefixStr="Back"
PointInTeamStr="Inlets"
PointOutTeamStr="Outlets"
PointConnectKeyStr='?>'
def getLiargVariablesList(_ValueVariable):
	return _ValueVariable
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PointerClass(BaseClass):

	def default_init(
					self,	
					_PointGetVariable=None,
					_PointingKeyVariable=None,
					_PointingSetVariable=None,
					_PointingValueClass=BaseClass,
					_PointingInTeamStr="Inlets",
					_PointingOutTeamStr="Outlets",
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_point(self):

		#/####################/#
		# Adapt the type for getting things to point
		#

		#debug
		'''
		self.debug(
			[
				'Adapt the type for getting things to point',
				("self.",self,[
								'PointingKeyVariable',
							])
			]
		)
		'''


		#init
		PointedValueVariablesList=SYS.GetList(
			self.PointingKeyVariable,
			self
		)

		#debug
		self.debug(
				[
					'in the end, PointedValueVariablesList is ',
					SYS._str(PointedValueVariablesList)
				]
			)

		#/####################/#
		# Adapt the type for setting things in the commanded variables
		#

		#debug
		'''
		self.debug(
			[
				'Adapt the type for setting things in the pointed variables',
				("self.",self,['PointingSetVariable'])
			]
		)
		'''

		#inits
		PointingSetVariablesList=SYS.SetList(self.PointingSetVariable)

		#debug
		self.debug(
				[
					'in the end, PointingSetVariablesList is ',
					SYS._str(PointingSetVariablesList)
				]
			)

		#/####################/#
		# Now store all this things in the outlets team
		#

		#debug
		self.debug(
				[
					'Now we team all that stuff'
				]
			)

		#get
		PointedDeriveParenterVariable=

		self.TeamDict[
			self.PointingOutTeamStr
		].manage(
				self.getManagingKeyStr(self.PointingKeyVariable),
				SYS.update(
					[('PointVariablesList',PointedValueVariablesList)],
					__PointingSetVariable,
				),
				_ValueClass=self.PointingValueClass
			)

		#map
		map(
			lambda __PointedValueVariable,__PointingSetVariable:
			,
			PointedValueVariablesList,
			PointingSetVariablesList
		)




#</DefineClass>

#<DefineLocals>

#set
Parenter.ParenterClass.ManagingValueClass=PointerClass

#</DefineLocals>

#</DefinePrint>
PointerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PointVariablesList',
		'PointingKeyVariable',
		'PointingSetVariable',
		'PointingInTeamStr',
		'PointingOutTeamStr',
		'PointingValueClass'
	]
)
#<DefinePrint>
