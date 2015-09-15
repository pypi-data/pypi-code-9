# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Figurer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Viewers.Viewer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo("Figurer","Figure","Figuring","Figured")
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Itemizers import Setter,Manager
import copy
#</ImportSpecificModules>

#<DefineLocals>
FigurePlotKeyStr='#plot'
FigureBarKeyStr='#bar'
FigureScatterKeyStr='#scatter'
FigureAxesKeyStr='#axes'
FigureMpld3KeyStr='#mpld3.plugins.'
class FigurerParentersClass(SYS.ParenterClass):pass
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class FigurerClass(BaseClass):
	
	def default_init(self,
						_FigurePyplotVariable=None,
						_FigureCartoonVariablesList=None,
						_FigureTooltipVariablesList=None,
						_FiguringGridIntsTuple=(20,20),
						_FiguringShapeIntsTuple=(1,1),
						_FiguringDrawVariable=None,
						_FiguringShiftIntsTuple=(0,1),
						_FiguredTeamTagStr="",
						_FiguredDeriveTeamerVariablesList=None,
						_FiguredPanelDeriveTeamerVariable=None,
						_FiguredAxesDeriveTeamerVariable=None,
						_FiguredAxesVariable=None,
						_FiguredAnchorIntsList=[0,0],
						_FiguredShiftTuplesList={
							'DefaultValueType':property,
							'PropertyInitVariable':None,
							'PropertyDocStr':'I am reactive when I am a Panel and want to know the space I take !'
						},
						_FiguredPanelShapeIntsList=None,
						_FiguredCursorIntsList=[0,0],
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

		#set
		self.TeamingValueClass=FigurerParentersClass

	def do_figure(self):	
		
		#/###################/#
		# First we get the children figurers and check what they are
		#

		#debug
		self.debug(
				[
					'We figure here',
					#('self.',self,['ViewFirstDeriveViewerVariable'])
					'self.TeamDict.keys() is ',
					str(self.TeamDict.keys())
				]
			)

		#filter
		FiguredTeamTagStrsList=SYS._filter(
			lambda __KeyStr:
			__KeyStr in ['Panels','Axes','Plots'],
			self.TeamDict.keys()
		)

		#Check
		if len(FiguredTeamTagStrsList)==1:

			#filter
			self.FiguredTeamTagStr=FiguredTeamTagStrsList[0]

			#get
			self.FiguredDeriveTeamerVariablesList=self.TeamDict[
				self.FiguredTeamTagStr
			].ManagementDict.values()
		
		#debug
		'''
		self.debug(
				[
					('self.',self,[
							'FiguredTeamTagStr',
							#'FiguredDeriveTeamerVariablesList'
						])
				]
			)
		'''

		#/###################/#
		# do something before descending a figure call
		#

		if self.FiguredTeamTagStr=='Panels':

			#debug
			'''
			self.debug(
					[
						'I am the top figurer...'
					]
				)
			'''

		elif self.FiguredTeamTagStr=='Axes' or self.ParentDeriveTeamerVariable.TeamTagStr=='Panels':

			#/###############/#
			# Add an axe for the symbol of the panel
			#

			#debug
			'''
			self.debug(
					[
						'We transform the team dict Axes to add a panel axe',
						'self.TeamDict[\'Axes\'] is ',
						SYS._str(self.TeamDict['Axes'])
					]
				)
			'''

			#team
			self.team('Axes')

			#debug
			'''
			self.debug(
					[
						'before setting',
						'self.TeamedValueVariable.ManagementDict is ',
						SYS._str(self.TeamedValueVariable.ManagementDict),
						'Manager.ManagementDict is ',
						str(Manager.ManagementDict)
					]
				)
			'''

			#map an add
			map(
				lambda __DeriveFigurer:
				setattr(
					__DeriveFigurer,
					'ManagementIndexInt',
					__DeriveFigurer.ManagementIndexInt+1
				),
				self.TeamedValueVariable.ManagementDict.values()
			)

			#update
			self.TeamedValueVariable.ManagementDict=Manager.ManagementDict(
				[
					(
						'Panel',SYS.FigurerClass(
							**{

								'ManagementTagStr':'Panel',
								'ManagementIndexInt':0,
								'ParentDeriveTeamerVariable':self.TeamedValueVariable,
								'ViewFirstDeriveViewerVariable':self.ViewFirstDeriveViewerVariable,
								'FigurePyplotVariable':self.FigurePyplotVariable,
								'FiguringShapeIntsTuple':(1,1),
								'FiguringDrawVariable':{
									'#axes':
									{
										'set_axis_off':[],
										#'text':'$\\textbf{'+self.ManagementTagStr+'}$'
									}
								},
								'FiguredPanelDeriveTeamerVariable':self,
							}
						)
					)
				],
				**self.TeamedValueVariable.ManagementDict
			)

			#debug
			'''
			self.debug(
					[
						'after setting',
						'self.TeamedValueVariable.ManagementDict is ',
						SYS._str(self.TeamedValueVariable.ManagementDict)
					]
				)
			'''

			#Add maybe a shift in the next figure
			if len(self.TeamedValueVariable.ManagementDict)>1:

				#debug
				'''
				self.debug(
						[
							'We add a shift down and right to the next figure',
							'self.TeamedValueVariable.ManagementDict.get(1) is',
							SYS._str(self.TeamedValueVariable.ManagementDict.get(1))
						]
					)
				'''

				#set
				self.TeamedValueVariable.ManagementDict.get(1).FiguringShiftIntsTuple=(1,1)

			#/##################/#
			# There are some Axes to count
			#

			#map get
			self.FiguredShiftTuplesList=map(
					lambda __DeriveFigurer:
					(
						__DeriveFigurer.FiguringShapeIntsTuple,
						__DeriveFigurer.FiguringShiftIntsTuple
					),
					self.TeamDict['Axes'].ManagementDict.values()
				)

			#debug
			'''
			self.debug(
					[
						'I am a still Panel...',
						('self.',self,[
							'FiguredShiftTuplesList',
							'ManagementIndexInt'
						])
					]
				)
			'''

			#/###############/#
			# Determine what is the anchor considering the one of the last panel
			#

			#Check
			if self.ManagementIndexInt>0:

				#debug
				'''
				self.debug(
					[
						'We get the previous Panel',
						'self.ParentDeriveTeamerVariable.ManagementDict is ',
						SYS._str(self.ParentDeriveTeamerVariable.ManagementDict)
					]
				)
				'''

				#get the previous
				FiguredPreviousPanelFigurer=self.ParentDeriveTeamerVariable.ManagementDict.get(
					self.ManagementIndexInt-1
				)

				#debug
				'''
				self.debug(
						[
							'We look for the previous panel...',
							#('FiguredPreviousPanelFigurer.',FiguredPreviousPanelFigurer,[
							#		'FiguredAnchorIntsList',
							#		'FiguredPanelShapeIntsList'
							#	]
							#)
						]
					)
				'''

				#Check
				if self.FiguringShiftIntsTuple[0]>0:

					#add
					self.FiguredAnchorIntsList[0]=FiguredPreviousPanelFigurer.FiguredAnchorIntsList[0
							]+self.FiguringShiftIntsTuple[0]+FiguredPreviousPanelFigurer.FiguredPanelShapeIntsList[0]+1

				if self.FiguringShiftIntsTuple[1]>0:

					#add
					self.FiguredAnchorIntsList[1]=FiguredPreviousPanelFigurer.FiguredAnchorIntsList[1
							]+self.FiguringShiftIntsTuple[1]+FiguredPreviousPanelFigurer.FiguredPanelShapeIntsList[1]+1

				#debug
				self.debug(
						[
							'we have setted the new anchor',
							('self.',self,['FiguredAnchorIntsList'])
						]
					)

			#/###############/#
			# Init the Cursor for after
			#

			#init
			self.FiguredCursorIntsList=copy.copy(self.FiguredAnchorIntsList)


			#/###############/#
			# Look maybe at a Panel without Axes and Plots
			#

			#Check
			if len(self.TeamDict['Axes']==1):

				#debug
				'''
				self.debug(
						[
							'I am a Panel without Axes and Plots',
							'So we just set an axe here'
						]
					)
				'''

				#set
				self.setAxes()

				#/###################/#
				# if there axes setted then apply the draw set variable 
				#

				#Check
				if self.FiguredAxesVariable!=None:

					#debug
					'''
					self.debug(
							[
								'There are axes so command the figuring draw variable',
								('self.',self,[
									'FiguringDrawVariable'
								])
							]
						)
					'''

					#commad self
					#self.command(self,self.FiguringDrawVariable)
					#self.command(self,[])
					self['#map@set'](self.FiguringDrawVariable)

				#return
				return

		elif self.FiguredTeamTagStr=='Plots':

			#debug
			'''
			self.debug(
					[
						'I am an Axes..',
						('self.',self,['ParentDeriveTeamerVariable'])
					]
				)
			'''

			#get the parent panel
			self.FiguredPanelDeriveTeamerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#debug
			'''
			self.debug(
					[
						'I am still an Axes..',
						('self.',self,[
							'FiguredPanelDeriveTeamerVariable',
							#'ViewFirstDeriveViewerVariable',
							'FiguredAnchorIntsList',
							'FiguringShapeIntsTuple'
						])
					]
				)
			'''

			#alias
			self.FiguringGridIntsTuple=self.ViewFirstDeriveViewerVariable.FiguringGridIntsTuple
			self.setAxes()

			#debug
			'''
			self.debug(
					[
						'I am still an Axes..',
						('self.',self,['FiguredAxesVariable'])
					]
				)
			'''

		else:

			#debug
			'''
			self.debug(
					[
						'I dont have such panels axes plots...',
						'So I can be a plot or the top one axe one plot figurer'
					]
				)
			'''

			#Check
			if self!=self.ViewFirstDeriveViewerVariable:

				#get
				FiguredParentParentVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

				#debug
				'''
				self.debug(
					[
						'FiguredParentParentVariable.ParentDeriveTeamerVariable.TeamTagStr is ',
						FiguredParentParentVariable.ParentDeriveTeamerVariable.TeamTagStr,
						'FiguredParentParentVariable is ',
						SYS._str(FiguredParentParentVariable)
					]
				)
				'''

				#Check
				if FiguredParentParentVariable.ParentDeriveTeamerVariable.TeamTagStr=='Views':

					#/###################/#
					# build a FiguredAxesVariables
					#

					#debug
					'''
					self.debug(
							[
								'I am a panel without Axes and Plots so just set an axis here...',
							]
						)
					'''

					#alias
					self.FiguringGridIntsTuple=self.ViewFirstDeriveViewerVariable.FiguringGridIntsTuple

					#set
					self.setAxes()

				#Check
				elif FiguredParentParentVariable.ParentDeriveTeamerVariable.TeamTagStr=='Panels':

					#alias
					self.FiguredPanelDeriveTeamerVariable=FiguredParentParentVariable

					#/###################/#
					# build a FiguredAxesVariables
					#

					#debug
					'''
					self.debug(
							[
								'I am an axes without Plots so just set an axis here...',
							]
						)
					'''

					#alias
					self.FiguringGridIntsTuple=self.ViewFirstDeriveViewerVariable.FiguringGridIntsTuple
					self.FiguredAnchorIntsList=self.FiguredPanelDeriveTeamerVariable.FiguredCursorIntsList

					#set
					self.setAxes()

				else:

					#/###################/#
					# point to the FiguredAxesVariable
					#

					#debug
					self.debug(
							[
								'I am Plot..',
								'I set my FiguredAxesVariables corresponding to my parent one',
								#'FiguredParentParentVariable is ',
								#SYS._str(FiguredParentParentVariable),
								'FiguredParentParentVariable.ManagementTagStr is ',
								FiguredParentParentVariable.ManagementTagStr,
								'FiguredParentParentVariable.FiguredAxesVariable is ',
								FiguredParentParentVariable.FiguredAxesVariable,
							]
						)

					#get the parent panel
					self.FiguredAxesDeriveTeamerVariable=FiguredParentParentVariable

					#get the one of the parent
					self.FiguredAxesVariable=self.FiguredAxesDeriveTeamerVariable.FiguredAxesVariable

				#debug
				self.debug(
						[
							'I have definitely an axes..',
							('self.',self,['FiguredAxesVariable'])
						]
					)

				#/###################/#
				# if there axes setted then apply the draw set variable 
				#

				#Check
				if self.FiguredAxesVariable!=None:

					#debug
					'''
					self.debug(
							[
								'There are axes so command the figuring draw variable',
								('self.',self,[
									'FiguringDrawVariable'
								])
							]
						)
					'''

					#commad self
					#self.command(self,self.FiguringDrawVariable)
					#self.command(self,[])
					self['#map@set'](self.FiguringDrawVariable)

				#/###################/#
				# if it is the last then trigger the axes to set also
				#

				#Check
				if self.ManagementIndexInt==(len(self.ParentDeriveTeamerVariable.ManagementDict)-1):

					#debug
					'''
					self.debug(
						[
							'I am the last plot of this axes !',
							'Lets the axes setting itself now',
							('self.FiguredAxesDeriveTeamerVariable',
								self.FiguredAxesDeriveTeamerVariable,
								['FiguringDrawVariable'])
						]
					)
					'''

					#commad self
					self.FiguredAxesDeriveTeamerVariable['#map@set'](
						self.FiguredAxesDeriveTeamerVariable.FiguringDrawVariable
					)


			else:

				#debug
				self.debug(
						[
							'I am the top figurer but with just one axes..',
							('self.',self,['FiguringGridIntsTuple'])
						]
					)

				#Set the size of the grid to this just one plot
				self.FiguringGridIntsTuple=(1,1)

				#get the parent panel
				self.FiguredPanelDeriveTeamerVariable=self.ParentDeriveTeamerVariable

				#init
				self.setAxes()

				#map set
				self['#map@set'](
					self.FiguringDrawVariable
				)		

	def mimic_view(self):

		#import mpld3
		import mpld3

		#fig to html
		self.ViewedHtmlStr=mpld3.fig_to_html(
			self.FigurePyplotVariable,
			template_type="simple"
		)

		#call the base method
		BaseClass.view(self)

	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#call the parent method
		BaseClass.propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable)

		#debug
		'''
		self.debug(
				[
					'We have parented !',
					('self.',self,['ViewFirstDeriveViewerVariable'])
				]
			)
		'''

		#/###############/#
		# If it is the top then init the figure
		#

		#Check
		if self.ViewFirstDeriveViewerVariable==self:

			#debug
			'''
			self.debug(
					[
						'We init a figure'
					]
				)
			'''

			#import pyplot
			from matplotlib import pyplot

			#subplots
			self.FigurePyplotVariable = pyplot.figure()

		else:

			#debug
			'''
			self.debug(
					[
						'We just do an alias'
					]
				)
			'''

			#alias
			self.FigurePyplotVariable=self.ViewFirstDeriveViewerVariable.FigurePyplotVariable

		#/#################/#
		# Lets go for figure
		#

		#debug
		'''
		self.debug(
				'We are going to figure'
			)
		'''

		#figure
		self.figure()

	def mimic_set(self):

		#Check
		if self.SettingKeyVariable in [
											FigurePlotKeyStr,
											FigureScatterKeyStr,
											FigureBarKeyStr
										]:

			#debug
			'''
			self.debug(
					[
						'before plot',
						('self.',self,[
							#'ViewDeriveControllerVariable',
							'SettingValueVariable'
						])
					]
				)
			'''

			#init
			FigurePlotArgumentDict=Setter.ArgumentDict(
					self.SettingValueVariable,
					self.ViewDeriveControllerVariable
				)

			#debug
			'''
			self.debug(
					[
						'We plot here',
						'FigurePlotArgumentDict is',
						SYS._str(FigurePlotArgumentDict)
					]
				)
			'''

			#plot
			self.FigureCartoonVariablesList.append(
				self.FiguredAxesVariable.plot(
					*FigurePlotArgumentDict['LiargVariablesList'],
					**FigurePlotArgumentDict['KwargVariablesDict']
				)[0]
			)

			#debug
			'''
			self.debug(
				[
					('self.',self,['FigureCartoonVariablesList']),
					#str(self.FigureCartoonVariablesList[0][0]),
				]
			)
			'''

			#return 
			return {'HookingIsBool':False}

		elif self.SettingKeyVariable==FigureAxesKeyStr:

			#debug
			'''
			self.debug(
					[
						'before axes',
						('self.',self,[
							#'ViewDeriveControllerVariable',
							'FiguredAxesVariable'
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
								self.ViewDeriveControllerVariable
							)
					),
					SYS.SetList(
						self.SettingValueVariable
					)
				)

			
			#/#################/#
			# Special case for the legend
			#

			#dict
			ArgumentDict=dict(ArgumentTuplesList)
			if 'legend' in ArgumentDict:

				"""
				#Check
				if '#kwarg' not in ArgumentDict['legend']:
					ArgumentDict['legend']['#kwarg']={}

				#add
				ArgumentDict['legend']['#kwarg']['handles']=SYS.flat(
						map(
							lambda __Figurer:
							__Figurer.FigureCartoonVariablesList,
							self.TeamDict['Plots'].ManagementDict.values()
						)
					)
				"""

				#legend
				self.FiguredAxesVariable.legend()

				#link
				#ArgumentTuplesList[SYS.unzip(ArgumentTuplesList,[0]).index('legend')]=(
				#	'legend',
				#	ArgumentDict['legend']
				#)

				#remove
				del ArgumentTuplesList[SYS.unzip(ArgumentTuplesList,[0]).index('legend')]

			#debug
			self.debug(
					[
						'We axe here',
						'ArgumentTuplesList is ',
						SYS._str(ArgumentTuplesList)
					]
				)
			
			#map
			map(
					lambda __ArgumentTuple:
					getattr(
						self.FiguredAxesVariable,
						__ArgumentTuple[0]
					)()
					if len(__ArgumentTuple[1]['LiargVariablesList']
						)==0 and __ArgumentTuple[1]['KwargVariablesDict']==None
					else(
						getattr(
							self.FiguredAxesVariable,
							__ArgumentTuple[0],
							**__ArgumentTuple[1]['KwargVariablesDict']
						)()
						if len(__ArgumentTuple[1]['LiargVariablesList']
						)==0
						else(
							getattr(
								self.FiguredAxesVariable,
								__ArgumentTuple[0]
							)(
								*__ArgumentTuple[1]['LiargVariablesList'],
								**__ArgumentTuple[1]['KwargVariablesDict']
							) 
							if __ArgumentTuple[1]['KwargVariablesDict']!=None
							else
							getattr(
								self.FiguredAxesVariable,
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
			FigureMpld3KeyStr):

			#deprefix
			ToolTipKeyStr=SYS.deprefix(
					self.SettingKeyVariable,
					FigureMpld3KeyStr
				)

			#debug
			'''
			self.debug(
					[
						'before plugins',
						('self.',self,['ViewDeriveControllerVariable'])
					]
				)
			'''

			#init
			FigurePluginArgumentDict=Setter.ArgumentDict(
					self.SettingValueVariable,
					self.ViewDeriveControllerVariable
				)

			#debug
			'''
			self.debug(
					[
						'We plugin here',
						'FigurePluginArgumentDict is ',
						SYS._str(FigurePluginArgumentDict)
					]
				)
			'''

			#plugin
			from mpld3 import plugins
			self.FigureTooltipVariablesList=map(
				lambda __FigureCartoonVariable:
				getattr(
					plugins,
					ToolTipKeyStr
				)(
					*[
						__FigureCartoonVariable
					]+FigurePluginArgumentDict['LiargVariablesList'],
					**FigurePluginArgumentDict['KwargVariablesDict']
				),
				self.FigureCartoonVariablesList
			)

			#debug
			'''
			self.debug(
					[
						('self.',self,['FigureTooltipVariablesList'])
					]
				)
			'''
			
			#connect
			map(
				lambda __FigureTooltipVariable:
				plugins.connect(
					self.FigurePyplotVariable,
					__FigureTooltipVariable
				),
				self.FigureTooltipVariablesList
			)

			#return 
			return {'HookingIsBool':False}

		#call the base method
		BaseClass.set(self)

	def setAxes(self):

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
						'self.FiguredPanelDeriveTeamerVariable.FiguredCursorIntsList is ',
						str(self.FiguredPanelDeriveTeamerVariable.FiguredCursorIntsList),
						('self.',self,['FiguringShapeIntsTuple','FiguringShiftIntsTuple'])
					]
				)
			'''

			#get
			FiguredPreviousAxesFigurer=self.ParentDeriveTeamerVariable.ManagementDict.get(self.ManagementIndexInt-1)

			#shift
			if self.FiguringShiftIntsTuple[0]>0:
				self.FiguredPanelDeriveTeamerVariable.FiguredCursorIntsList[0
				]+=self.FiguringShiftIntsTuple[0]+FiguredPreviousAxesFigurer.FiguringShapeIntsTuple[0]
			if self.FiguringShiftIntsTuple[1]>0:
				self.FiguredPanelDeriveTeamerVariable.FiguredCursorIntsList[1
				]+=self.FiguringShiftIntsTuple[1]+FiguredPreviousAxesFigurer.FiguringShapeIntsTuple[1]

			#debug
			'''
			self.debug(
					[
						'Ok we have shifted',
						'now we link with the fig',
						('self.FiguredPanelDeriveTeamerVariable.',self.FiguredPanelDeriveTeamerVariable,
							['FiguredCursorIntsList']),
					]
				)
			'''

		#set
		self.FiguredAnchorIntsList=copy.copy(
			self.FiguredPanelDeriveTeamerVariable.FiguredCursorIntsList
		)

		#/#################/#
		# init
		#

		#debug
		self.debug(
				[
					'Ok we set an axes here',
					('self.',self,[
							'FiguringGridIntsTuple',
							'FiguredAnchorIntsList',
							'FiguringShapeIntsTuple'
						]),
					''
				]
			)

		#init
		from matplotlib import pyplot
		self.FiguredAxesVariable=pyplot.subplot2grid(
				self.FiguringGridIntsTuple, 
				self.FiguredAnchorIntsList, 
				rowspan=self.FiguringShapeIntsTuple[0],
				colspan=self.FiguringShapeIntsTuple[1]
			)

		#debug
		'''
		self.debug(
				[
					'Ok we have initiated the axes',
					('self.',self,['FiguredAxesVariable'])
				]
			)
		'''

		#/#################/#
		# link to the fig
		#

		#link
		self.FiguredAxesVariable._figure=self.FigurePyplotVariable	

		#debug
		'''
		self.debug(
				[
					'Ok we have setted the axe'
				]
			)
		'''

	def propertize_setFiguredShiftTuplesList(self,_SettingValueVariable):

		#set
		self._FiguredShiftTuplesList=_SettingValueVariable

		#debug
		'''
		self.debug(
				[
					'We bind a set of FiguredShiftTuplesList here',
					'_SettingValueVariable is',
					str(_SettingValueVariable)
				]
			)
		'''

		#init
		self.FiguredPanelShapeIntsList=list(_SettingValueVariable[0][0])

		#Check
		if len(_SettingValueVariable)>1:
		
			#shift
			for __FiguredShiftTuple in _SettingValueVariable[1:]:

				#debug
				'''
				self.debug(
						[	
							'We shift with ',
							'__FiguredShiftTuple is ',
							str(__FiguredShiftTuple)
						]
					)
				'''

				#Check
				if __FiguredShiftTuple[1][0]>0:

					#add
					self.FiguredPanelShapeIntsList[0]+=__FiguredShiftTuple[1][0]+__FiguredShiftTuple[0][0]

				if __FiguredShiftTuple[1][1]>0:

					#dd
					self.FiguredPanelShapeIntsList[1]+=__FiguredShiftTuple[1][1]+__FiguredShiftTuple[0][1]

		#debug
		self.debug(
				[
					'in the end of the shift',
					('self.',self,[
						'FiguredPanelShapeIntsList',
						'FiguredCursorIntsList'
					])
				]
			)


#</DefineClass>

#</DefinePrint>
FigurerClass.PrintingClassSkipKeyStrsList.extend(
	[
		#'FigurePyplotVariable',
		'FigureCartoonVariablesList',
		'FigureTooltipVariablesList',
		'FiguringGridIntsTuple',
		'FiguringShapeIntsTuple',
		'FiguringDrawVariable',
		'FiguringShiftIntsTuple',
		'FiguredTeamTagStr',
		'FiguredDeriveTeamerVariablesList',
		'FiguredPanelDeriveTeamerVariable',
		'FiguredAxesDeriveTeamerVariable',
		'FiguredAxesVariable',
		'FiguredAnchorIntsList',
		'FiguredShiftTuplesList',
		'FiguredPanelShapeIntsList',
		'FiguredCursorIntsList'
	]
)
#<DefinePrint>

#<DefineLocals>
FigurerParentersClass.ManagingValueClass=FigurerClass
#<DefineLocals>
