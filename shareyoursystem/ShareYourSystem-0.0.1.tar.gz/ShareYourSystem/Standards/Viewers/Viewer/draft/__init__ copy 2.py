# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Viewer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Numscipyer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo("Viewer","View","Viewing","Viewed")
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Controllers import Controller
import copy
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class ViewerClass(BaseClass):
	
	def default_init(self, 
						_ViewDeriveControllerVariable=None,
						_ViewFirstDeriveViewerVariable=None,
						_ViewingXVariable=None,
						_ViewingYVariable=None,
						_ViewingIdStr="",
						_ViewingXScaleFloat=1.,
						_ViewingYScaleFloat=1.,
						_ViewingXLabelStr="",
						_ViewingYLabelStr="",
						_ViewedTagStr="",
						_ViewedXTagStr="",
						_ViewedYTagStr="",
						_ViewedHtmlStr="",
						_ViewedLegendLabelStr="",
						_ViewedXLabelStr="",
						_ViewedYLabelStr="",
						_ViewedXlimLiargStr="",
						_ViewedYlimLiargStr="",
						_ViewedXtickLiargStr="",
						_ViewedYtickLiargStr="",
						_ViewedXtickLabelLiargStr="",
						_ViewedYtickLabelLiargStr="",
						**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#init
		self.ViewDeriveControllerVariable=self

	def do_view(self):

		#debug
		'''
		self.debug(
				[
					'We view here',
					('self.',self,[
						'ViewingQtBool'
					])
				]
			)
		'''

		#Check
		if self.ViewingIdStr=="":
			self.ViewingIdStr=str(self.PrintIdInt)

		#debug
		self.debug(
			[
				"id(self) is ",
				str(id(self)),
				('self.',self,['ViewingIdStr']),
				'SYS.IdDict["+self.ViewingIdStr+"]',
				SYS._str(SYS.IdDict[int(self.ViewingIdStr)]),
				#SYS._str(SYS.IdDict[id(self)]),
				('self.',self,[
					'ViewingXVariable',
					'ViewingYVariable'
				])
			]
		)

		#set
		self.ViewedTagStr=self.StructureTagStr.replace('*','')

		#/####################/#
		# Now we view each Axe
		#

		#map
		map(
			lambda __AxeStr:
			self.viewAxe(__AxeStr),
			[
				'X',
				'Y'
			]
		)


		"""
		#/##################/#
		# Set the X axis
		#

		#set
		self.ViewedXTagStr=self.ViewedTagStr+'X'

		#join
		self.ViewedXlimLiargStr="".join([
						">>SYS.set(SYS,'"+self.ViewedXTagStr+"LimFloatsArray',",
						"[SYS.IdDict["+self.ViewingIdStr+"].ViewingXVariable.min(),",
						"SYS.IdDict["+self.ViewingIdStr+"].ViewingXVariable.max()]",
						').'+self.ViewedXTagStr+"LimFloatsArray"
						])

		#join
		self.ViewedXtickLiargStr="".join([
						">>SYS.set(SYS,'"+self.ViewedXTagStr+"TickFloatsArray',",
						"map(lambda __Float:float('%.2f'%__Float),",
						"SYS.getTickFloatsArray(",
						'SYS.'+self.ViewedXTagStr+"LimFloatsArray,3",
						")))."+self.ViewedXTagStr+"TickFloatsArray"
						])

		self.ViewedXtickLabelLiargStr="".join([
						">>SYS.set(SYS,'"+self.ViewedXTagStr+"TickStrsArray',",
						"map(lambda __Float:'$'+str(self.ViewingXScaleFloat*__Float)+'$',",
						"SYS."+self.ViewedXTagStr+"TickFloatsArray))."+self.ViewedXTagStr+"TickStrsArray"
						])
				
		#debug
		'''
		self.debug(
			[
				'In the end of the set of the x axis',
				(
					'self.',self,[
						'ViewedLegendLabelStr',
						'ViewedXLabelStr',
						'ViewedXlimLiargTagStr',
						'ViewedXtickLiargStr',
						'ViewedXtickLabelLiargStr'
					]
				)
			]
		)
		'''

		#/##################/#
		# Set the Y axis
		#

		#set
		self.ViewedYTagStr=self.ViewedTagStr+'Y'

		#join
		self.ViewedYlimLiargStr="".join([
						">>SYS.set(SYS,'"+self.ViewedYTagStr+"LimFloatsArray',",
						"[SYS.IdDict["+self.ViewingIdStr+"].ViewingYVariable.min(),",
						"SYS.IdDict["+self.ViewingIdStr+"].ViewingYVariable.max()]",
						').'+self.ViewedYTagStr+"LimFloatsArray"
						])

		#join
		self.ViewedYtickLiargStr="".join([
						">>SYS.set(SYS,'"+self.ViewedYTagStr+"TickFloatsArray',",
						"map(lambda __Float:float('%.2f'%__Float),",
						"SYS.getTickFloatsArray(",
						'SYS.'+self.ViewedYTagStr+"LimFloatsArray,3",
						")))."+self.ViewedYTagStr+"TickFloatsArray"
						])

		self.ViewedYtickLabelLiargStr="".join([
						">>SYS.set(SYS,'"+self.ViewedYTagStr+"TickStrsArray',",
						"map(lambda __Float:'$'+str(self.ViewingYScaleFloat*__Float)+'$',",
						"SYS."+self.ViewedYTagStr+"TickFloatsArray))."+self.ViewedYTagStr+"TickStrsArray"
						])
				
		#debug
		'''
		self.debug(
			[
				'ViewedLegendLabelStr',
				'ViewedYLabelStr',
				'ViewedYlimLiargTagStr',
				'ViewedYtickLiargStr',
				'ViewedYtickLabelLiargStr'
			]
		)
		'''
		"""

	def viewAxe(self,_AxeStr):


		#/##################/#
		# Set a certain axis
		#

		#set
		ViewedTagStr=self.ViewedTagStr+_AxeStr

		#set
		setattr(
			self,
			'Viewed'+_AxeStr+'TagStr',
			ViewedTagStr
		)

		#join

		setattr(
			self,
			'Viewed'+_AxeStr+'limLiargStr',
			"".join([
						">>SYS.set(SYS,'"+ViewedTagStr+"LimFloatsArray',",
						"[SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"Variable.min(),",
						"SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"Variable.max()]",
						').'+ViewedTagStr+"LimFloatsArray"
						])
		)

		#join
		setattr(
			self,
			'Viewed'+_AxeStr+'tickLiargStr',
			"".join([
						">>SYS.set(SYS,'"+ViewedTagStr+"TickFloatsArray',",
						"map(lambda __Float:float('%.2f'%__Float),",
						"SYS.getTickFloatsArray(",
						'SYS.'+ViewedTagStr+"LimFloatsArray,3",
						")))."+ViewedTagStr+"TickFloatsArray"
						])
		)

		#set
		setattr(
			self,
			'Viewed'+_AxeStr+'tickLabelLiargStr',
			"".join([
						">>SYS.set(SYS,'"+ViewedTagStr+"TickStrsArray',",
						"map(lambda __Float:'$'+str(self.Viewing"+_AxeStr+"ScaleFloat*__Float)+'$',",
						"SYS."+ViewedTagStr+"TickFloatsArray))."+ViewedTagStr+"TickStrsArray"
						])
		)
				
		#debug
		'''
		self.debug(
			[
				'In the end of the set of the x axis',
				(
					'self.',self,[
						'ViewedLegendLabelStr',
						'Viewed'+_AxeStr+'LabelStr',
						'Viewed'+_AxeStr+'limLiargTagStr',
						'Viewed'+_AxeStr+'tickLiargStr',
						'Viewed'+_AxeStr+'tickLabelLiargStr'
					]
				)
			]
		)
		'''

#</DefineClass>

#<DefineLocals>
Controller.ViewsClass.ManagingValueClass=ViewerClass
#<DefineLocals>

#</DefinePrint>
ViewerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ViewDeriveControllerVariable',
		'ViewFirstDeriveViewerVariable',
		'ViewingXVariable',
		'ViewingYVariable',
		'ViewingIdStr',
		'ViewingXScaleFloat',
		'ViewingYScaleFloat',
		'ViewingXLabelStr',
		'ViewingYLabelStr',
		'ViewedTagStr',
		'ViewedHtmlStr',
		'ViewedLegendLabelStr',
		'ViewedXLabelStr',
		'ViewedYLabelStr',
		'ViewedXlimLiargStr',
		'ViewedYlimLiargStr',
		'ViewedXtickLiargStr',
		'ViewedYtickLiargStr',
		'ViewedXtickLabelLiargStr',
		'ViewedYtickLabelLiargStr'
	]
)
#<DefinePrint>
