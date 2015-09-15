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
BaseModuleStr="ShareYourSystem.Specials.Oldpredicters.Predisenser"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Predirater','Predirate','Predirating','Predirated')
#</DefineAugmentation>

#<ImportSpecificModules>
import scipy.stats
import numpy as np
#</ImportSpecificModules>

#<DefineLocals>
def getThresholdArray(_Variable,_ThresholdFloat=1.):

	#Check
	if type(_Variable) in [np.float64,float,int]:

		#return
		return max(
				min(
					_Variable,
					_ThresholdFloat
					),
				-_ThresholdFloat
			)
	else:

		#return
		return map(
			lambda __ElementVariable:
			getThresholdArray(
				__ElementVariable,
				_ThresholdFloat=_ThresholdFloat
			),
			_Variable
		)
SYS.getThresholdArray=getThresholdArray
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PrediraterClass(BaseClass):
	
	def default_init(self,

						_PrediratingConstantTimeFloat=10.,
						_PrediratingTransferVariable=np.tanh,
						_PrediratingMonitorIntsList=None,
						_PrediratingInititalFloat=0.1,
						_PrediratingCommandNoiseFloat=0.,
						_PrediratingRateNoiseFloat=0.,
						_PrediratingSymmetryFloat=1.,
									
						_PrediratedLeakWeigthFloatsArray=None,		
						_PrediratedLeakExactFastLateralWeigthFloatsArray=None,
						_PrediratedTotalPerturbativeFastLateralWeigthFloatsArray=None,
						_PrediratedInitialRateFloatsArray=None,
						_PrediratedControlDecoderWeigthFloatsArray=None,
						
						_PrediratedPerturbativeUnitTraceFloatsArray=None,
						_PrediratedExactUnitTraceFloatsArray=None,
						_PrediratedControlUnitTraceFloatsArray=None,
						
						_PrediratedPerturbativeDecoderTraceFloatsArray=None,
						_PrediratedExactDecoderTraceFloatsArray=None,
						_PrediratedControlDecoderTraceFloatsArray=None,

						_PredirateColorDict=None,

						**_KwargVariablesDict
					):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_predirate(self):


		#/#################/#
		# Build the leak matrix
		#

		#diag
		self.PrediratedLeakWeigthFloatsArray=(1./self.PrediratingConstantTimeFloat)*np.diag(
			np.ones(
				self.OldpredictingUnitsInt
				)
			)
		
		#add
		self.PrediratedLeakExactFastLateralWeigthFloatsArray=self.OldpredictedExactFastLateralWeigthFloatsArray-(
			1.-(self.OldpredictingCostFloat*self.PrediratingConstantTimeFloat)
		)*self.PrediratedLeakWeigthFloatsArray

		#debug
		self.debug(
			[
				('self.',self,[
						'PrediratedLeakExactFastLateralWeigthFloatsArray'	
					])
			]
		)

		#sum
		self.PrediratedTotalPerturbativeFastLateralWeigthFloatsArray=self.PrediratingSymmetryFloat*self.PrediratedLeakExactFastLateralWeigthFloatsArray+self.OldpredictedPerturbativeFastLateralWeigthFloatsArray

		#debug
		self.debug(
			[
				('self.',self,[
						'PrediratedTotalPerturbativeFastLateralWeigthFloatsArray'	
					])
			]
		)
		
		#pinv
		self.PrediratedControlDecoderWeigthFloatsArray=(1./self.PrediratingConstantTimeFloat
			)*np.linalg.pinv(
				self.OldpredictedExactDecoderWeigthFloatsArray.T
			)


		#/#################/#
		# Prepare the initial conditions
		#

		#random sensors
		PrediratedInitialRateFloatsArray=self.PrediratingInititalFloat*scipy.stats.uniform.rvs(
			size=self.OldpredictingUnitsInt
		)

		#/#################/#
		# Shape the size of all the unit traces
		#

		#init perturbative rates
		self.PrediratedPerturbativeUnitTraceFloatsArray=np.zeros(
				(self.OldpredictingUnitsInt,len(self.PredisensedTimeTraceFloatsArray))
			)
		self.PrediratedPerturbativeUnitTraceFloatsArray[:,0]=PrediratedInitialRateFloatsArray

		#init exact rates
		self.PrediratedExactUnitTraceFloatsArray=np.zeros(
				(self.OldpredictingUnitsInt,len(self.PredisensedTimeTraceFloatsArray))
			)
		self.PrediratedExactUnitTraceFloatsArray[:,0]=PrediratedInitialRateFloatsArray

		#init leak control rates
		self.PrediratedControlUnitTraceFloatsArray=np.zeros(
				(self.OldpredictingUnitsInt,len(self.PredisensedTimeTraceFloatsArray))
			)
		self.PrediratedControlUnitTraceFloatsArray[:,0]=PrediratedInitialRateFloatsArray

		#/#################/#
		# Shape the size of all the decoder traces
		#

		#init perturbative decoder
		self.PrediratedPerturbativeDecoderTraceFloatsArray=np.zeros(
				(self.OldpredictingSensorsInt,len(self.PredisensedTimeTraceFloatsArray))
			)
		self.PrediratedPerturbativeDecoderTraceFloatsArray[:,0]=np.dot(
				self.OldpredictedExactDecoderWeigthFloatsArray,
				PrediratedInitialRateFloatsArray
			)

		#init exact decoder
		self.PrediratedExactDecoderTraceFloatsArray=np.zeros(
				(self.OldpredictingSensorsInt,len(self.PredisensedTimeTraceFloatsArray))
			)
		self.PrediratedExactDecoderTraceFloatsArray[:,0]=np.dot(
				self.OldpredictedExactDecoderWeigthFloatsArray,
				PrediratedInitialRateFloatsArray
			)

		#init leak control decoder
		self.PrediratedControlDecoderTraceFloatsArray=np.zeros(
				(self.OldpredictingSensorsInt,len(self.PredisensedTimeTraceFloatsArray))
			)
		self.PrediratedControlDecoderTraceFloatsArray[:,0]=np.dot(
				self.PrediratedControlDecoderWeigthFloatsArray,
				PrediratedInitialRateFloatsArray
			)

		#/#################/#
		# integrativ Loop
		#

		#for loop
		for __IndexInt in xrange(1,len(self.PredisensedTimeTraceFloatsArray)):

			#/#################/#
			# Perturbative Rate
			#

			#Input Current
			PrediratedPerturbativeUnitCurrentFloatsArray=np.dot(
				self.OldpredictedTotalPerturbativeInputWeigthFloatsArray,
				self.PredisensedSensorTraceFloatsArray[:,__IndexInt-1]
			)

			#Check
			if self.PrediratingCommandNoiseFloat!=0.:
				PrediratedPerturbativeUnitCurrentFloatsArray+=self.PrediratingCommandNoiseFloat*scipy.stats.norm.rvs(
						size=self.OldpredictingUnitsInt
					)

			#Lateral Current
			PrediratedPerturbativeUnitCurrentFloatsArray-=np.dot(
				self.PrediratedTotalPerturbativeFastLateralWeigthFloatsArray,
				self.PrediratedPerturbativeUnitTraceFloatsArray[:,__IndexInt-1]
			)

			#transfer
			PrediratedPerturbativeUnitCurrentFloatsArray=self.PrediratingTransferVariable(
				PrediratedPerturbativeUnitCurrentFloatsArray
			)

			#Leak and Cost Current (non transfered)
			PrediratedPerturbativeUnitCurrentFloatsArray-=np.dot(
				self.PrediratedLeakWeigthFloatsArray,
				self.PrediratedPerturbativeUnitTraceFloatsArray[:,__IndexInt-1]
			)

			#/#################/#
			# Exact Rate 
			#

			#Input Current
			PrediratedExactUnitCurrentFloatsArray=np.dot(
				self.OldpredictedExactDecoderWeigthFloatsArray.T,
				self.PredisensedSensorTraceFloatsArray[:,__IndexInt-1]
			)

			#Check
			if self.PrediratingCommandNoiseFloat!=0.:
				PrediratedExactUnitCurrentFloatsArray+=self.PrediratingCommandNoiseFloat*scipy.stats.norm.rvs(
						size=self.OldpredictingUnitsInt
					)

			#Lateral Current
			PrediratedExactUnitCurrentFloatsArray-=np.dot(
				self.PrediratedLeakExactFastLateralWeigthFloatsArray,
				self.PrediratedExactUnitTraceFloatsArray[:,__IndexInt-1]
			)
			
			#transfer
			PrediratedExactUnitCurrentFloatsArray=self.PrediratingTransferVariable(
				PrediratedExactUnitCurrentFloatsArray
			)

			#Leak Current (non transfered)
			PrediratedExactUnitCurrentFloatsArray-=np.dot(
				self.PrediratedLeakWeigthFloatsArray,
				self.PrediratedExactUnitTraceFloatsArray[:,__IndexInt-1]
			)
			
			#debug
			'''
			self.debug(
					[
						'PrediratedExactUnitCurrentFloatsArray is ',
						str(PrediratedExactUnitCurrentFloatsArray)
					]
				)
			'''

			#/#################/#
			# Control Rate
			#

			#Input Current
			PrediratedControlUnitCurrentFloatsArray=np.dot(
				self.OldpredictedExactDecoderWeigthFloatsArray.T,
				self.PredisensedSensorTraceFloatsArray[:,__IndexInt-1]
			)

			#Check
			if self.PrediratingCommandNoiseFloat!=0.:
				PrediratedControlUnitCurrentFloatsArray+=self.PrediratingCommandNoiseFloat*scipy.stats.norm.rvs(
						size=self.OldpredictingUnitsInt
					)

			#transfer
			PrediratedControlUnitCurrentFloatsArray=self.PrediratingTransferVariable(
				PrediratedControlUnitCurrentFloatsArray
			)

			#Leal Current
			PrediratedControlUnitCurrentFloatsArray-=np.dot(
				self.PrediratedLeakWeigthFloatsArray,
				self.PrediratedControlUnitTraceFloatsArray[:,__IndexInt-1]
			)
			
			#/#################/#
			# Euler part
			#

			#set
			LocalDict=locals()

			#rate
			for __TagStr in [
								'Perturbative',
								'Exact',
								'Control'
							]:	

				#get
				PrediratedArray=getattr(
					self,
					'Predirated'+__TagStr+'UnitTraceFloatsArray'
				)

				PrediratedArray[:,__IndexInt]=PrediratedArray[:,__IndexInt-1]+LocalDict[
					'Predirated'+__TagStr+'UnitCurrentFloatsArray'
				]*self.PredisensingStepTimeFloat

				#set
				if self.PrediratingRateNoiseFloat!=0.:
					PrediratedArray[:,__IndexInt]+=self.PrediratingRateNoiseFloat*scipy.stats.norm.rvs(
						size=self.OldpredictingUnitsInt
					)

		
			#/#################/#
			# Post process part
			#

			"""
			#Saturate
			self.PrediratedPerturbativeUnitTraceFloatsArray[
				np.where(
					self.PrediratedPerturbativeUnitTraceFloatsArray[
							:,
							__IndexInt
						]>10.
				)
			]=10.
			self.PrediratedPerturbativeUnitTraceFloatsArray[
				np.where(
					self.PrediratedPerturbativeUnitTraceFloatsArray[
							:,
							__IndexInt
						]<-10.
				)
			]=-10.
			"""

			#/#################/#
			# Decoder part
			#

			#dot
			self.PrediratedPerturbativeDecoderTraceFloatsArray[
				:,
				__IndexInt
			]=np.dot(
					self.OldpredictedExactDecoderWeigthFloatsArray,
					self.PrediratedPerturbativeUnitTraceFloatsArray[:,__IndexInt-1]
				)

			#exact control
			self.PrediratedExactDecoderTraceFloatsArray[
				:,
				__IndexInt
			]=np.dot(
					self.OldpredictedExactDecoderWeigthFloatsArray,
					self.PrediratedExactUnitTraceFloatsArray[:,__IndexInt-1]
				)

			#leak control
			self.PrediratedControlDecoderTraceFloatsArray[
				:,
				__IndexInt
			]=np.dot(
					self.PrediratedControlDecoderWeigthFloatsArray,
					self.PrediratedControlUnitTraceFloatsArray[:,__IndexInt-1]
				)

	def mimic_view(self):

		#/#################/#
		# First call the base method
		#

		BaseClass.view(self)

		#/#################/#
		# Build the Units colors
		#

		self.PredirateControlColorTuplesList=SYS.getColorTuplesList(
			'black','green',len(self.PrediratingMonitorIntsList)+3,_PlotBool=False
		)[3:]
		self.PredirateExactColorTuplesList=SYS.getColorTuplesList(
			'black','blue',len(self.PrediratingMonitorIntsList)+3,_PlotBool=False
		)[3:]
		self.PrediratePerturbativeColorTuplesList=SYS.getColorTuplesList(
			'black','red',len(self.PrediratingMonitorIntsList)+3,_PlotBool=False
		)[3:]

		#debug
		'''
		self.debug(
				[
					'We have built the colors',
					('self.',self,['PrediratePerturbativeColorTuplesList'])
				]
			)
		'''

		#/#################/#
		# Build the input-unit traces axes
		#

		#debug
		self.debug(
				[
					('self.',self,['PredisensingMonitorIntsList'])
				]
			)

		#get
		self.set(
			'/-Charts/|Unit',
			{
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
												'>>self.PrediratedControlUnitTraceFloatsArray[\''+str(__IntsTuple[1])+'\']'
											],
											'#kwarg':{
												'label':'$r_{'+str(__IntsTuple[1])+'}^{control}$',
												'linestyle':'-',
												'linewidth':1,
												'color':self.PredirateControlColorTuplesList[__IntsTuple[0]]
											}
										}
									),
									('plot',
										{
											'#liarg:#map@get':[
												'PredisensedTimeTraceFloatsArray',
												'>>self.PrediratedExactUnitTraceFloatsArray[\''+str(__IntsTuple[1])+'\']'
											],
											'#kwarg':{
												'label':'$r_{'+str(__IntsTuple[1])+'}^{exact}$',
												'linestyle':'-',
												'linewidth':2,
												'color':self.PredirateExactColorTuplesList[__IntsTuple[0]],
											
											}
										}
									),
									('plot',
										{
											'#liarg:#map@get':[
												'PredisensedTimeTraceFloatsArray',
												'>>self.PrediratedPerturbativeUnitTraceFloatsArray[\''+str(__IntsTuple[1])+'\']'
											],
											'#kwarg':{
												'label':'$r_{'+str(__IntsTuple[1])+'}^{perturb}$',
												'linestyle':'-',
												'linewidth':4,
												'color':self.PrediratePerturbativeColorTuplesList[__IntsTuple[0]]
											
											}
										}
									)
								]
							}
						),
						enumerate(self.PrediratingMonitorIntsList)
					)	
				},
				'PyplotingChartVariable.extend':
				[[	
					('set_ylabel','$r(t)$'),
					('set_ylim',{
						'#liarg:#map@get':[
							">>SYS.set(SYS,'RateLimFloatsArray',"+"".join([
								"[max(-20.,self.PrediratedPerturbativeUnitTraceFloatsArray.min()),"
								"min(20.,self.PrediratedPerturbativeUnitTraceFloatsArray.max())]"
								])+').RateLimFloatsArray'
						]
					}),
					('set_yticks',{
						'#liarg:#map@get':[
							"".join(
								[
									">>SYS.set(SYS,'RateTickFloatsArray',"
									"map(lambda __Float:float('%.2f'%__Float),",
									"SYS.getTickFloatsArray(SYS.RateLimFloatsArray,3))",
									").RateTickFloatsArray"
								]
							)
						]
					}),
					('set_yticklabels',{
						'#liarg:#map@get':[
							">>map(lambda __Float:'$'+str(__Float)+'$',SYS.RateTickFloatsArray)"
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
									'ncol':len(self.PrediratingMonitorIntsList),
									'loc':2,
									'bbox_to_anchor':(1.05, 1)
								}
							})
				]]
			}
		)

		#/#################/#
		# Build the Decoder colors
		#

		self.PredirateDecoderControlColorTuplesList=SYS.getColorTuplesList(
			'black','green',len(self.PredisensingMonitorIntsList)+3,_PlotBool=False
		)[3:]
		self.PredirateDecoderExactColorTuplesList=SYS.getColorTuplesList(
			'black','blue',len(self.PredisensingMonitorIntsList)+3,_PlotBool=False
		)[3:]
		self.PredirateDecoderPerturbativeColorTuplesList=SYS.getColorTuplesList(
			'black','red',len(self.PredisensingMonitorIntsList)+3,_PlotBool=False
		)[3:]

		#debug
		'''
		self.debug(
				[
					'We have built the colors',
					('self.',self,['PrediratePerturbativeColorTuplesList'])
				]
			)
		'''
		#get
		self.set(
			'/-Charts/|Decoder',
			{
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
												'>>self.PredisensedSensorTraceFloatsArray[\''+str(__IntsTuple[1])+'\']'
											],
											'#kwarg':{
												'label':'$x_{'+str(__IntsTuple[1])+'}$',
												'linestyle':'-',
												'linewidth':1,
												'color':self.PredisenseSensorColorTuplesList[__IntsTuple[0]]
											}
										}
									),
									('plot',
										{
											'#liarg:#map@get':[
												'PredisensedTimeTraceFloatsArray',
												'>>self.PrediratedPerturbativeDecoderTraceFloatsArray[\''+str(__IntsTuple[1])+'\']'
											],
											'#kwarg':{
												'label':'$\hat{x}_{'+str(__IntsTuple[1])+'}^{perturb}$',
												'linestyle':'--',
												'linewidth':4,
												'color':self.PredirateDecoderPerturbativeColorTuplesList[__IntsTuple[0]],
											
											}
										}
									),
									('plot',
										{
											'#liarg:#map@get':[
												'PredisensedTimeTraceFloatsArray',
												'>>self.PrediratedExactDecoderTraceFloatsArray[\''+str(__IntsTuple[1])+'\']'
											],
											'#kwarg':{
												'label':'$\hat{x}_{'+str(__IntsTuple[1])+'}^{exact}$',
												'linestyle':'--',
												'linewidth':2,
												'color':self.PredirateDecoderExactColorTuplesList[__IntsTuple[0]],
											
											}
										}
									),
									('plot',
										{
											'#liarg:#map@get':[
												'PredisensedTimeTraceFloatsArray',
												'>>self.PrediratedControlDecoderTraceFloatsArray[\''+str(__IntsTuple[1])+'\']'
											],
											'#kwarg':{
												'label':'$\hat{x}_{'+str(__IntsTuple[1])+'}^{control}$',
												'linestyle':'--',
												'linewidth':1,
												'color':self.PredirateDecoderControlColorTuplesList[__IntsTuple[0]],
											
											}
										}
									)
									
								]
							}
						),
						enumerate(self.PredisensingMonitorIntsList)
					)	
				},
				'PyplotingChartVariable.extend':
				[[
					('set_ylabel','$x(t),\ \hat{x}(t)$'),
					('set_ylim',{
						'#liarg:#map@get':[
							">>SYS.SensorLimFloatsArray"
						]
					}),
					('set_yticks',{
						'#liarg:#map@get':[
							">>SYS.SensorTickFloatsArray"
						]
					}),
					('set_yticklabels',{
						'#liarg:#map@get':[
							">>SYS.SensorTickStrsArray"]
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
									'ncol':len(self.PredisensingMonitorIntsList),
									'loc':2,
									'bbox_to_anchor':(1.05, 1)
								}
							})
				]]
			}
		)	
#</DefineClass>

#</DefinePrint>
PrediraterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PrediratingConstantTimeFloat',
		'PrediratingTransferVariable',
		'PrediratingMonitorIntsList',
		'PrediratingInititalFloat',
		'PrediratingSymmetryFloat',
			
		'PrediratedLeakWeigthFloatsArray',		
		'PrediratedLeakExactFastLateralWeigthFloatsArray',
		'PrediratedTotalPerturbativeFastLateralWeigthFloatsArray',
		'PrediratedInitialRateFloatsArray',
		'PrediratedControlDecoderWeigthFloatsArray',

		'PredisensedSensorTraceFloatsArray',
		'PrediratedPerturbativeUnitTraceFloatsArray',
		'PrediratedExactUnitTraceFloatsArray',
		'PrediratedControlUnitTraceFloatsArray',
		
		'PrediratedPerturbativeDecoderTraceFloatsArray',
		'PrediratedExactDecoderTraceFloatsArray',
		'PrediratedControlDecoderTraceFloatsArray',

		'PredirateControlColorTuplesList',
		'PredirateExactColorTuplesList',
		'PrediratePerturbativeColorTuplesList',
		'PredirateDecoderControlColorTuplesList',
		'PredirateDecoderExactColorTuplesList',
		'PredirateDecoderPerturbativeColorTuplesList'
	]
)
#<DefinePrint>

