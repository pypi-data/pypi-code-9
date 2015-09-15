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

#<DefineLocals>
ViewAlphabetStr="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#</DefineLocals>

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
						_ViewingColorStrsList=None,
						_ViewingLabelStrsList=None,
						_ViewingAddXMinFloat=0.,
						_ViewingAddXMaxFloat=0.,
						_ViewingAddYMinFloat=0.,
						_ViewingAddYMaxFloat=0.,
						_ViewingXIndexBool=False,
						_ViewingYIndexBool=False,
						_ViewingXSampleInt=3,
						_ViewingYSampleInt=3,
						_ViewedTagStr="",
						_ViewedXTagStr="",
						_ViewedYTagStr="",
						_ViewedHtmlStr="",
						_ViewedLegendLabelStr="",
						_ViewedXLabelStr="",
						_ViewedYLabelStr="",
						_ViewedXlimMinStrsList=None,
						_ViewedXlimMaxStrsList=None,
						_ViewedYlimMinStrsList=None,
						_ViewedYlimMaxStrsList=None,
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

		#Check
		if self.ViewingIdStr=="":
			self.ViewingIdStr=str(self.PrintIdInt)

		#set
		#self.ViewedTagStr='_'+self.ViewingIdStr+'_'+self.StructureTagStr.replace('*','')
		self.ViewedTagStr='_'+self.ViewingIdStr+'_'

		#debug
		'''
		self.debug(
				[
					'We view here',
					('self.',self,[
						'ViewingIdStr',
						'ViewedTagStr'
						]
					),
				#"id(self) is ",
				#str(id(self)),
				#('self.',self,['ViewingIdStr']),
				#'SYS.IdDict["+self.ViewingIdStr+"]',
				#SYS._str(SYS.IdDict[int(self.ViewingIdStr)]),
				#SYS._str(SYS.IdDict[id(self)]),
				#('self.',self,[
				#	'ViewingXVariable',
				#	'ViewingYVariable'
				#])
			]
		)
		'''

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

		#get
		LimMinStrsList=getattr(
			self,
			'Viewed'+_AxeStr+'limMinStrsList'
		)
		if LimMinStrsList==None:
			LimMinStrsList=[]

		LimMinStrsList.append(
			"SYS.getExtremumFloat(SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"Variable,'min')"
		)

		#get 
		LimMaxStrsList=getattr(
			self,
			'Viewed'+_AxeStr+'limMaxStrsList'
		)
		if LimMaxStrsList==None:
			LimMaxStrsList=[]
		LimMaxStrsList.append(
			"SYS.getExtremumFloat(SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"Variable,'max')"
		)

		#get
		ViewingAddMinFloat=getattr(self,'ViewingAdd'+_AxeStr+'MinFloat')
		ViewingAddMaxFloat=getattr(self,'ViewingAdd'+_AxeStr+'MaxFloat')

		#debug
		'''
		self.debug(
			[
				'ViewingAddMinFloat is '+str(ViewingAddMinFloat),
				'ViewingAddMaxFloat is '+str(ViewingAddMaxFloat)
			]
		)
		'''

		#set
		setattr(
			self,
			'Viewed'+_AxeStr+'limLiargStr',
			"".join([
				">>SYS.set(SYS,'"+ViewedTagStr+"LimFloatsArray',",
				"[",
				#"SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"Variable.min()",
				"min("+",".join(LimMinStrsList)+")"+'+'+str(ViewingAddMinFloat)
				if len(LimMinStrsList)>1
				else LimMinStrsList[0]+'+('+str(ViewingAddMinFloat)+')',
				",",
				#"SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"Variable.max()]",
				"max("+",".join(LimMaxStrsList)+")"+'+'+str(ViewingAddMaxFloat)
				if len(LimMaxStrsList)>1
				else LimMaxStrsList[0]+'+('+str(ViewingAddMaxFloat)+')',
				']).'+ViewedTagStr+"LimFloatsArray"
			])
		)


		#debug
		'''
		self.debug(
			[
				"getattr(self,'Viewed'+_AxeStr+'limLiargStr') is",
				getattr(self,'Viewed'+_AxeStr+'limLiargStr')
			]
		)
		'''
		
		#get
		ViewedIndexBool=getattr(
			self,
			'Viewing'+_AxeStr+'IndexBool'
		)

		#join
		if ViewedIndexBool:
			setattr(
				self,
				'Viewed'+_AxeStr+'tickLiargStr',
				"".join([
							">>SYS.set(SYS,'"+ViewedTagStr+"TickVariablesArray',",
							"SYS.getTickIntsArray(",
							'SYS.'+ViewedTagStr+"LimFloatsArray,"+str(
								getattr(self,'Viewing'+_AxeStr+'SampleInt')
							),
							"))."+ViewedTagStr+"TickVariablesArray"
							])
			)

		else:
			setattr(
				self,
				'Viewed'+_AxeStr+'tickLiargStr',
				"".join([
							">>SYS.set(SYS,'"+ViewedTagStr+"TickVariablesArray',",
							"map(lambda __Float:float(SYS.getFloatStr(__Float)),",
							"SYS.getTickFloatsArray(",
							'SYS.'+ViewedTagStr+"LimFloatsArray,"+str(
								getattr(self,'Viewing'+_AxeStr+'SampleInt')
							),
							")))."+ViewedTagStr+"TickVariablesArray"
							])
			)

		#debug
		'''
		self.debug(
			[
				'Scale the tick labels',
				('self.',self,[
						"Viewing"+_AxeStr+"ScaleFloat"
					])
			]
		)
		'''

		#Check
		if ViewedIndexBool:

			#set
			setattr(
				self,
				'Viewed'+_AxeStr+'tickLabelLiargStr',
				"".join([
							">>SYS.set(SYS,'"+ViewedTagStr+"TickStrsArray',",
							"map(lambda __Float:'$'+str(int(SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"ScaleFloat*__Float))+'$',",
							#"map(lambda __Float:'$'+str(self.Viewing"+_AxeStr+"ScaleFloat*__Float)+'$',",
							"SYS."+ViewedTagStr+"TickVariablesArray))."+ViewedTagStr+"TickStrsArray"
							])
			)
		else:

			#set
			setattr(
				self,
				'Viewed'+_AxeStr+'tickLabelLiargStr',
				"".join([
							">>SYS.set(SYS,'"+ViewedTagStr+"TickStrsArray',",
							"map(lambda __Float:'$'+SYS.getFloatStr(SYS.IdDict["+self.ViewingIdStr+"].Viewing"+_AxeStr+"ScaleFloat*__Float)+'$',",
							#"map(lambda __Float:'$'+str(self.Viewing"+_AxeStr+"ScaleFloat*__Float)+'$',",
							"SYS."+ViewedTagStr+"TickVariablesArray))."+ViewedTagStr+"TickStrsArray"
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

	def getLabelStr(self,_VariableStr):

		#Check
		if '_' in _VariableStr:
			ViewedWordStrsList=_VariableStr.split('_')
			return ViewedWordStrsList[0]+'_{'+",".join(ViewedWordStrsList[1:])+'}'
		else:
			return _VariableStr


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
		'ViewingColorStrsList',
		'ViewingLabelStrsList',
		'ViewingAddXMinFloat',
		'ViewingAddXMaxFloat',
		'ViewingAddYMinFloat',
		'ViewingAddYMaxFloat',
		'ViewingXIndexBool',
		'ViewingYIndexBool',
		'ViewingXSampleInt',
		'ViewingYSampleInt',
		'ViewedTagStr',
		'ViewedXTagStr',
		'ViewedYTagStr',
		'ViewedHtmlStr',
		'ViewedLegendLabelStr',
		'ViewedXLabelStr',
		'ViewedYLabelStr',
		'ViewedXlimMinStrsList',
		'ViewedXlimMaxStrsList',
		'ViewedYlimMinStrsList',
		'ViewedYlimMaxStrsList',
		'ViewedXlimLiargStr',
		'ViewedYlimLiargStr',
		'ViewedXtickLiargStr',
		'ViewedYtickLiargStr',
		'ViewedXtickLabelLiargStr',
		'ViewedYtickLabelLiargStr'
	]
)
#<DefinePrint>
