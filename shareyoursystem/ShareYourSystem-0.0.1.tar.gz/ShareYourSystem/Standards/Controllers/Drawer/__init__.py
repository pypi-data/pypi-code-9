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
BaseModuleStr="ShareYourSystem.Standards.Controllers.Controller"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Drawer','Draw','Drawing','Drawn')
#</DefineAugmentation>

#<ImportSpecificModules>
import operator
from ShareYourSystem.Standards.Viewers import Pyploter
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class DrawerClass(BaseClass):

	def default_init(self,
						_DrawingSetVariable=None,
						**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_draw(self):

		#team
		self.team('Views')

		#map set
		self.TeamDict['Views']['#map@set'](
			self.DrawingSetVariable
		)

	def getTickTuplesList(self):

		return [
			(
				'set_ylim',
				{
					'#liarg:#map@get':[
					"".join([
						">>SYS.set(SYS,'SensorLimFloatsArray',",
						"[-0.1,1.5*self.PredisensingClampFloat*self.PredictingConstantTimeFloat]",
						').SensorLimFloatsArray'
						])
					]
				}
			),
			(
				'set_yticks',
				{
					'#liarg:#map@get':[
					"".join([
						">>SYS.set(SYS,'SensorTickFloatsArray',",
						"map(lambda __Float:float('%.2f'%__Float),",
						"SYS.getTickFloatsArray(",
						"SYS.SensorLimFloatsArray,3",
						"))).SensorTickFloatsArray"
						])
					]
				}
			),
			(
				'set_yticklabels',
				{
					'#liarg:#map@get':[
					"".join([
						">>SYS.set(SYS,'SensorTickStrsArray',",
						"map(lambda __Float:'$'+str(__Float)+'$',",
						"SYS.SensorTickFloatsArray)).SensorTickStrsArray"
						])
					]
				}
			)
		]

#</DefineClass>

#</DefinePrint>
DrawerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'DrawingSetVariable'
	]
)
#<DefinePrint>
