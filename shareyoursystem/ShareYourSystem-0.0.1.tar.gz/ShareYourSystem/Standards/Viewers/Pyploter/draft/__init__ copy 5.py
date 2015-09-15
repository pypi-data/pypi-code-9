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
						_PyplotingGridIntsTuple=(20,20),
						_PyplotingShapeIntsTuple=(5,5),
						_PyplotingDrawVariable=None,
						_PyplotingChartVariable=None,
						_PyplotingShiftIntsTuple=(1,0),
						_PyplotedTeamTagStr="",
						_PyplotedParentFigureDerivePyploterVariable=None,
						_PyplotedParentPanelDerivePyploterVariable=None,
						_PyplotedParentChartDerivePyploterVariable=None,						
						_PyplotedFigureVariable=None,
						_PyplotedAxesVariable=None,
						_PyplotedLinesList=None,
						_PyplotedAnchorIntsList=[0,0],
						_PyplotedShiftTuplesList={
							'DefaultValueType':property,
							'PropertyInitVariable':None,
							'PropertyDocStr':'I am reactive when I am a Panel and want to know the space I take !'
						},
						_PyplotedPanelShapeIntsList=None,
						_PyplotedCursorIntsList=[0,0],
						_PyplotedParentSingularStr="",
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_pyplot(self):	
		
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
		if self.ParentedTotalSingularListDict!=None and len(self.ParentedTotalSingularListDict)>0:

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
		self.debug(
			[
				'Ok',
				('self.',self,['PyplotedParentSingularStr'])
			]
		)
		
		#/###############/#
		# Cases depending on the level
		#

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Panels' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Panels',
			'Charts',
			'Draws'
		]):


			#/###############/#
			# If it is the top then init the pyplot
			#

			#debug
			self.debug(
					[
						'Figure Level',
					]
				)

			#import pyplot
			from matplotlib import pyplot

			#init
			self.PyplotedFigureVariable = pyplot.subplot()

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
				# Set Chart 
				#

				#debug
				'''
				self.debug(
					[
						'We are in the case of a Figure Panel Axes draw'
					]
				)
				'''

				#init
				self.PyplotedAxesVariable = pyplot.axes()

				#link
				self.PyplotedAxesVariable._figure = self.PyplotedFigureVariable	

				#/###############/#
				# draw 
				#

				#pyplotDraw
				self.pyplotDraw()
				
			#/###############/#
			# structure
			#

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

		

		#/###################/#
		# Wrap case
		#

		elif self.ParentDeriveTeamerVariable!=None:

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

			elif self.ParentDeriveTeamerVariable.TeamTagStr=='Charts':

				#debug
				'''
				self.debug(
						[
							'Chart level.'
						]
					)
				'''

				#/#################/#
				# Determine the parent
				#

				#set
				self.PyplotedParentPanelDerivePyploterVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

				#debug
				'''
				self.debug(
						[
							'self.PyplotedParentPanelDerivePyploterVariable.PyplotedParentSingularStr is ',
							self.PyplotedParentPanelDerivePyploterVariable.PyplotedParentSingularStr,
							'Check now who are the parents'
						]
					)
				'''

				#Check
				if self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable!=None:
						
					#debug
					self.debug(
						[
							'Ok there is a parent parent for this Chart'
						]
					)

					#alias
					PyplotedParentFigureDerivePyploterVariable=self.PyplotedParentPanelDerivePyploterVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
						
					if PyplotedParentFigureDerivePyploterVariable!=None:

						#set
						self.PyplotedParentFigureDerivePyploterVariable=PyplotedParentFigureDerivePyploterVariable

						#debug
						self.debug(
							[
								'Yes the panel parent parent exists'
							]
						)

					else:

						#debug
						self.debug(
							[
								'Nope the parent parent not exist so direct set figure with panel parent'
							]
						)

						#set
						self.PyplotedParentFigureDerivePyploterVariable=self.PyplotedParentPanelDerivePyploterVariable

				else:

					#set
					self.PyplotedParentFigureDerivePyploterVariable=self

				#debug
				self.debug(
					[
						'Ok for this Chart, we have determined the panel and figure parent',
						#('self.',self,[
						#	'PyplotedParentFigureDerivePyploterVariable'
						#])
					]
				)

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
						self.PyplotingDrawVariable
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

				#Check
				if self.ManagementIndexInt==(len(self.ParentDeriveTeamerVariable.ManagementDict)-1):

					#debug
					'''
					self.debug(
						[
							'I am the last draw of this axes !',
							'Lets the axes setting itself now',
							('self.PyplotedParentChartDerivePyploterVariable.',
								self.PyplotedParentChartDerivePyploterVariable,
								['PyplotingDrawVariable'])
						]
					)	
					'''

					#Check
					if self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable!=None:
	
						#/#################/#
						# We map argument in the axes
						#

						#debug
						'''
						self.debug(
							[
								'We chart in the parent axe',
								('self.',self,[
									'PyplotedParentChartDerivePyploterVariable'
								]),
								'self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable is ',
								SYS._str(self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable)
							]
						)
						'''

						#map argument
						self.PyplotedParentFigureDerivePyploterVariable.mapArgument(
							self.PyplotedParentChartDerivePyploterVariable.PyplotedAxesVariable,
							self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable
						)

	"""
	def mimic_view(self):

		#import mpld3
		import mpld3

		#fig to html
		self.ViewedHtmlStr=mpld3.fig_to_html(
			self.PyplotedFigureVariable,
			template_type="simple"
		)

		#call the base method
		BaseClass.view(self)
	"""
	
	"""
	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#/##################/#
		# Maybe pyplot
		#

		#debug
		'''
		self.debug(
			[
				'We are going to parent but before',
				('self.',self,['StructuringDoStr']),
				'self.StructuringTopDeriveStructurerVariable!=self is ',
				str(self.StructuringTopDeriveStructurerVariable!=self),
				'self.ParentedTotalListDict.keys() is ',
				str(self.ParentedTotalListDict.keys()),
				'self.ParentedTotalSingularListDict.keys() is ',
				str(self.ParentedTotalSingularListDict.keys())
			]
		)
		''' 

		#Check
		if self.StructuringDoStr=='Pyplot' and self.StructuringTopDeriveStructurerVariable!=self:

			#record
			self.pyplot()

		#/#################/#
		# Call the base method
		#

		#call the base method
		BaseClass.propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable)
	"""

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

	def pyplotChart(self):

		#/#################/#
		# First shift in the grid
		#

		#Check
		if self.ManagementIndexInt>0:

			#debug
			'''
			self.debug(
					[
						'first we shift',
						'self.PyplotedParentPanelDerivePyploterVariable.PyplotedCursorIntsList is ',
						str(self.PyplotedParentPanelDerivePyploterVariable.PyplotedCursorIntsList),
						('self.',self,['PyplotingShapeIntsTuple','PyplotingShiftIntsTuple'])
					]
				)
			'''

			#get
			PreviousChartPyploter=self.ParentDeriveTeamerVariable.ManagementDict.getValue(
				self.ManagementIndexInt-1
			)

			#debug
			self.debug(
				[
					'We have getted the PreviousChartPyploter',
					'PreviousChartPyploter is ',
					SYS._str(PreviousChartPyploter)
				]
			)

			#shift
			if self.PyplotingShiftIntsTuple[0]>0:
				self.PyplotedParentPanelDerivePyploterVariable.PyplotedCursorIntsList[0
				]+=self.PyplotingShiftIntsTuple[0]+PreviousChartPyploter.PyplotingShapeIntsTuple[0]
			if self.PyplotingShiftIntsTuple[1]>0:
				self.PyplotedParentPanelDerivePyploterVariable.PyplotedCursorIntsList[1
				]+=self.PyplotingShiftIntsTuple[1]+PreviousChartPyploter.PyplotingShapeIntsTuple[1]

			#debug
			'''
			self.debug(
					[
						'Ok we have shifted',
						'now we link with the fig',
						('self.PyplotedParentPanelDerivePyploterVariable.',self.PyplotedParentPanelDerivePyploterVariable,
							['PyplotedCursorIntsList']),
					]
				)
			'''

		#set
		if self.PyplotedParentPanelDerivePyploterVariable!=None:
			self.PyplotedAnchorIntsList=copy.copy(
				self.PyplotedParentPanelDerivePyploterVariable.PyplotedCursorIntsList
			)

		#/#################/#
		# init
		#

		#debug
		'''
		self.debug(
				[
					'Ok we set an axes here',
					('self.',self,[
							'PyplotingGridIntsTuple',
							'PyplotedAnchorIntsList',
							'PyplotingShapeIntsTuple'
						]),
					''
				]
			)
		'''

		#init
		from matplotlib import pyplot
		self.PyplotedAxesVariable=pyplot.subplot2grid(
				self.PyplotedParentFigureDerivePyploterVariable.PyplotingGridIntsTuple, 
				self.PyplotedAnchorIntsList, 
				rowspan=self.PyplotingShapeIntsTuple[0],
				colspan=self.PyplotingShapeIntsTuple[1]
			)

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
		self.PyplotedAxesVariable._figure=self.PyplotedFigureVariable	

		#debug
		'''
		self.debug(
				[
					'Ok we have setted the axe'
				]
			)
		'''

	def pyplotDraw(self):

		#/#################/#
		# We mapArgument draw in the parent axes
		#

		#debug
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

		#map argument
		self.PyplotedLinesList.extend(
			self.PyplotedParentFigureDerivePyploterVariable.mapArgument(
				self.PyplotedParentChartDerivePyploterVariable.PyplotedAxesVariable,
				self.PyplotingDrawVariable
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

		#Check
		if self.ParentDeriveTeamerVariable!=None:

			#Check
			if self.ManagementIndexInt==(len(self.ParentDeriveTeamerVariable.ManagementDict)-1):

				#debug
				'''
				self.debug(
					[
						'I am the last draw of this axes !',
						'Lets the axes setting itself now',
						('self.PyplotedParentChartDerivePyploterVariable.',
							self.PyplotedParentChartDerivePyploterVariable,
							['PyplotingDrawVariable'])
					]
				)	
				'''

				#Check
				if self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable!=None:

					#/#################/#
					# We map argument in the axes
					#

					#debug
					'''
					self.debug(
						[
							'We chart in the parent axe',
							('self.',self,[
								'PyplotedParentChartDerivePyploterVariable'
							]),
							'self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable is ',
							SYS._str(self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable)
						]
					)
					'''

					#map argument
					self.PyplotedParentFigureDerivePyploterVariable.mapArgument(
						self.PyplotedParentChartDerivePyploterVariable.PyplotedAxesVariable,
						self.PyplotedParentChartDerivePyploterVariable.PyplotingChartVariable
					)

	def propertize_setPyplotedShiftTuplesList(self,_SettingValueVariable):

		#set
		self._PyplotedShiftTuplesList=_SettingValueVariable

		#debug
		'''
		self.debug(
				[
					'We bind a set of PyplotedShiftTuplesList here',
					'_SettingValueVariable is',
					str(_SettingValueVariable)
				]
			)
		'''

		#init
		self.PyplotedPanelShapeIntsList=list(_SettingValueVariable[0][0])

		#Check
		if len(_SettingValueVariable)>1:
		
			#shift
			for __PyplotedShiftTuple in _SettingValueVariable[1:]:

				#debug
				'''
				self.debug(
						[	
							'We shift with ',
							'__PyplotedShiftTuple is ',
							str(__PyplotedShiftTuple)
						]
					)
				'''

				#Check
				if __PyplotedShiftTuple[1][0]>0:

					#add
					self.PyplotedPanelShapeIntsList[0]+=__PyplotedShiftTuple[1][0]+__PyplotedShiftTuple[0][0]

				if __PyplotedShiftTuple[1][1]>0:

					#dd
					self.PyplotedPanelShapeIntsList[1]+=__PyplotedShiftTuple[1][1]+__PyplotedShiftTuple[0][1]

		#debug
		'''
		self.debug(
				[
					'in the end of the shift',
					('self.',self,[
						'PyplotedPanelShapeIntsList',
						'PyplotedCursorIntsList'
					])
				]
			)
		'''


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
					self.PrintingCopyVariable.PrintingInstanceSkipKeyStrsList.append(
						__KeyStr
					) if getattr(self.PrintingCopyVariable,__KeyStr)==None
					else None,
					[
						'PyplotedFigureVariable',
						'PyplotedAxesVariable'
					]
				)


		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

#</DefineClass>

#</DefinePrint>
PyploterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PyplotTooltipVariablesList',
		'PyplotingGridIntsTuple',
		'PyplotingShapeIntsTuple',
		'PyplotingDrawVariable',
		'PyplotingChartVariable',
		'PyplotingShiftIntsTuple',
		'PyplotedTeamTagStr',
		'PyplotedParentFigureDerivePyploterVariable',
		'PyplotedParentPanelDerivePyploterVariable',
		'PyplotedParentChartDerivePyploterVariable',
		#'PyplotedFigureVariable',
		#'PyplotedAxesVariable',
		'PyplotedLinesList',
		'PyplotedAnchorIntsList',
		'PyplotedShiftTuplesList',
		'PyplotedPanelShapeIntsList',
		'PyplotedCursorIntsList',
		'PyplotedParentSingularStr'
	]
)
#<DefinePrint>

