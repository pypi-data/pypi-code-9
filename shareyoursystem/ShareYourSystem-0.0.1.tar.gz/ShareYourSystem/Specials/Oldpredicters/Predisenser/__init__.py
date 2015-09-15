# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


"""

#<DefineAugmentation>
import ShareYourSystem as SYS
import types
BaseModuleStr="ShareYourSystem.Specials.Oldpredicters.Oldpredicter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Predisenser','Predisense','Predisensing','Predisensed')
#</DefineAugmentation>

#<ImportSpecificModules>
import scipy.stats
import numpy as np
#</ImportSpecificModules>

#<DefineLocals>
def getKrenelFloatsArray(
		_LevelFloatsTuple=None,
		_TimeFloatsTuple=None,
		_RunTimeFloat=100.,
		_StepTimeFloat=0.1,
	):

	#get the bins
	BinsInt=_RunTimeFloat/_StepTimeFloat

	#init
	KrenelFloatsArray=_LevelFloatsTuple[0]*np.ones(
		BinsInt,
		dtype=type(_LevelFloatsTuple[0])
	)

	#Debug
	'''
	print('getKrenelFloatsArray')
	print('_TimeFloatsTuple[0]/_StepTimeFloat:_TimeFloatsTuple[1]/_StepTimeFloat')
	print(_TimeFloatsTuple[0]/_StepTimeFloat,_TimeFloatsTuple[1]/_StepTimeFloat)
	print('_LevelFloatsTuple[1] is '+str(_LevelFloatsTuple[1]))
	print('')
	'''

	#put the second level
	KrenelFloatsArray[
		int(_TimeFloatsTuple[0]/_StepTimeFloat):int(_TimeFloatsTuple[1]/_StepTimeFloat)
	]=_LevelFloatsTuple[1]

	#return
	return KrenelFloatsArray

def getFourierFloatsArray(
		_RunTimeFloat=100.,
		_StepTimeFloat=0.1,
	):

	#get the bins
	BinsInt=_RunTimeFloat/_StepTimeFloat

	#compute
	FourierFloatsArray=np.array(
		map(
			lambda __TimeFloat:
			sum(
				map(
					lambda __FrequencyFloat,__PhaseFloat: 
					np.cos(2.*np.pi*0.001*__TimeFloat*__FrequencyFloat+__PhaseFloat),
					[200.],
					[np.pi/2.]
				)
			),
			np.arange(0.,_RunTimeFloat,_StepTimeFloat)
		)
	)
	
	#Debug
	'''
	print('getFourierFloatsArray l 86')
	print('FourierFloatsArray is ')
	print(FourierFloatsArray)
	print('')
	'''

	#return
	return FourierFloatsArray


def getTickFloatsArray(_LimList,_SampleFloat):

	#Debug
	'''
	print('getTickFloatsArray l 64')
	print('_LimList is')
	print(_LimList)
	print('_SampleFloat is ')
	print(_SampleFloat)
	print('')
	'''
	
	#return
	return np.array(list(np.arange(
		_LimList[0],
		_LimList[1],
		(_LimList[1]-_LimList[0])/float(_SampleFloat)
	))+[_LimList[1]])

SYS.getTickFloatsArray=getTickFloatsArray
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PredisenserClass(BaseClass):
	
	def default_init(self,
						_PredisensingRunTimeFloat=100.,
						_PredisensingStepTimeFloat=0.1,
						_PredisensingMonitorIntsList=None,
						_PredisensingKrenelClampFloat=1.,
						_PredisensingFourierClampFloat=0.1,
						_PredisensedTimeTraceFloatsArray=None,
						_PredisensedCommandTraceFloatsArray=None,
						_PredisensedInputCurrentTraceFloatsArray=None,
						_PredisensedInitialSensorFloatsArray=None,
						_PredisensedSensorTraceFloatsArray=None,
						_PredisenseCommandColorTuplesList=None,
						_PredisenseSensorColorTuplesList=None,
						**_KwargVariablesDict
					):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_predisense(self):

		#/#################/#
		# External care : Prepare time and the command
		#

		#arange
		self.PredisensedTimeTraceFloatsArray=np.arange(
			0.,
			self.PredisensingRunTimeFloat,
			self.PredisensingStepTimeFloat
		)

		#array
		self.PredisensedCommandTraceFloatsArray=np.array(
			map(
				lambda __IndexInt:
				getKrenelFloatsArray(
					[
						0.,
						1.
					],
					[
						self.PredisensingRunTimeFloat/4.,
						3.*self.PredisensingRunTimeFloat/4.
						#1.5*self.PredisensingRunTimeFloat/4.,
					],
					self.PredisensingRunTimeFloat,
					self.PredisensingStepTimeFloat
				)*(
			self.PredisensingKrenelClampFloat+self.PredisensingFourierClampFloat*getFourierFloatsArray(
							self.PredisensingRunTimeFloat,
							self.PredisensingStepTimeFloat
						)
				),
				xrange(self.OldpredictingSensorsInt)
			)
		)

		#set
		self.PredisensedInputCurrentTraceFloatsArray=self.PredisensedCommandTraceFloatsArray*self.OldpredictingConstantTimeFloat

		#/#################/#
		# Prepare the initial conditions
		#

		#random sensors
		PredisensedInitialSensorFloatsArray=0.1*max(
				self.PredisensingKrenelClampFloat,
				self.PredisensingFourierClampFloat
			)*scipy.stats.uniform.rvs(
			size=self.OldpredictingSensorsInt
		)
		
		#/#################/#
		# Shape the size of the sensors run
		#

		#init sensors
		self.PredisensedSensorTraceFloatsArray=np.zeros(
				(
					self.OldpredictingSensorsInt,
					len(self.PredisensedTimeTraceFloatsArray)
				)
			)
		self.PredisensedSensorTraceFloatsArray[:,0]=PredisensedInitialSensorFloatsArray

		#/#################/#
		# integrativ Loop
		#

		#for loop
		for __IndexInt in xrange(1,len(self.PredisensedTimeTraceFloatsArray)):

			#/#################/#
			# Sensor part
			#

			#debug
			'''
			self.debug(
					[
						'shape(self.PredisensedCommandTraceFloatsArray) is '+str(
							np.shape(self.PredisensedCommandTraceFloatsArray)
						),
						'shape(self.PredisensedSensorTraceFloatsArray) is '+str(
							np.shape(self.PredisensedSensorTraceFloatsArray)
						),
						('self.',self,[
							'OldpredictedSensorJacobianFloatsArray'
						])
					]
				)
			'''
			
			#Current
			PredisensedSensorCurrentFloatsArray=np.dot(
				self.OldpredictedSensorJacobianFloatsArray,
				self.PredisensedSensorTraceFloatsArray[:,__IndexInt-1]
			)+self.PredisensedCommandTraceFloatsArray[:,__IndexInt-1]

			#/#################/#
			# Euler part
			#

			#sensor
			self.PredisensedSensorTraceFloatsArray[
				:,
				__IndexInt
			]=self.PredisensedSensorTraceFloatsArray[
				:,
				__IndexInt-1
			]+PredisensedSensorCurrentFloatsArray*self.PredisensingStepTimeFloat

			#set
			LocalDict=locals()

	def mimic_view(self):
		
		#debug
		'''
		self.debug(
				[
					('self.',self,['PredisensingMonitorIntsList'])
				]
			)
		'''

		#/#################/#
		# Build the colors
		#	

		self.PredisenseCommandColorTuplesList=SYS.getColorTuplesList(
			'black','red',len(self.PredisensingMonitorIntsList)+3,_PlotBool=False
		)[3:]

		self.PredisenseSensorColorTuplesList=SYS.getColorTuplesList(
			'black','blue',len(self.PredisensingMonitorIntsList)+3,_PlotBool=False
		)[3:]

		#debug
		'''
		self.debug(
				[
					'We have built the colors',
					('self.',self,[
						'PredisenseCommandColorTuplesList'
						'PredisenseSensorColorTuplesList'])
				]
			)
		'''
		
		#/#################/#
		# Build the input-unit traces axes
		#

		#init
		self.mapSet(
			{
				'-Charts':[
					('ManagingBeforeSetVariable',
					{
						'PyplotingShapeIntsTuple':(5,15),
						'#copy:PyplotingChartVariable':
						[
							('set_xticks',{
									'#liarg:#map@get':[
										">>SYS.set(SYS,'TimeTicksArray',SYS.getTickFloatsArray([0.,self.PredisensingRunTimeFloat],4)).TimeTicksArray"
									]	
							}),
							('set_xticklabels',{
								'#liarg:#map@get':[
									">>map(lambda __Float:'$%.0f$'%__Float,SYS.TimeTicksArray)"
								]
							}),
							('set_xlim',{
								'#liarg:#map@get':[0.,'>>self.PredisensingRunTimeFloat']
							})
						]
					}),
					('|Sensor',{
						'-Draws':{
							'#map@set':map(
								lambda __IntsTuple:
								(
									'|'+str(__IntsTuple[0]),
									{
										'PyplotingDrawVariable':
										[
											('plot',
												{
													'#liarg:#map@get':[
														'PredisensedTimeTraceFloatsArray',
														'>>self.PredisensedInputCurrentTraceFloatsArray.__getitem__('+str(__IntsTuple[1])+')'
													],
													'#kwarg':{
														'label':'$\\tau_{D}c_{'+str(__IntsTuple[1])+'}$',
														'linestyle':'-',
														'color':self.PredisenseCommandColorTuplesList[__IntsTuple[0]]
													}
											}),
											('plot',
												{
													'#liarg:#map@get':[
														'PredisensedTimeTraceFloatsArray',
														'>>self.PredisensedSensorTraceFloatsArray['+str(__IntsTuple[1])+',:]'
													],
													'#kwarg':{
														'color':self.PredisenseSensorColorTuplesList[__IntsTuple[0]],
														'label':'$x_{'+str(__IntsTuple[1])+'}$',
														'linewidth':3,
														'linestyle':'-'
													}
											})
										]
									}
								),
								enumerate(self.PredisensingMonitorIntsList)
							)	
						},
						'PyplotingChartVariable.extend':
						[[
							('set_ylabel','$\\tau_{D}c(t),\ x(t)$'),
							('set_ylim',{'#liarg:#map@get':[
								"".join([
									">>SYS.set(SYS,'SensorLimFloatsArray',",
									"[min(-0.1,self.PredisensedSensorTraceFloatsArray.min()),1.5*max(self.PredisensingKrenelClampFloat,self.PredisensingFourierClampFloat)*self.OldpredictingConstantTimeFloat]",
									').SensorLimFloatsArray'
								])]
							}),
							('set_yticks',{
								'#liarg:#map@get':[
									"".join([
										">>SYS.set(SYS,'SensorTickFloatsArray',",
										"map(lambda __Float:float('%.2f'%__Float),",
										"SYS.getTickFloatsArray(",
										"SYS.SensorLimFloatsArray,3",
										"))).SensorTickFloatsArray"
									])
								]
							}),
							('set_yticklabels',{
								'#liarg:#map@get':[
									"".join([
										">>SYS.set(SYS,'SensorTickStrsArray',",
										"map(lambda __Float:'$'+str(__Float)+'$',",
										"SYS.SensorTickFloatsArray)).SensorTickStrsArray"
										])
								]
							}),
							('tick_params',{
								'#kwarg':{
									'length':10,
									'width':5,
									'which':'major'
								}
							}),
							('tick_params',{
								'#kwarg':{
									'length':5,
									'width':2,
									'which':'minor'
								}
							}),
							('xaxis.set_ticks_position',
								{
									'#liarg':['bottom']
								}
							),
							('yaxis.set_ticks_position',
								{
									'#liarg':['left']
								}
							),
							('legend',{
								'#liarg':[],
								'#kwarg':{
									'fontsize':10,
									'shadow':True,
									'fancybox':True,
									'ncol':max(1,len(self.PredisensingMonitorIntsList)/2),
									'loc':2,
									'bbox_to_anchor':(1.05, 1)
								}
							})
						]]
					})
				]
			}				
		)

		#debug
		self.debug(
			'Ok we have setted the plots'
		)

		#call the base method
		BaseClass.view(self)

#</DefineClass>

#</DefinePrint>
PredisenserClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PredisensingRunTimeFloat',
		'PredisensingStepTimeFloat',
		'PredisensingClampFloat',
		'PredisensingMonitorIntsList',
		'PredisensedTimeTraceFloatsArray',
		'PredisensedInputCurrentTraceFloatsArray',
		'PredisensedCommandTraceFloatsArray',
		'PredisensedInitialSensorFloatsArray',
		'PredisensedSensorTraceFloatsArray',
		'PredisenseCommandColorTuplesList',
		'PredisenseSensorColorTuplesList'
	]
)
#<DefinePrint>

