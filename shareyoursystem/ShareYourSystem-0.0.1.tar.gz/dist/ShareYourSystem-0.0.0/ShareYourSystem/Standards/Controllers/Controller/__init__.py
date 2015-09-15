# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Controller

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Hdformater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Controller','Control','Controlling','Controlled')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Itemizers import Structurer
#</ImportSpecificModules>

#<DefineLocals>
class ModelsClass(Structurer.StructurerClass):pass
class ViewsClass(Structurer.StructurerClass):pass
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ControllerClass(BaseClass):

	def default_init(self,
				_ControlTagStr="Top",
				_ControlComponentDeriveControllersList=None,
				**_KwargVariablesDict
			):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_control(self):
		
		#debug
		'''
		self.debug(
				[
					'We control here',
					'First make parent the components
				]
			)
		'''

		"""
		#/##########################/#
		# ParentDown the Components first
		#

		#first parent the components
		self.parentDown(
			['Components']
		)

		#debug
		self.debug(
				[
					'Ok we have parented the components',
					('self.',self,[
						'ControlComponentDeriveControllersList'
					])
				]
			)

		#reverse
		#self.ControlComponentDeriveControllersList.reverse()

		#map
		map(
			lambda __ControlledComponentDeriveController:
			__ControlledComponentDeriveController.parentDown(
					['Models']
				),
			self.ControlComponentDeriveControllersList
		)
		"""

		#/##########################/#
		# ParentDown the Components first
		#
		
		#debug
		self.debug(
			[
				'We network in the components and the models'
			]
		)

		#parentDown
		self.network(
			[
				'Components',
				'Models'
			]
		)


	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#call the base method
		BaseClass.propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable)

		#/##################/#
		# Set the ControlTagStr
		#

		#debug
		'''
		self.debug(
				[
					'We have parented',
					'we set the control path str',
					('self.',self,[
							'ParentedTotalPathStr',
							'ManagementTagStr'
						])
				]
			)
		'''
		
		#Check
		if self.ManagementTagStr!='':

			#get
			self.ControlTagStr=(
					self.ParentedTotalPathStr+'/'+self.ManagementTagStr
				).replace('/','_')

		#remove
		if self.ControlTagStr[0]=='_':
			self.ControlTagStr=self.ControlTagStr[1:]

		#/##################/#
		# Add to the top Controller
		#

		if self.ParentTopDeriveTeamerVariable.ControlComponentDeriveControllersList==None:
			self.ParentTopDeriveTeamerVariable.ControlComponentDeriveControllersList=[self]
		else:
			self.ParentTopDeriveTeamerVariable.ControlComponentDeriveControllersList.append(
				self
			)

#</DefineClass>

#<DefineLocals>

#Set
ControllerClass.TeamingClassesDict={
	'Components':Structurer.StructurerClass,
	'Models':ModelsClass,
	'Views':ViewsClass
}

#<DefineLocals>

#</DefinePrint>
ControllerClass.PrintingClassSkipKeyStrsList.extend(
	[
		#'ControlTagStr',
		'ControlComponentDeriveControllersList'
	]
)
#<DefinePrint>



