# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Pyploter

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Viewers.Viewer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo("Pyploter","Pyplot","Pyploting","Pyploted")
#</DefineAugmentation>

#<ImportSpecificModules>
Viewer=BaseModule
from ShareYourSystem.Standards.Interfacers import Printer
from ShareYourSystem.Standards.Itemizers import Setter,Manager
from ShareYourSystem.Standards.Controllers import Controller
import copy
#</ImportSpecificModules>

#<DefineLocals>
PyplotPlotKeyStr='#plot'
PyplotBarKeyStr='#bar'
PyplotScatterKeyStr='#scatter'
PyplotAxesKeyStr='#axes'
PyplotMpld3KeyStr='#mpld3.plugins.'
def getFiguresList():

	#import 
	import matplotlib._pylab_helpers

	#return
	return [
		Manager.canvas.figure for Manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()
	]
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['pyplot'],
	'ClassingStructureVariable':[
		('Panel','Panels'),
		('Chart','Charts'),
		('Draw','Draws')
	]
})
class PyploterClass(BaseClass):
	
	def default_init(self,
						_PyplotTooltipVariablesList=None,
						_PyplotingXVariable=None,
						_PyplotingYVariable=None,
						_PyplotingZVariable=None,
						_PyplotingCloseBool=True,
						_PyplotingGridVariable=None,
						_PyplotingSubplotInt=1,
						_PyplotingShapeVariable=None,
						_PyplotingFigureVariable=None,
						_PyplotingDrawVariable=None,
						_PyplotingChartVariable=None,
						_PyplotingShiftVariable=None,
						_PyplotingPrintBool=True,
						_PyplotingLabelStr="",
						_PyplotingLegendDict=None,
						_PyplotingTextVariable=None,
						_PyplotingXSkipTickBool=False,
						_PyplotingYSkipTickBool=False,
						_PyplotingMarkerVariable=None,
						_PyplotingColorVariable=None,
						_PyplotingFontVariable =None,
						_PyplotedSingleBool=False,
						_PyplotedTeamTagStr="",
						_PyplotedParentFigureDerivePyploterVariable=None,
						_PyplotedParentPanelDerivePyploterVariable=None,
						_PyplotedParentChartDerivePyploterVariable=None,						
						_PyplotedFigureVariable=None,
						_PyplotedAxesVariable=None,
						_PyplotedAxesList=None,
						_PyplotedLinesList=None,
						_PyplotedPreviousAnchorIntsList=[0,0],
						_PyplotedPreviousShapeIntsList=[0,0],
						_PyplotedAnchorIntsList=None,
						_PyplotedShiftVariablesList=None,
						_PyplotedHitIntsList=None,
						_PyplotedPanelShapeIntsList=None,
						_PyplotedShapeIntsList=[5,5],
						_PyplotedChartTuplesList=None,
						_PyplotedDrawTuplesList=None,
						_PyplotedParentSingularStr="",
						_PyplotedPreviousChartDerivePyploterVariable=None,
						_PyplotedPreviousPanelDerivePyploterVariable=None,
						_PyplotedTextIntsList=None,
						_PyplotedXVariable=None,
						_PyplotedYVariable=None,
						_PyplotedZVariable=None,
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_pyplot(self,**_KwargVariablesDict):	
		
		#/#################/#
		# Determine if it is an inside structure or the top
		#

		#debug
		'''
		self.debug(
			[
				'We pyplot here',
				'First look for deeper teams in the structure',
			]
		)
		'''

		#Check
		if self.ParentedTotalSingularListDict!=None and len(
			self.ParentedTotalSingularListDict
		)>0:

			#debug
			'''
			self.debug(
				[
					'self.ParentedTotalSingularListDict.keys() is ',
					str(self.ParentedTotalSingularListDict.keys())
				]
			)
			'''

			#get
			self.PyplotedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,['PyplotedParentSingularStr'])
			]
		)
		'''

		#/###############/#
		# Cases depending on the level
		#

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Panels' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Panels',
			'Charts',
			'Draws'
		]):

			#/########################/#
			# pyplotFigure
			#

			#call
			self.pyplotFigure(**_KwargVariablesDict)

			#/########################/#
			# structure pyplot
			# 

			#debug
			'''
			self.debug(
				[
					'We structure pyplot all the children...',
					'self.TeamDict.keys() is ',
					str(self.TeamDict.keys())
				]
			)
			'''

			#Check
			if self.PyplotedSingleBool:
				return

			#structure
			self.structure(
				[
					'Panels',
					'Charts',
					'Draws'
				],
				'#all',
				_ManagerCommandSetList=['pyplot']
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have structure Panels, Charts, Draws',
					'getFiguresList is ',
					str(getFiguresList())
				]
			)
			'''

		else:

			#/########################/#
			# Inside structure
			#

			#debug
			'''
			self.debug(
				[
					'Ok we check if this parentsingular has a special method ',
					('self.',self,[
						'PyplotedParentSingularStr'
					])
				]
			)
			'''

			#Check
			if self.ParentDeriveTeamerVariable.TeamTagStr=='Panels':

				#debug
				'''
				self.debug(
						[
							'Panel level.'
						]
					)
				'''

				#/#################/#
				# Determine the parent
				#

				#set
				self.PyplotedParentFigureDerivePyploterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

				#/#################/#
				# pyplotPanel
				#

				#debug
				'''
				self.debug(
					[
						'pyplotPanel'
					]
				)
				'''

				#pyplotPanel
				self.pyplotPanel()

			elif self.ParentDeriveTeamerVariable.TeamTagStr=='Charts':

				#debug
				'''
				self.debug(
						[
							'Chart level.',
							'determine the parent
						]
					)
				'''

				#/#################/#
				# Determine the parent
				#

				#Check
				if self.ParentDeriveTeamerVariable!=None:

					#Check
					if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable!=None:

						#Check
						if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.PyplotedParentSingularStr=='Panel':

							#debug
							'''
							self.debug(
								[
									'Ok there is a parent Panel for this Chart',
									'Check now for a parent figure'
								]
							)	
							'''

							#alias
							self.PyplotedParentPanelDerivePyploterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

							#alias
							self.PyplotedParentFigureDerivePyploterVariable=self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
				
						else:

							#alias
							self.PyplotedParentPanelDerivePyploterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

							#alias
							self.PyplotedParentFigureDerivePyploterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
								
							#debug
							'''
							self.debug(
									[
										'There is no Panel parent',
										'We set bigger PyplotingShapeVariable',
										('self.',self,[
												'PyplotingShapeVariable'
											])
									]
								)
							'''
								
				#debug
				'''
				self.debug(
					[
						'Ok for this Chart, we have determined the panel and figure parent',
						#('self.',self,[
						#	'PyplotedParentFigureDerivePyploterVariable'
						#])
					]
				)
				'''

				#/#################/#
				# Build the Axes
				#

				#debug
				'''
				self.debug(
					[
						'we set a Chart'
					]
				)
				'''

				#set Chart
				self.pyplotChart()

				#debug
				'''
				self.debug(
					[
						'we have setted the Chart here',
						('self.',self,[
							'PyplotedAxesVariable'
						])
					]
				)
				'''

			elif self.ParentDeriveTeamerVariable.TeamTagStr=='Draws':

				#debug
				'''
				self.debug(
						[
							'Draws level.'
						]
					)
				'''

				#/#################/#
				# Determine the parent
				#

				#set
				self.PyplotedParentChartDerivePyploterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

				#debug
				'''
				self.debug(
						[
							'self.PyplotedParentChartDerivePyploterVariable.PyplotedParentSingularStr is ',
							self.PyplotedParentChartDerivePyploterVariable.PyplotedParentSingularStr
						]
					)
				'''

				#Check
				if self.PyplotedParentChartDerivePyploterVariable.PyplotedParentSingularStr=='Panel':

					#set
					self.PyplotedParentPanelDerivePyploterVariable=self.PyplotedParentChartDerivePyploterVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
			
					#set
					self.PyplotedParentFigureDerivePyploterVariable=self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

				else:

					#debug
					'''
					self.debug(
							[
								'It is not a parent chart inside a panel ',
								'Look if the parent parent is actually the top
							]
						)
					'''

					#Check
					if self.PyplotedParentChartDerivePyploterVariable.ParentDeriveTeamerVariable!=None:
						
						#alias
						PyplotedParentFigurePanelDerivePyploterVariable=self.PyplotedParentChartDerivePyploterVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
						
						#Check
						if PyplotedParentFigurePanelDerivePyploterVariable!=None:

							#debug
							'''
							self.debug(
								[
									'Yes the parent parent is the top'
								]
							)
							'''

							#set
							self.PyplotedParentPanelDerivePyploterVariable=PyplotedParentFigurePanelDerivePyploterVariable
					
							#set
							self.PyplotedParentFigureDerivePyploterVariable=PyplotedParentFigurePanelDerivePyploterVariable

					else:

						#debug
						'''
						self.debug(
							[
								'Nope the parent parent not exist so direct set figure panel with chart parent'
							]
						)
						'''

						#set
						self.PyplotedParentPanelDerivePyploterVariable=self.PyplotedParentChartDerivePyploterVariable
					
						#set
						self.PyplotedParentFigureDerivePyploterVariable=self.PyplotedParentChartDerivePyploterVariable


				#debug
				'''
				self.debug(
					[
						'Ok for this Draw, we have determined the chart panel and figure parent',
						('self.',self,[
							'PyplotedParentFigureDerivePyploterVariable'
						])
					]
				)
				'''

				#pyplotDraw
				self.pyplotDraw()

		#debug
		'''
		self.debug(
			[
				'In the end',
				'getFiguresList is ',
				str(getFiguresList())
			]
		)
		'''

	def pyplotFigure(self,**_KwargVariablesDict):

		#debug
		"""
		self.debug(
			[
				'We pyplot figure here',
				('self.',self,[
						'PyplotedSingleBool',
						'PyplotedAxesVariable'
					])
			]
		)
		"""
		
		#Check
		if self.PyplotedSingleBool==False:

			#Check
			if self.PyplotingCloseBool:

				#/###############/#
				# Close the old ones
				#

				#get
				PyplotedOldFiguresList=getFiguresList()

				#debug
				'''
				self.debug(
					[
						'The old figures was',
						str(PyplotedOldFiguresList)
					]
				)
				'''

				#import
				from matplotlib import pyplot

				#map
				map(
					lambda __Figure:
					pyplot.close(__Figure),
					getFiguresList()
				)
			
			#/###############/#
			# If it is the top then init the pyplot
			#

			#debug
			'''
			self.debug(
					[
						'Figure Level'
					]
				)
			'''
			
			#import pyplot
			from matplotlib import pyplot

			#init
			if self.PyplotingFigureVariable!=None:

				#init
				self.PyplotedFigureVariable = pyplot.figure(
					**self.PyplotingFigureVariable
				)

			else:

				#init
				self.PyplotedFigureVariable = pyplot.figure()

			#/###############/#
			# Case of a Figure Panel Axes Draws 
			#

			#Check
			if all(
				map(
					lambda __KeyStr:
					__KeyStr not in self.TeamDict,
					['Charts','Panels']
				)
			):

				#/###############/#
				# Set parent 
				#

				#
				self.PyplotedParentFigureDerivePyploterVariable=self
				self.PyplotedParentPanelDerivePyploterVariable=self
				self.PyplotedParentChartDerivePyploterVariable=self

				#/###############/#
				# pyplotChart 
				#

				#debug
				self.debug(
					[
						'We are in the case of a Figure Panel Axes draw',
						('self.',self,[
							'PyplotingSubplotInt',
							'PyplotedAxesList'
						])
					]
				)

				#Check
				if 'Draws' not in self.TeamDict:

					#set
					self.PyplotedSingleBool=True

					#Check
					if len(self.PyplotedAxesList)==0 and self.PyplotingSubplotInt>0:

						#Check
						if self.PyplotingGridVariable==None:
							self.PyplotingGridVariable=(1,self.PyplotingSubplotInt)

						#set
						self.PyplotedAxesList=[
							None
						]*self.PyplotingGridVariable[0]*self.PyplotingGridVariable[1]


				else:

					#axes
					self.PyplotedAxesVariable=pyplot.axes()
					self.PyplotedAxesVariable._figure=self.PyplotedFigureVariable

					#/###############/#
					# pyplotDraw
					#

					#pyplotDraw
					self.pyplotDraw()

					#/#################/#
					# Look for view argument
					#

					#debug
					'''
					self.debug(
						[
							'First look for view arguments'
						]
					)
					'''

					#map
					map(
						lambda __AxeStr:
						self.pyplotAxe(__AxeStr),
						[
							'X',
							'Y'
						]
					)

					#debug
					'''
					self.debug(
						[
							'Ok we have maybe setted the PyplotingChartVariable',
							('self.',self,[
									'PyplotingChartVariable'
								]),
							'getFiguresList is ',
							str(getFiguresList())
						]
					)
					'''

		#Check
		if self.PyplotedSingleBool:


			#/###############/#
			# First get the axes
			#

			#debug
			'''
			self.debug(
				[
					'We get the axes',
					('self',self,[
							'PyplotedAxesList',
							'PyplotingSubplotInt'
						])
				]
			)
			'''
			
			#decrement
			PyplotedIndexInt=self.PyplotingSubplotInt-1

			#Check
			if self.PyplotedAxesList[PyplotedIndexInt]==None:

				#init
				self.PyplotedAxesList[PyplotedIndexInt] = self.PyplotedFigureVariable.add_subplot(
					self.PyplotingGridVariable[0],
					self.PyplotingGridVariable[1],
					self.PyplotingSubplotInt
				)

			#get
			self.PyplotedAxesVariable=self.PyplotedAxesList[
				PyplotedIndexInt
			]

			#debug
			'''
			self.debug(
				[
					'after pyplotDraw',
					'getFiguresList is ',
					str(getFiguresList())
				]
			)
			'''

			#/###############/#
			# pyplotDraw
			#

			#pyplotDraw
			self.pyplotDraw()

			#/###############/#
			# First get the option to set
			#

			#get
			map(
				lambda __AxisStr:
				setattr(
					self,
					'Pyploted'+__AxisStr+'Variable',
					self[	
						getattr(self,'Pyploting'+__AxisStr+'Variable')
					]
				)
				if type(
					getattr(self,'Pyploting'+__AxisStr+'Variable')
				)==str
				else None,
				[
					'X','Y','Z'
				]
			)

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'PyplotingXVariable',
							'PyplotingYVariable',
							'PyplotingZVariable',
							'PyplotedXVariable',
							'PyplotedYVariable',
							'PyplotedZVariable'
						])
				]
			)
			'''

			#map
			PyplotedListsList=map(
				lambda __PlotStr:
				[__PlotStr,'Pyploting'+__PlotStr+'Variable',None],
				[
					'Marker',
					'Color'
				]
			)

			#map
			map(
				lambda __PyplotedList:
				__PyplotedList.__setitem__(
					2,
					getattr(
						self,
						__PyplotedList[1]
					)
				),
				PyplotedListsList
			)

			#filter
			PyplotedListsList=SYS._filter(
				lambda __PyplotedList:
				type(
					__PyplotedList[2]
					)!=None.__class__,
				PyplotedListsList
			)
			
			#debug
			'''
			self.debug(
				[
					'PyplotedListsList is ',
					str(PyplotedListsList),
					self['#direct:o']
				]
			)
			'''

			#map
			map(
				lambda __PyplotedList:
				_KwargVariablesDict.__setitem__(
					__PyplotedList[0][0].lower()+__PyplotedList[0][1:],
					self[
						__PyplotedList[2]
					]
				),
				PyplotedListsList
			)
				
			#debug
			'''
			self.debug(
				[
					'We have setted the kwarg',
					'_KwargVariablesDict is '+str(_KwargVariablesDict)
				]
			)
			'''

			#Check
			if type(self.PyplotingZVariable)==None.__class__:

				if type(self.PyplotingYVariable)==None.__class__:

					#plot 
					self.PyplotedAxesVariable.plot(
						self.PyplotedXVariable,
						**_KwargVariablesDict
					)

				else:

					#plot 
					self.PyplotedAxesVariable.plot(
						self.PyplotedXVariable,
						self.PyplotedYVariable,
						**_KwargVariablesDict
					)
			else:

				#plot 
				self.PyplotedAxesVariable.plot(
					self.PyplotedXVariable,
					self.PyplotedYVariable,
					self.PyplotedZVariable,
					**_KwargVariablesDict
				)

			#/###############/#
			# Look for Chart setting
			#

			#Check
			if self.PyplotingChartVariable!=None:

				#debug
				'''
				self.debug(
					[
						'In this single plot'
					]
				)
				'''

				#mapArgument
				self.mapArgument(
					self.PyplotedAxesVariable,
					self.PyplotingChartVariable
				)


	def pyplotPanel(self):

		#debug
		self.debug(
			[
				"We pyplot Panel here"
			]
		)

		#/################/#
		# Build a label axes
		#

		#get
		PyplotedLabelDerivePyploter=self.getTeamer(
			'Charts'
		).getManager(
			'Label',
			0
		)

		#set the size
		PyplotedLabelDerivePyploter.PyplotingShapeVariable=[1,1]

		#get
		if self.PyplotingLabelStr=="":
			PyplotedLabelStr=Viewer.ViewAlphabetStr[self.ManagementIndexInt]
		else:
			PyplotedLabelStr=self.PyplotingLabelStr

		#Check
		if self.PyplotingTextVariable==None:

			#Check
			if self.PyplotedParentFigureDerivePyploterVariable.PyplotingTextVariable!=None:

				#list
				self.PyplotedTextIntsList=list(
					self.PyplotedParentFigureDerivePyploterVariable.PyplotingTextVariable
				)
				
			else:

				#default
				self.PyplotedTextIntsList=[-0.25,-0.2]
		else:

			#list
			self.PyplotedTextIntsList=list(self.PyplotingTextVariable)

		#set
		PyplotedLabelDerivePyploter.PyplotingChartVariable=[
			('plot',[]),
			('text',{
						'#liarg':[
							self.PyplotedTextIntsList[0],
							self.PyplotedTextIntsList[1],
							'$\mathbf{'+PyplotedLabelStr+'}$'
						],
						'#kwarg':{
							'fontsize':20,
						}
					}
			),
			('set_axis_off',"Noarg")
		]

	def pyplotAxe(self,_AxeStr):

		#debug
		'''
		self.debug(
			[
				'We pyplotAxe here',
				('self.',self,[
					'PyplotingChartVariable',
					'PyplotedChartTuplesList',
				])
			]
		)
		'''

		#set
		LowAxeStr=_AxeStr.lower()

		#get
		ViewedSkipTickBool=getattr(
				self,
				'Pyploting'+_AxeStr+'SkipTickBool'
			)

		#/###############/#
		# Look for a label
		#

		#get
		ViewingLabelStr=getattr(
			self,
			'Viewing'+_AxeStr+'LabelStr'
		)

		#init
		ViewedShiftVariablesList=[1,0]

		#Check
		if ViewingLabelStr!="":

			#Init
			ViewedLabelPlot=False

			#/################/#
			# Determine the next possible shift
 			#

			#Check
			if len(self.ParentDeriveTeamerVariable.ManagementDict)>(self.ManagementIndexInt+1):

				#get
				ViewedNextDerivePyploter=self.ParentDeriveTeamerVariable.ManagementDict.getValue(
					self.ManagementIndexInt+1
				)

				#Check
				if type(ViewedNextDerivePyploter.PyplotingShiftVariable)==list:

					#copy
					ViewedShiftVariablesList=ViewedNextDerivePyploter.PyplotingShiftVariable[:]

			#debug
			'''
			self.debug(
				[
					'We have looked to a maybe next plot to see if wee print the label on axes',
					'ViewedShiftVariablesList is '+str(ViewedShiftVariablesList)
				]
			)
			'''

			#/################/#
			# Simplify the labels to print 
			# if plots are sorted in columns or rows
			#

			#debug
			'''
			self.debug(
				[
					'Do we have to simplfy the tick print',
					'ViewedSkipTickBool is '+str(ViewedSkipTickBool)
				]
			)
			'''
			
			#Check
			if ViewedSkipTickBool:

				#Check
				if (
						_AxeStr=='X' and ViewedShiftVariablesList[0]>0
					) or (
						_AxeStr=='Y' and ViewedShiftVariablesList[1]>0
					):

					#Check
					if self.ParentDeriveTeamerVariable!=None and self.ManagementIndexInt<len(
						self.ParentDeriveTeamerVariable.ManagementDict
					)-1:

						#append
						self.PyplotedChartTuplesList.append(
							(
								'set_'+LowAxeStr+'label',{
									'#liarg':[""]
								}
							)
						)

						#set
						ViewedLabelPlot=True

			#Check
			if ViewedLabelPlot==False:

				#debug
				'''
				self.debug(
					[
						'We set axis label',
						'ViewingLabelStr is ',
						str(ViewingLabelStr)
					]
				)
				'''

				#append
				#self.PyplotedChartTuplesList.append(
				#	(
				#		'set_'+LowAxeStr+'label',ViewingLabelStr
				#	)
				#)

				#append
				self.PyplotedChartTuplesList.append(
					(
						'set_'+LowAxeStr+'label',{
								'#liarg':[ViewingLabelStr],
								'#kwarg':{
									'fontsize':20
								}
							}
					)
				)
				

		#/###############/#
		# Look for a lim
		#

		#get
		ViewedLimLiargStr=getattr(
			self,
			'Viewed'+_AxeStr+'limLiargStr'
		)

		#Check
		if ViewedLimLiargStr!="":

			#append
			self.PyplotedChartTuplesList.append(
				(
					'set_'+LowAxeStr+'lim',{
						'#liarg:#map@get':[ViewedLimLiargStr]
					}
				)
			)

		#/###############/#
		# Look for ticks
		#

		#get
		ViewedTickLiargStr=getattr(
			self,
			'Viewed'+_AxeStr+'tickLiargStr'
		)

		#Check
		if ViewedTickLiargStr!="":

			#append
			self.PyplotedChartTuplesList.append(
				(
					'set_'+LowAxeStr+'ticks',{
						'#liarg:#map@get':[ViewedTickLiargStr]
					}
				)
			)

		#/###############/#
		# Look for tick labels
		#

		#get
		ViewedTickLabelLiargStr=getattr(
			self,
			'Viewed'+_AxeStr+'tickLabelLiargStr'
		)

		#Check
		if ViewedTickLabelLiargStr!="":

			#Init
			ViewedTickLabelPlot=False

			#debug
			'''
			self.debug(
				[
					'_AxeStr is '+str(_AxeStr),
					'ViewedShiftVariablesList is '+str(ViewedShiftVariablesList),
					'ViewedSkipTickBool is '+str(ViewedSkipTickBool),
					('self.',self,[
							'ManagementIndexInt'
						]),
					'self.ManagementIndexInt<len(self.ParentDeriveTeamerVariable.ManagementDict)-1 is ',
					str(self.ManagementIndexInt<len(self.ParentDeriveTeamerVariable.ManagementDict)-1)
				]
			)
			'''

			#Check
			if ViewedShiftVariablesList!=None:

				#/################/#
				# Simplify the ticklabels to print 
				# if plots are sorted in columns or rows
				#

				#Check
				if ViewedSkipTickBool:

					#Check
					if (
							_AxeStr=='X' and ViewedShiftVariablesList[0]>0
						) or (
							_AxeStr=='Y' and ViewedShiftVariablesList[1]>0
						):

						#Check
						if self.ManagementIndexInt<len(
							self.ParentDeriveTeamerVariable.ManagementDict
						)-1:

							#debug
							'''
							self.debug(
								[
									'We remove the tick labels'
								]
							)
							'''

							#append
							self.PyplotedChartTuplesList.append(
								(
									'set_'+LowAxeStr+'ticklabels',{
										'#liarg':[[]]
									}
								)
							)

							#set
							ViewedTickLabelPlot=True

			#Check
			if ViewedTickLabelPlot==False:

				#append
				self.PyplotedChartTuplesList.append(
					(
						'set_'+LowAxeStr+'ticklabels',{
							'#liarg:#map@get':[ViewedTickLabelLiargStr],
							'#kwarg':{
								'fontsize':15
							}
						}
					)
				)

	def pyplotChart(self):

		#/#################/#
		# Check
		#

		#debug
		'''
		self.debug(
			[
				'We pyplot Chart here',
				('self.',self,[
					'PyplotingChartVariable'
				])
			]
		)
		'''
		
		#Check
		if self.PyplotingChartVariable!=None:

			#Check
			if self.PyplotedChartTuplesList==None:
				self.PyplotedChartTuplesList=[]

			#copy
			self.PyplotedChartTuplesList+=copy.copy(
				self.PyplotingChartVariable.items()
				if hasattr(self.PyplotingChartVariable,'items')
				else self.PyplotingChartVariable
			)

		#/#################/#
		# Look for view argument
		#

		#debug
		'''
		self.debug(
			[
				'First look for view arguments'
			]
		)
		'''
		
		#map
		map(
			lambda __AxeStr:
			self.pyplotAxe(__AxeStr),
			['X','Y']
		)

		#debug
		'''
		self.debug(
			[
				'Ok we have maybe setted the PyplotedChartTuplesList',
				('self.',self,[
						'PyplotedChartTuplesList',
						'ManagementIndexInt'
					])
			]
		)
		'''

		#/#################/#
		# Determine the previous Chart
		#

		#Check
		if self.ManagementIndexInt>0:

			#debug
			'''
			self.debug(
					[
						'We get the previous axes in the same panel
					]
				)
			'''

			#get
			self.PyplotedPreviousChartDerivePyploterVariable=self.ParentDeriveTeamerVariable.ManagementDict.getValue(
				self.ManagementIndexInt-1
			)

		elif self.PyplotedParentPanelDerivePyploterVariable.ManagementIndexInt>0:

			#debug
			'''
			self.debug(
				[
					'We get the last axes in the previous panel'
					'self.PyplotedParentPanelDerivePyploterVariable.ManagementIndexInt is ',
					str(self.PyplotedParentPanelDerivePyploterVariable.ManagementIndexInt),
					'self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable.ManagementDict.keys() is',
					str(self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable.ManagementDict.keys())
				]
			)
			'''

			#get
			self.PyplotedPreviousChartDerivePyploterVariable=self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable.ManagementDict.getValue(
				self.PyplotedParentPanelDerivePyploterVariable.ManagementIndexInt-1
			).TeamDict[
				'Charts'
			].ManagementDict.getValue(
				-1
			)

			#debug
			'''
			self.debug(
				[
					#'PyplotedPreviousChartDerivePyploterVariable is ',
					#SYS._str(PyplotedPreviousChartDerivePyploterVariable),
					'PyplotedPreviousChartDerivePyploterVariable.ParentTagStr is ',
					SYS._str(PyplotedPreviousChartDerivePyploterVariable.ParentTagStr),
					'self.PyplotedParentPanelDerivePyploterVariable.PyplotedCursorIntsList is ',
					str(self.PyplotedParentPanelDerivePyploterVariable.PyplotedCursorIntsList)
				]
			)
			'''

		else:

			#set
			self.PyplotedPreviousChartDerivePyploterVariable=None


		#debug
		'''
		self.debug(
			[
				'PyplotedPreviousChartDerivePyploterVariable is ',
				SYS._str(PyplotedPreviousChartDerivePyploterVariable)
			]
		)
		'''

		#/#################/#
		# Shift while in the grid to find a good place
		#

		#debug
		'''
		self.debug(
			[
				'We are going to shift',
				('self.',self,[
						'ManagementIndexInt'
					])
			]
		)
		'''

		#set
		self.setAnchor()

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'PyplotingShiftVariable',
						'PyplotedShiftVariablesList',
						'PyplotedAnchorIntsList',
				])
			]
		)
		'''

		#/#################/#
		# list maybe direct things
		#

		#debug
		'''
		self.debug(
			[
				'We determine the shape',
				('self.',self,[
						'PyplotingShapeVariable'
					])
			]
		)
		'''

		#Check
		if type(self.PyplotingShapeVariable)==list:

			#copy
			self.PyplotedShapeIntsList=self.PyplotingShapeVariable[:]

		else:

			#/################/#
			# Case of a command shape for all the charts 
			#

			#Check
			if type(self.PyplotedParentPanelDerivePyploterVariable.PyplotingShapeVariable)==list:

				#debug
				'''
				self.debug(
					[
						'Shape is determined from the parent panel'
					]
				)
				'''

				#copy
				self.PyplotedShapeIntsList=self.PyplotedParentPanelDerivePyploterVariable.PyplotingShapeVariable[:]

			#/################/#
			# Case of one panel
			#

			#Check
			elif self.PyplotedParentPanelDerivePyploterVariable==self.PyplotedParentFigureDerivePyploterVariable:

				#debug
				'''
				self.debug(
					[
						'This is just one panel case',
						'self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable is',
						str(self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable),
						('self.',self,[
								'PyplotedShiftVariablesList'
							])
					]
				)
				'''

				#Check
				if self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable==None:
					self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable=(22,20)

				#init
				self.PyplotedShapeIntsList=list(
						self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable
					)

				#/################/#
				# Look for the next panel to see if shift has to be
				# down or right

				PyplotedChartsDerivePyploter=self.PyplotedParentFigureDerivePyploterVariable.TeamDict[
							'Charts'
						]

				#Check
				if len(
						PyplotedChartsDerivePyploter.ManagementDict
					)>1:

					#debug
					'''
					self.debug(
						[
							'PyplotedChartsDerivePyploter.ManagementDict.keys() is ',
							str(PyplotedChartsDerivePyploter.ManagementDict.keys())
						]
					)
					'''

					#get
					PyplotedNextChartDerivePyloter=PyplotedChartsDerivePyploter.ManagementDict.getValue(
						1
					)

					#Check
					if PyplotedNextChartDerivePyloter.PyplotingShiftVariable!=None:

						#copy
						PyplotedShiftVariablesList=PyplotedNextChartDerivePyloter.PyplotingShiftVariable[:]
					else:

						#default
						PyplotedShiftVariablesList=[1,0]

				else:

					#set
					PyplotedShiftVariablesList=[1,0]

				#/################/#
				# Then divide the shape 
				# given the number of charts

				#Check
				if PyplotedShiftVariablesList[0]>0:

					#divide
					self.PyplotedShapeIntsList[0] /= len(
						self.PyplotedParentFigureDerivePyploterVariable.TeamDict[
							'Charts'
						].ManagementDict
					)
					self.PyplotedShapeIntsList[1] -= 2
					
				else:

					#divide
					self.PyplotedShapeIntsList[1] /= len(
							self.PyplotedParentFigureDerivePyploterVariable.TeamDict[
								'Charts'
							].ManagementDict
						)

			else:

				#init
				self.PyplotedShapeIntsList=[5,5]

		#debug
		'''
		self.debug(
			[
				'In the end',
				('self.',self,[
						'PyplotedShapeIntsList'
					])
			]
		)
		'''

		#/#################/#
		# Do the check for the anchor and the size 
		# of the Chart

		#init
		PyplotedResetBoolsList=[False,False]

		#debug
		'''
		self.debug(
			[
				'We begin to find the good shift'
			]
		)
		'''

		#init
		PyplotedCountInt=0

		#while
		while PyplotedResetBoolsList!=[True,True] and PyplotedCountInt<2:

			#/#################/#
			# Check if the anchor is good
			#

			#debug
			'''
			self.debug(
				[
					'Now we check if the anchor is still inside the figure',
					('self.',self,[
							'PyplotingShiftVariable',
							'PyplotingShapeVariable'
						]),
					'PyplotedCountInt is '+str(PyplotedCountInt)
				]
			)
			'''

			#shift and check
			for __AxeInt in [0,1]:
			
				#debug
				'''
				self.debug(
					[	
						'__AxeInt is '+str(__AxeInt),
						('self.',self,[
								'PyplotedAnchorIntsList',
							]),
						'self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable is ',
						str(self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable)
					]
				)
				'''

				#Check
				if self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable==None:
					self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable=(22,20)

				#Check
				if self.PyplotedAnchorIntsList[
						__AxeInt
					] < self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable[
						__AxeInt
					]:

					#/#################/#
					# Now check if the shape is good
					#

					#set
					PyplotedMaxAnchorInt=self.PyplotedAnchorIntsList[
							__AxeInt
						]+self.PyplotedShapeIntsList[
							__AxeInt
						]

					#debug
					'''
					self.debug(
						[
							'Ok the anchor for this axe is good',
							'but now check if the total chart can be included',
							'PyplotedMaxAnchorInt is ',
							str(PyplotedMaxAnchorInt)
						]
					)
					'''

					#Check
					if PyplotedMaxAnchorInt > self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable[
							__AxeInt
						]:

						#debug
						'''
						self.debug(
							[
								'It doesn t fit',
								('self.',self,[
										'PyplotedAnchorIntsList'
									])
							]
						)
						'''

						#set
						self.PyplotedShapeIntsList[
							__AxeInt
						]=self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable[
							__AxeInt
						]-self.PyplotedAnchorIntsList[
							__AxeInt
						]

						#debug
						'''
						self.debug(
							[
								'Nope we have reduced the size of the Chart',
								('self.',self,[
										'PyplotedShapeIntsList'
									]
								)
							]
						)
						'''

					#set
					PyplotedResetBoolsList[
						__AxeInt
					]=True

				#/#################/#
				# Check if the shift was good
				#

				#Check
				if PyplotedResetBoolsList[
						__AxeInt
					]==False:

					#Check
					if __AxeInt==0:

						#debug
						'''
						self.debug(
							[
								'We can maybe shift on the right'
							]
						)
						'''

						#reset
						self.PyplotingShiftVariable=[0,1]
						PyplotedResetBoolsList=[False,False]

						#set again
						self.setAnchor()

						#break
						break

					elif __AxeInt==1:

						#debug
						'''
						self.debug(
							[
								'We can maybe shift below'
							]
						)
						'''

						#reset
						self.PyplotingShiftVariable=[1,0]
						PyplotedResetBoolsList=[False,False]

						#set again
						self.setAnchor()

						#break
						break

			#debug
			'''
			self.debug(
				[
					'In the end of a trial',
					'PyplotedResetBoolsList is ',
					str(PyplotedResetBoolsList),
					('self.',self,[
							'PyplotedAnchorIntsList'
						])
				]
			)
			'''

			#increment
			PyplotedCountInt+=1

		#/#################/#
		# Compute the hit
		#

		#debug
		'''
		self.debug(
			[
				'We build the PyplotedHitIntsList',
				('self.',self,[
						'PyplotedAnchorIntsList',
						'PyplotedShapeIntsList'
					])
			]
		)
		'''
		
		#map
		self.PyplotedHitIntsList=map(
			lambda __PyplotedAnchorInt,__PyplotedShapeInt:
			 __PyplotedAnchorInt+__PyplotedShapeInt,
			self.PyplotedAnchorIntsList,
			self.PyplotedShapeIntsList
		)

		#debug
		'''
		self.debug(
			[
				'In the end',
				('self.',self,[
						'PyplotedHitIntsList'
					])
			]
		)
		'''
		
		#/#################/#
		# init
		#

		#debug
		'''
		self.debug(
			[
				'We init the axes',
				('self.',self,[
					'PyplotedAnchorIntsList',
					'PyplotedShapeIntsList'
				])
			]
		)
		'''

		#import
		from matplotlib import pyplot

		#subplot2grid
		self.PyplotedAxesVariable=pyplot.subplot2grid(
				self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridVariable, 
				self.PyplotedAnchorIntsList, 
				rowspan=self.PyplotedShapeIntsList[0],
				colspan=self.PyplotedShapeIntsList[1]
			)

		#give a pointer back
		self.PyplotedAxesVariable.ParentPyploter=self

		#debug
		'''
		self.debug(
				[
					'Ok we have initiated the axes',
					('self.',self,['PyplotedAxesVariable'])
				]
			)
		'''

		#/#################/#
		# link to the fig
		#

		#link
		self.PyplotedAxesVariable._figure=self.PyplotedParentFigureDerivePyploterVariable.PyplotedFigureVariable
		
		#debug
		'''
		self.debug(
				[
					'Ok we have setted the axe'
				]
			)
		'''

		#/#################/#
		# Direct set if there are no draws
		#

		#Check
		if 'Draws' not in self.TeamDict or len(self.TeamDict['Draws'])==0:

			#debug
			'''
			self.debug(
				[
					'We mapArgument here',
					('self.',self,[
							'PyplotedChartTuplesList'
						])
				]
			)	
			'''

			#map argument
			self.mapArgument(
				self.PyplotedAxesVariable,
				self.PyplotedChartTuplesList
			)

	def pyplotDraw(self):

		#/#################/#
		# Check
		#

		#Check
		if self.PyplotingDrawVariable!=None:

			#copy
			self.PyplotedDrawTuplesList+=copy.copy(
				self.PyplotingDrawVariable.items()
				if hasattr(self.PyplotingDrawVariable,'items')
				else self.PyplotingDrawVariable
			)

		#/#################/#
		# We mapArgument draw in the parent axes
		#

		#debug
		'''
		self.debug(
			[
				'We map argument draw in the parent axe',
				('self.',self,[
					'PyplotingDrawVariable',
					#'PyplotedParentFigureDerivePyploterVariable'
				]),
				'self.PyplotedParentChartDerivePyploterVariable.PyplotedAxesVariable is ',
				str(self.PyplotedParentChartDerivePyploterVariable.PyplotedAxesVariable)
			]
		)
		'''
		
		#map argument
		self.PyplotedLinesList.extend(
			self.PyplotedParentFigureDerivePyploterVariable.mapArgument(
				self.PyplotedParentChartDerivePyploterVariable.PyplotedAxesVariable,
				self.PyplotedDrawTuplesList
			)
		)

		#debug
		'''
		self.debug(
			[
				'Ok now look if we have to set the axes',
				'self.ManagementIndexInt==(len(self.ParentDeriveTeamerVariable.ManagementDict)-1) is ',
				str(self.ManagementIndexInt==(len(self.ParentDeriveTeamerVariable.ManagementDict)-1))
			]
		)
		'''
		
		#/###################/#
		# If it is the last then trigger the axes to set also
		#

		#debug
		'''
		self.debug(
			[
				'Check if we have to make trigger the parent Chart',
				'self.ParentDeriveTeamerVariable!=None is ',
				str(self.ParentDeriveTeamerVariable!=None)
			]
		)
		'''

		#Check
		if self.ParentDeriveTeamerVariable!=None:

			#Check
			if self.ManagementIndexInt==(
				len(self.ParentDeriveTeamerVariable.ManagementDict)-1
			):

				#debug
				'''
				self.debug(
					[
						'I am the last draw of this axes !',
						'Lets the axes setting itself now',
						('self.PyplotedParentChartDerivePyploterVariable.',
							self.PyplotedParentChartDerivePyploterVariable,
							[
								'PyplotingDrawVariable',
								'PyplotedChartTuplesList'
							])
					]
				)	
				'''
				
				#call
				self.PyplotedParentChartDerivePyploterVariable.setEndAxes()
					
	def mimic_set(self):

		#Check
		if self.SettingKeyVariable in [
					PyplotPlotKeyStr,
					PyplotScatterKeyStr,
					PyplotBarKeyStr
				]:

			#/####################/#
			# first maybe pyplot if it was not already
			# 

			#debug
			'''
			self.debug(
					[
						'we maybe pyplot first',
					]
				)
			'''

			#pyplot
			self.pyplot()

			#/####################/#
			# Then add in the plot
			# 

			#debug
			'''
			self.debug(
					[
						'before plot',
						('self.',self,[
							#'PyplotedParentFigureDerivePyploterVariable',
							'SettingValueVariable'
						])
					]
				)
			'''

			#init
			PyplotPlotArgumentDict=Setter.ArgumentDict(
					self.SettingValueVariable,
					self.PyplotedParentFigureDerivePyploterVariable
				)

			#debug
			'''
			self.debug(
					[
						'We plot here',
						'PyplotPlotArgumentDict is',
						SYS._str(PyplotPlotArgumentDict)
					]
				)
			'''

			#plot
			self.PyplotedLinesList.append(
				self.PyplotedAxesVariable.plot(
					*PyplotPlotArgumentDict['LiargVariablesList'],
					**PyplotPlotArgumentDict['KwargVariablesDict']
				)[0]
			)

			#debug
			'''
			self.debug(
				[
					('self.',self,['PyplotedLinesList']),
					#str(self.PyplotedLinesList[0][0]),
				]
			)
			'''

			#return 
			return {'HookingIsBool':False}

		elif self.SettingKeyVariable==PyplotAxesKeyStr:

			#debug
			'''
			self.debug(
					[
						'before axes',
						('self.',self,[
							#'PyplotedParentFigureDerivePyploterVariable',
							'PyplotedAxesVariable'
						])
					]
				)
			'''

			#map
			ArgumentTuplesList=map(
					lambda __ItemTuple:
					(
						__ItemTuple[0],
						Setter.ArgumentDict(
								__ItemTuple[1],
								self.PyplotedParentFigureDerivePyploterVariable
							)
					),
					SYS.SetList(
						self.SettingValueVariable
					)
				)

			#debug
			'''
			self.debug(
					[
						'We axe here',
						'ArgumentTuplesList is ',
						SYS._str(ArgumentTuplesList),
					]
				)
			'''

			#map
			map(
					lambda __ArgumentTuple:
					SYS.get(
						self.PyplotedAxesVariable,
						__ArgumentTuple[0]
					)()
					if len(__ArgumentTuple[1]['LiargVariablesList']
						)==0 and __ArgumentTuple[1]['KwargVariablesDict']==None
					else(
						SYS.get(
							self.PyplotedAxesVariable,
							__ArgumentTuple[0]
						)(**__ArgumentTuple[1]['KwargVariablesDict'])
						if len(__ArgumentTuple[1]['LiargVariablesList']
						)==0
						else(
							SYS.get(
								self.PyplotedAxesVariable,
								__ArgumentTuple[0]
							)(
								*__ArgumentTuple[1]['LiargVariablesList'],
								**__ArgumentTuple[1]['KwargVariablesDict']
							) 
							if __ArgumentTuple[1]['KwargVariablesDict']!=None
							else
							SYS.get(
								self.PyplotedAxesVariable,
								__ArgumentTuple[0]
							)(
								*__ArgumentTuple[1]['LiargVariablesList']
							)
						)
					),
					ArgumentTuplesList
				)

			#return 
			return {'HookingIsBool':False}

		elif type(self.SettingKeyVariable)==str and self.SettingKeyVariable.startswith(
			PyplotMpld3KeyStr):

			#deprefix
			ToolTipKeyStr=SYS.deprefix(
					self.SettingKeyVariable,
					PyplotMpld3KeyStr
				)

			#debug
			'''
			self.debug(
					[
						'before plugins',
						('self.',self,['PyplotedParentFigureDerivePyploterVariable'])
					]
				)
			'''

			#init
			PyplotPluginArgumentDict=Setter.ArgumentDict(
					self.SettingValueVariable,
					self.PyplotedParentFigureDerivePyploterVariable
				)

			#debug
			'''
			self.debug(
					[
						'We plugin here',
						'PyplotPluginArgumentDict is ',
						SYS._str(PyplotPluginArgumentDict)
					]
				)
			'''

			#plugin
			from mpld3 import plugins
			self.PyplotTooltipVariablesList=map(
				lambda __PyplotCartoonVariable:
				getattr(
					plugins,
					ToolTipKeyStr
				)(
					*[
						__PyplotCartoonVariable
					]+PyplotPluginArgumentDict['LiargVariablesList'],
					**PyplotPluginArgumentDict['KwargVariablesDict']
				),
				self.PyplotedLinesList
			)

			#debug
			'''
			self.debug(
					[
						('self.',self,['PyplotTooltipVariablesList'])
					]
				)
			'''
			
			#connect
			map(
				lambda __PyplotTooltipVariable:
				plugins.connect(
					self.PyplotedFigureVariable,
					__PyplotTooltipVariable
				),
				self.PyplotTooltipVariablesList
			)

			#return 
			return {'HookingIsBool':False}
				#we set a Chart

		#call the base method
		BaseClass.set(self)

	def show(self):

		#import
		from matplotlib import pyplot

		#show
		pyplot.show()

		#return
		return self

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Remove the brian objects that are non setted
			#

			#map
			map(
					lambda __KeyStr:
					self.forcePrint(
						[__KeyStr],
						'PyploterClass'
					)
					if getattr(self.PrintingCopyVariable,__KeyStr)!=None
					else None,
					[
						'PyplotedFigureVariable',
						'PyplotedAxesVariable'
					]
				)


			#Debug
			'''
			print('self.__class__ is ')
			print(self.__class__)
			print('self.PyplotingPrintBool')
			print(self.__class__.PyplotingPrintBool)
			print('self.__class__.PyplotingPrintBool')
			print(self.__class__.PyplotingPrintBool)
			print('')
			'''

			#/##################/#
			# Maybe just give a pointer repr of the children
			# pyplot objects

			#Check
			if self.__class__.PyplotingPrintBool==False or self.PyplotingPrintBool==False:

				#Debug
				'''
				print('We remove the pyplot teams')
				print('self.TeamDict.keys() is ')
				print(self.TeamDict.keys())
				print('self.PrintingCopyVariable.TeamDict.keys() is ')
				print(self.PrintingCopyVariable.TeamDict.keys())
				print('')
				'''

				#map
				map(
					lambda __TeamStr:
					self.PrintingCopyVariable.TeamDict.__setitem__(
						__TeamStr,
						Printer.getPointerStr(
							self.TeamDict[
								__TeamStr
							]
						)
					) if __TeamStr in self.TeamDict
					else None,
					['Draws','Charts','Panels']
				)

				#Debug
				'''
				print('We remove the pyplot teams')
				print('self.TeamDict.keys() is ')
				print(self.TeamDict.keys())
				print('')
				'''

		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

	def setEndAxes(self):

		#add
		self.PyplotedChartTuplesList+=[
				(
					'tick_params',{
						'#kwarg':{
							'length':10,
							'width':5,
							'which':'major'
						}
					}
				),
				(
					'tick_params',{
						'#kwarg':{
							'length':5,
							'width':2,
							'which':'minor'
						}
					}
				),
				('xaxis.set_ticks_position',
					{
						'#liarg':['bottom']
					}
				),
				('yaxis.set_ticks_position',
					{
						'#liarg':['left']
					}
				)
		]

		#debug
		'''
		self.debug(
			[
				'Are we going to add a legend',
				('self.',self,[
					'PyplotingLegendDict'
				])
			]
		)
		'''

		#Check
		if self.PyplotingLegendDict!=None and len(self.PyplotingLegendDict)>0:

			#debug
			'''
			self.debug(
				[
					'We complete the legend',
					('self.',self,[
							'PyplotingLegendDict'
						])
				]
			)
			'''

			#complete
			SYS.complete(
				self.PyplotingLegendDict,
				{
					'fontsize':self.PyplotedParentFigureDerivePyploterVariable.PyplotingFontVariable 
					if self.PyplotedParentFigureDerivePyploterVariable.PyplotingFontVariable!=None else 15,
					'shadow':True,
					'fancybox':True,
					'loc':2,
					'bbox_to_anchor':(1.,1.)
				}
			)

			#debug
			'''
			self.debug(
				[
					'We add a legend',
					('self.',self,[
							'PyplotingLegendDict'
						])
				]
			)
			'''
			
			#add
			self.PyplotedChartTuplesList+=[
				('legend',{
					'#liarg':[],
					'#kwarg':self.PyplotingLegendDict
				})
			]

		#/#################/#
		# We map argument in the axes
		#

		#debug
		'''
		self.debug(
			[
				'We chart in the parent axe',
				('self.',self,[
					'PyplotedChartTuplesList'
				])
			]
		)
		'''

		#map argument
		self.mapArgument(
			self.PyplotedAxesVariable,
			self.PyplotedChartTuplesList
		)


	def setAnchor(self):

		#debug
		'''
		self.debug(
			[
				'We setAnchor here',
				('self.',self,[
						'ManagementIndexInt'
					])
			]
		)
		'''

		#init
		if self.ManagementIndexInt==0:

			#debug
			'''
			self.debug(
				[
					'This is the case where this is a first axes of a new panel'
				]
			)
			'''

			#Check
			if self.PyplotedParentPanelDerivePyploterVariable!=None and self.PyplotedParentPanelDerivePyploterVariable.ManagementIndexInt>0:

				#debug
				'''
				self.debug(
					[
						'And we want to shift compare to the previous panel'
					]
				)
				'''

				#get
				self.PyplotedPreviousPanelDerivePyploterVariable=self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable.ManagementDict.getValue(
						self.PyplotedParentPanelDerivePyploterVariable.ManagementIndexInt-1
					)

				#get
				PyplotedHitIntsListsList=map(
					lambda __DerivePyploter:
					__DerivePyploter.PyplotedHitIntsList,
					self.PyplotedPreviousPanelDerivePyploterVariable.TeamDict[
						'Charts'
					].ManagementDict.values()
				)

				#map

				#map
				self.PyplotedPreviousPanelDerivePyploterVariable.PyplotedHitIntsList=map(
					lambda __ZipList:
					max(__ZipList),
					SYS.unzip(PyplotedHitIntsListsList,[0,1])
				)

				#/###################/#
				# Determine the previous 
				# 

				#copy
				self.PyplotedPreviousAnchorIntsList=self.PyplotedPreviousPanelDerivePyploterVariable.PyplotedAnchorIntsList
				self.PyplotedPreviousShapeIntsList=self.PyplotedPreviousPanelDerivePyploterVariable.PyplotedHitIntsList

				#/###################/#
				# Determine the shift 
				# 

				#debug
				'''
				self.debug(
					[
						'We determine the shift',
						('self.',self,[
								'PyplotingShiftVariable',
							]),
						'self.PyplotedParentPanelDerivePyploterVariable.PyplotingShiftVariable is ',
						str(self.PyplotedParentPanelDerivePyploterVariable.PyplotingShiftVariable)
					]
				)
				'''

				#Check
				if self.PyplotingShiftVariable!=None:

					#list
					self.PyplotedShiftVariablesList=list(
						self.PyplotingShiftVariable
					)

				elif self.PyplotedParentPanelDerivePyploterVariable.PyplotingShiftVariable!=None:

					#copy
					self.PyplotedShiftVariablesList=self.PyplotedParentPanelDerivePyploterVariable.PyplotingShiftVariable[:]
				else:

					#default
					self.PyplotedShiftVariablesList=[1,0]

			else:

				#debug
				'''
				self.debug(
					[
						'And this is the first panel'
					]
				)
				'''

				#/###################/#
				# Determine the shift 
				#

				#Check
				if self.PyplotingShiftVariable!=None:

					#list
					self.PyplotedShiftVariablesList=list(self.PyplotingShiftVariable)
				else:

					#default
					self.PyplotedShiftVariablesList=[0,0]		
		else:

			#debug
			'''
			self.debug(
				[
					'This is the case where this is an axes in the panel',
					'and we want to shift compare to the previous axes'
				]
			)
			'''

			#/###################/#
			# Look for the previous Chart in the same panel
			#

			#get
			self.PyplotedPreviousChartDerivePyploterVariable=self.ParentDeriveTeamerVariable.ManagementDict.getValue(
				self.ManagementIndexInt-1
			)

			#/###################/#
			# Determine the previous 
			# 

			#copy
			self.PyplotedPreviousAnchorIntsList=self.PyplotedPreviousChartDerivePyploterVariable.PyplotedAnchorIntsList
			self.PyplotedPreviousShapeIntsList=self.PyplotedPreviousChartDerivePyploterVariable.PyplotedShapeIntsList

			#/###################/#
			# Determine the shift 
			# 

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'PyplotingShiftVariable'
						])
				]
			)
			'''

			#Check
			if self.PyplotingShiftVariable!=None:

				#list
				self.PyplotedShiftVariablesList=list(self.PyplotingShiftVariable)
			else:

				#init
				self.PyplotedShiftVariablesList=[1,0]

		#/###################/#
		# Compute the anchor
		#	

		#map
		PyplotedTrueShiftIntsList=map(
			lambda __PyplotedShiftVariable:
			__PyplotedShiftVariable 
			if type(__PyplotedShiftVariable)==list
			else
			(
				__PyplotedShiftVariable-1 
				if __PyplotedShiftVariable>0
				else 0
			),
			self.PyplotedShiftVariablesList
		)

		#debug
		'''
		self.debug(
			[
				'We compute the anchor compared to the previous',
				('self.',self,[
						'PyplotedPreviousAnchorIntsList',
						'PyplotedShiftVariablesList',
						'PyplotedPreviousShapeIntsList',
					]),
				'PyplotedTrueShiftIntsList is '+str(PyplotedTrueShiftIntsList)
			]
		)
		'''
		
		#set
		self.PyplotedAnchorIntsList=map(
			lambda __PyplotedPreviousAnchorInt,__PyplotedShiftVariable,__PyplotedTrueShiftInt,__PyplotedPreviousShapeInt:
			__PyplotedPreviousAnchorInt+__PyplotedTrueShiftInt+int(
				__PyplotedShiftVariable>0
			)*__PyplotedPreviousShapeInt
			if type(__PyplotedShiftVariable)==int else (
				__PyplotedShiftVariable[1]
				if __PyplotedShiftVariable[0]=='top'
				else 0
			),
			self.PyplotedPreviousAnchorIntsList,
			self.PyplotedShiftVariablesList,
			PyplotedTrueShiftIntsList,
			self.PyplotedPreviousShapeIntsList
		)

		#debug
		'''
		self.debug(
			[
				'In the end',
				('self.',self,[
						'PyplotedAnchorIntsList'
					])
			]
		)
		'''

		#/###################/#
		# give to the panel
		#

		#Check
		if self.ManagementIndexInt==0:

			#alias
			self.PyplotedParentPanelDerivePyploterVariable.PyplotedAnchorIntsList=self.PyplotedAnchorIntsList

#</DefineClass>

#</DefinePrint>
PyploterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PyplotTooltipVariablesList',
		'PyplotingXVariable',
		'PyplotingYVariable',
		'PyplotingZVariable',
		'PyplotingGridVariable',
		'PyplotingSubplotInt',
		'PyplotingShapeVariable',
		'PyplotingFigureVariable',
		'PyplotingDrawVariable',
		'PyplotingChartVariable',
		'PyplotingShiftVariable',
		'PyplotingPrintBool',
		'PyplotingLabelStr',
		'PyplotingLegendDict',
		'PyplotingTextVariable',
		'PyplotingXSkipTickBool',
		'PyplotingYSkipTickBool',
		'PyplotingMarkerVariable',
		'PyplotingColorVariable',
		'PyplotingFontVariable',
		'PyplotingSubplotInt',
		'PyplotingCloseBool',
		'PyplotedSingleBool',
		'PyplotedTeamTagStr',
		'PyplotedParentFigureDerivePyploterVariable',
		'PyplotedParentPanelDerivePyploterVariable',
		'PyplotedParentChartDerivePyploterVariable',
		'PyplotedFigureVariable',
		'PyplotedAxesVariable',
		'PyplotedAxesList',
		'PyplotedLinesList',
		'PyplotedPreviousAnchorIntsList',
		'PyplotedPreviousShapeIntsList',
		'PyplotedAnchorIntsList',
		'PyplotedShiftVariablesList',
		'PyplotedHitIntsList',
		'PyplotedPanelShapeIntsList',
		'PyplotedShapeIntsList',
		'PyplotedChartTuplesList',
		'PyplotedDrawTuplesList',
		'PyplotedParentSingularStr',
		'PyplotedPreviousChartDerivePyploterVariable',
		'PyplotedPreviousPanelDerivePyploterVariable',
		'PyplotedTextIntsList',
		'PyplotedXVariable',
		'PyplotedYVariable',
		'PyplotedZVariable'
	]
)
#<DefinePrint>

