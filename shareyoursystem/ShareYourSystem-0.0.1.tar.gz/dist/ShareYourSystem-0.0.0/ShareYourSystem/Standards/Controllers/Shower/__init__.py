# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Displayer
"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Controllers.Drawer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Shower','Show','Showing','Shown')
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ShowerClass(BaseClass):

	def default_init(self,
						_ShowingQtBool=True,
						_ShowingMpld3Bool=False,
						**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_show(self):

		#debug
		self.debug(
			[
				'We show here',
				'first network'
			]
		)

		#/##################/#
		# First network
		#

		#network all the view things
		self.network(
			[
				'Views',
				'Panels',
				'Axes',
				'Plots'
			],
			_DoStr='Show'
		)

		#/##################/#
		# Then show the figure
		#

		#debug
		'''
		self.debug(
				[
					'We show with which device',
					('self.',self,['ShowingQtBool'])
				]
			)
		'''

		#Check
		if self.ShowingQtBool:

			#import
			from matplotlib import pyplot

			#show
			pyplot.show()

		if self.ShowingMpld3Bool:

			#import
			import mpld3

			#show
			mpld3.show()

#</DefineClass>

#</DefinePrint>
ShowerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ShowingQtBool',
		'ShowingMpld3Bool'
	]
)
#<DefinePrint>
