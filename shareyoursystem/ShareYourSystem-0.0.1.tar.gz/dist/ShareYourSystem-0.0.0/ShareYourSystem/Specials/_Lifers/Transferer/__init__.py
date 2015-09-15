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
BaseModuleStr="ShareYourSystem.Specials.Lifers.Stabilizer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Transferer','Transfer','Transfering','Transfered')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Recorders import Leaker
import scipy.stats
import numpy as np
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class TransfererClass(BaseClass):
	
	def default_init(self,
			_TransferingCurrentVariable = None,
			_TransferingScanFrequencyVariable = None,
			_TransferingSampleInt = 100,
			_TransferingColorStrsList = None,
			_TransferingLabelStrsList = None,
			_TransferedCurrentFloatsArray = None,
			_TransferedScanFrequencyFloatsArray = None,
			_TransferedRateComplexesArray = None,
			_TransferedRateAmplitudeFloatsArray = None,
			_TransferedRatePhaseFloatsArray = None,
			_TransferedNormRateAmplitudeFloatsArray = None,
			_TransferedNormRatePhaseFloatsArray = None,
			_TransferedParentSingularStr = "",
			_TransferedNetworkDeriveTransfererVariable=None,
			**_KwargVariablesDict
		):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_transfer(self):

		#/#################/#
		# Determine if it is an inside structure or the top
		#

		#debug
		'''
		self.debug(
			[
				'We leak here',
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
			self.TransferedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,['TransferedParentSingularStr'])
			]
		)
		'''

		#Check
		if (self.ParentDeriveTeamerVariable==None or "Populations" in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Traces',
			'Samples',
			'Events',
			'Interactomes',
			"Interactions",
			'Inputs'
		]) and self.TransferedParentSingularStr!='Population':

			#/########################/#
			# Network level
			# 

			#debug
			'''
			self.debug(
				[
					'It is a Network level for the transfer',
				]
			)
			'''

			#/########################/#
			# Determine parent level
			# 

			#alias
			self.TransferedNetworkDeriveTransfererVariable=self

			#/########################/#
			# transferNetwork
			# 

			#transfer
			self.transferNetwork()

			#/########################/#
			# structure transfer 
			# 

			#debug
			'''
			self.debug(
				[
					'We structure all the transfering children...'
				]
			)	
			'''

			#structure
			self.structure(
				[
					"Populations",
					'Inputs',
					'Interactomes',
					"Interactions",
				],
				'#all',
				_ManagerCommandSetList=[
						'transfer'
					]
			)
			
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
						'TransferedParentSingularStr'
					])
				]
			)
			'''

			#set
			TransferedMethodKeyStr='transfer'+self.TransferedParentSingularStr

			#Check
			if hasattr(self,TransferedMethodKeyStr):

				#/########################/#
				# call the special transfer<TransferedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.TransferedParentSingularStr+' level',
						'We transfer<TransferedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					TransferedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted transfer'+self.TransferedParentSingularStr
					]
				)
				'''	
	
	def transferNetwork(self):

		#debug
		'''
		self.debug(
			[
				"We compute transfer here",
				('self.',self,[
						'TransferingCurrentVariable'
					])
			]
		)
		'''

		#type
		TransferedCurrentType=type(
			self.TransferingCurrentVariable
		)

		#Check
		if TransferedCurrentType==None.__class__:

			#array
			self.TransferedCurrentFloatsArray=[1.]*self.StationarizingUnitsInt

		elif TransferedCurrentType in [np.float64,float]:

			#array
			self.TransferedCurrentFloatsArray=[
					self.TransferingCurrentVariable
				]*self.StationarizingUnitsInt

		else:

			#array
			self.TransferedCurrentFloatsArray=self.TransferingCurrentVariable

		#array
		self.TransferedCurrentFloatsArray=np.array(
			self.TransferedCurrentFloatsArray
		)

		#import 
		import scipy.linalg

		#debug
		"""
		self.debug(
			[
				"we do a transfer scan analysis",
				('self.',self,['TransferingScanFrequencyVariable'])
			]
		)
		"""

		#type
		TransferedScanType=type(self.TransferingScanFrequencyVariable)

		#Check
		if TransferedScanType==None.__class__:



			#Check
			self.TransferedScanFrequencyFloatsArray=np.logspace(
				0,
				3,
				self.TransferingSampleInt
			)

		elif TransferedScanType in [np.float64,float]:

			#Check
			self.TransferedScanFrequencyFloatsArray=np.array(
				[self.TransferingScanFrequencyVariable]
			)

		else:

			#Check
			self.TransferedScanFrequencyFloatsArray=np.array(
				self.TransferingScanFrequencyVariable
			)

		#debug
		"""
		self.debug(
			[
				('self.',self,['TransferedScanFrequencyFloatsArray'])
			]
		)
		"""

		#init
		self.TransferedRateComplexesArray=np.zeros(
				(
					self.StationarizingUnitsInt,
					len(self.TransferedScanFrequencyFloatsArray)
				),
				dtype=complex
			)
		self.TransferedRateAmplitudeFloatsArray=np.zeros(
				(
					self.StationarizingUnitsInt,
					len(self.TransferedScanFrequencyFloatsArray)
				),
				dtype=float
			)
		self.TransferedRatePhaseFloatsArray=np.zeros(
				(
					self.StationarizingUnitsInt,
					len(self.TransferedScanFrequencyFloatsArray)
				),
				dtype=float
			)

		#get
		self.StabilizedNeuralPerturbationMethodVariable=getattr(
			self,
			'get'+self.StationarizingInteractionStr+'NeuralPerturbationVariable'
		)

		#map
		map(
			lambda __IndexInt,__ScanFrequencyFloat:
			self.setTransfer(__IndexInt,__ScanFrequencyFloat),
			xrange(len(self.TransferedScanFrequencyFloatsArray)),
			self.TransferedScanFrequencyFloatsArray
		)

		#debug
		'''
		self.debug(
			[
				'after the solve decomposition',
				('self.',self,[
					'TransferedScanFrequencyFloatsArray',
					'TransferedCurrentFloatsArray',
					'TransferedRateComplexesArray',
					#'TransferedRateAmplitudeFloatsArray',
					#'TransferedRatePhaseFloatsArray'
				])	
			]
		)
		'''

		#find the Extremum
		self.NumscipiedFourierFrequencyFloatsArray = self.TransferedScanFrequencyFloatsArray
		self.NumscipiedFourierAmplitudeFloatsArray = self.TransferedRateAmplitudeFloatsArray
		self.NumscipiedFourierPhaseFloatsArray = self.TransferedRatePhaseFloatsArray
		self.setCrossPhase()
		self.setExtremum()

		#debug
		self.debug(
			[
				('self.',self,[ 
						'NumscipiedFourierMaxTupleFloatsArray',
						'NumscipiedFourierMaxCrossPhaseFloatsArray'
					])
			]
		)

	def setTransfer(self,__IndexInt,__ScanFrequencyFloat):

		#debug
		'''
		self.debug(
			[
				"We set transfer here",
				'__ScanFrequencyFloat is '+str(__ScanFrequencyFloat)
			]
		)
		'''

		#set
		self.StabilizedPerturbationComplex=1j*2.*np.pi*__ScanFrequencyFloat

		#debug
		'''
		self.debug(
			[
				"We set transfer here",
				('self.',self,['StabilizedPerturbationComplex'])
			]
		)
		'''

		#set
		self.setStabilizedTotalPerturbationComplexesArray()

		#debug
		'''
		self.debug(
			[
				"We have setted the StabilizedTotalPerturbationComplexesArray",
				('self.',self,[
					'StabilizedTotalPerturbationComplexesArray',
					'StabilizedNeuralPerturbationMethodVariable'
				])
			]
		)
		'''

		#Set
		TransferedNeuralCurrentFloatsArray=self.StabilizedNeuralPerturbationComplexesArray*self.TransferedCurrentFloatsArray

		#solve
		TransferedRateComplexesArray = scipy.linalg.solve(
			self.StabilizedTotalPerturbationComplexesArray,
			TransferedNeuralCurrentFloatsArray
		)

		#lu
		self.TransferedRateComplexesArray[
			:,
			__IndexInt
		]=TransferedRateComplexesArray

		#amp and phase
		self.TransferedRateAmplitudeFloatsArray[
			:,
			__IndexInt
		]=np.abs(
			TransferedRateComplexesArray
		)
		self.TransferedRatePhaseFloatsArray[
			:,
			__IndexInt
		]=np.angle(
			TransferedRateComplexesArray
		)

		#debug
		'''
		self.debug(
			[
				"In the end",
				('self.',self,[])
			]
		)
		'''

		#set
		self.TransferedNormRateAmplitudeFloatsArray = np.copy(self.TransferedRateAmplitudeFloatsArray)
		for IndexInt in xrange(len(self.TeamDict['Populations'].ManagementDict)):
			self.TransferedNormRateAmplitudeFloatsArray[IndexInt,:]/=self.StationarizingRateVariable[IndexInt]

		#set
		self.TransferedNormRatePhaseFloatsArray = np.copy(self.TransferedRatePhaseFloatsArray)
		for IndexInt in xrange(len(self.TeamDict['Populations'].ManagementDict)):
			self.TransferedNormRatePhaseFloatsArray[IndexInt,:]*=(180./np.pi)


	#/######################/#
	# Augment view
	#
	
	def viewNetwork(self):

		#
		# Maybe erase
		#

		del self.TeamDict['Panels']


		#
		# Plot the transfer functions
		#

		#Check 
		if len(self.TransferingColorStrsList)!=self.StationarizingUnitsInt:

			#set
			self.TransferingColorStrsList = SYS.getColorTuplesList(
					_FromColorStr='blue',
					_ToColorStr='black',
					_SampleInt=self.StationarizingUnitsInt,
					_PlotBool=False
				)

		#Check
		if len(self.TransferingLabelStrsList)!=self.StationarizingUnitsInt:

			#set
			self.TransferingLabelStrsList=map(
				lambda _Variable:
				_Variable.ManagementTagStr,
				self.TeamDict['Populations'].ManagementDict.values()
			)

		#Debug
		self.debug(
			[
				('self.',self,[
						'TransferingColorStrsList',
						'TransferingLabelStrsList'
					])
			]
		)

		#debug
		'''
		self.debug(
			[
				"We transfer view network here"
			]
		)
		'''

		#call
		ViewedTransferVariable = self.getTeamer(
				'Panels'
			).getManager(
				'Transfer'
			)

		ViewedChartsVariable=ViewedTransferVariable.getTeamer(
				'Charts'
			)

		#xlim
		xlimList =  [self.TransferedScanFrequencyFloatsArray[0],self.TransferedScanFrequencyFloatsArray[-1]]

		#
		# Amplitude
		#

		#plot
		ViewedAmplitudeChartVariable = ViewedChartsVariable.getManager('Amplitude')

		#get
		ViewedAmplitudeDrawVariable = ViewedAmplitudeChartVariable.getTeamer(
				'Draws'
			).getManager('0')


		#debug
		self.debug(
			[
				('self.',self,[
						'StationarizedRateFloatsArraysList',
						'StationarizingRateVariable'
					])
			]
		)

		#set
		yLimAmplitudeList=[
			self.TransferedNormRateAmplitudeFloatsArray.min(),
			self.TransferedNormRateAmplitudeFloatsArray.max()
		]
		yTickAmplitudeList=[0.,0.5,1.]

		#map
		ViewedAmplitudeDrawVariable.PyplotingDrawVariable = map(
			lambda __IndexInt:
			('plot',{
					'#liarg':[
						self.TransferedScanFrequencyFloatsArray,
						self.TransferedNormRateAmplitudeFloatsArray[__IndexInt,:]
					],
					'#kwarg':{
							'linestyle':'-',
							'linewidth':5,
							'color':self.TransferingColorStrsList[__IndexInt],
							'label':self.TransferingLabelStrsList[__IndexInt]
						}
				}),
			xrange(len(self.TeamDict['Populations'].ManagementDict))
		)

		#set log
		ViewedAmplitudeChartVariable.PyplotingChartVariable=[
				('set_xscale','log'),
				('set_xlim',xlimList),
				('set_xticklabels',[]),
				('set_yticks',yTickAmplitudeList),
				('set_yticklabels',map(lambda __Float:'$'+str(__Float)+'$',yTickAmplitudeList)),
				('set_ylabel',"$amplitude\ r_{a1}/r_{a0}$")
			]

		ViewedAmplitudeChartVariable.PyplotingLegendDict={
			'fontsize':10,
			'ncol':2 if self.StationarizingUnitsInt>3 else 1
		}

		#
		# Phase
		#

		#plot
		ViewedPhaseChartVariable = ViewedChartsVariable.getManager('Phase')

		#get
		ViewedPhaseDrawVariable = ViewedPhaseChartVariable.getTeamer(
				'Draws'
			).getManager('0')

		#set
		#yLimPhaseList=[TransferedNormRatePhaseFloatsArray.min(),TransferedNormRatePhaseFloatsArray.max()]
		yLimPhaseList=[-180.,180.]
		yTickPhaseList=[-180,-90,0,90,180]

		#map
		ViewedPhaseDrawVariable.PyplotingDrawVariable = map(
			lambda __IndexInt:
			('plot',{
					'#liarg':[
						self.TransferedScanFrequencyFloatsArray,
						#(180./np.pi)*np.array(map(
						#	SYS.getArgumentVariable,
						#	self.TransferedRateComplexesArray[__IndexInt,:]
						#))
						self.TransferedNormRatePhaseFloatsArray[__IndexInt,:]
					],
					'#kwarg':{
							'linestyle':'-',
							'linewidth':5,
							'color':self.TransferingColorStrsList[__IndexInt]
						}
				}),
			range(len(self.TeamDict['Populations'].ManagementDict))[1:]
		)+[
			('plot',{
					'#liarg':[
						self.TransferedScanFrequencyFloatsArray,
						#(180./np.pi)*np.array(map(
						#	SYS.getArgumentVariable,
						#	self.TransferedRateComplexesArray[__IndexInt,:]
						#))
						self.TransferedNormRatePhaseFloatsArray[0,:]
					],
					'#kwarg':{
							'linestyle':'--',
							'linewidth':3,
							'color':self.TransferingColorStrsList[0]
						}
				})
		]

		#set log
		ViewedPhaseChartVariable.PyplotingChartVariable=[
				('plot',{
					'#liarg':[	
							xlimList,
							[0.,0.]
						],
					'#kwarg':{
							'linestyle':'--',
							'linewidth':1,
							'color':"black"
						}
					}

				),
				('set_xscale','log'),
				('set_xlim',xlimList),
				('set_xlabel',"$frequency (Hz)$"),
				('set_ylim',yLimPhaseList),
				('set_ylabel',"$phase$"),
				('set_yticks',yTickPhaseList),
				('set_yticklabels',map(lambda __Float:'$'+str(__Float)+'$',yTickPhaseList))
			]

		#
		# Plot max but just (for the first)
		#

		#map
		ViewedAmplitudeDrawVariable.PyplotingDrawVariable += SYS.sum(map(
			lambda __IndexInt:
			map(
				lambda __FourierMaxTuple:
				('plot',{
					'#liarg':[
						[__FourierMaxTuple[0]]*2,
						yLimAmplitudeList
					],
					'#kwarg':{
							'linestyle':'--',
							'linewidth':1,
							#'color':self.TransferingColorStrsList[__IndexInt]
							'color':"black"
						}
				}),
				self.NumscipiedFourierMaxTupleFloatsArray[__IndexInt]
			),
			range(len(self.TeamDict['Populations'].ManagementDict))[:1]
		))

		#map
		'''
		ViewedPhaseDrawVariable.PyplotingDrawVariable += SYS.sum(map(
			lambda __IndexInt:
			map(
				lambda __FourierMaxTuple:
				('plot',{
					'#liarg':[
						[__FourierMaxTuple[0]]*2,
						yLimPhaseList
					],
					'#kwarg':{
							'linestyle':'--',
							'linewidth':1,
							#'color':self.TransferingColorStrsList[__IndexInt]
							'color':"black"
						}
				}),
				self.NumscipiedFourierMaxTupleFloatsArray[__IndexInt]
			),
			range(len(self.TeamDict['Populations'].ManagementDict))[:1]
		))	
		'''

		#map
		ViewedPhaseDrawVariable.PyplotingDrawVariable += SYS.sum(map(
			lambda __IndexInt:
			SYS.sum(map(
				lambda __FourierMaxTuple:
				map(
					lambda __PhaseFloat,_IndInt:
					('plot',{
						'#liarg':[
							__FourierMaxTuple[0],
							__PhaseFloat
						],
						'#kwarg':{
								'linestyle':'',
								'marker':"o",
								'markersize':5,
								'color':self.TransferingColorStrsList[_IndInt]
								#'color':"black"
							}
					}),
					__FourierMaxTuple[1][1:],
					xrange(len(__FourierMaxTuple[1][1:]))
				),
				self.NumscipiedFourierMaxCrossPhaseFloatsArray[__IndexInt]
			)),
			range(len(self.TeamDict['Populations'].ManagementDict))[:1]
		))	

		#
		# Recapepete
		#

		#mapSet
		self.mapSet(
			{
				'PyplotingFigureVariable':{
					'figsize':(10,10)
				},
				'PyplotingGridVariable':(40,30),
				'-Panels':[
					(
						'|Transfer',
						{
							'PyplotingTextVariable':[-0.6,0.],
							'PyplotingShapeVariable':[10,10],
							'-Charts':{
								'|Amplitude':{
								},
								'|Phase':{
									'PyplotingShiftVariable':[2,0]
								}
							}
						}
					)
				]
			}
		)




		#base
		BaseClass.viewNetwork(self)

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Print things if they are computed
			#

			#Check
			if self.TransferedNetworkDeriveTransfererVariable==self:

				#map
				map(
						lambda __KeyStr:
						self.forcePrint(
							[__KeyStr],
							'TransfererClass'
						)
						if getattr(
							self.PrintingCopyVariable,
							__KeyStr
						) not in [None,0.,""]
						else None,
						[
						]
					)

		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

#</DefineClass>

#</DefineLocals>
Leaker.LeakersStructurerClass.ManagingValueClass=TransfererClass
#<DefineLocals>

#</DefinePrint>
TransfererClass.PrintingClassSkipKeyStrsList.extend(
	[
		'TransferingCurrentVariable',
		'TransferingScanFrequencyVariable',
		'TransferingSampleInt',
		'TransferingColorStrsList',
		'TransferingLabelStrsList',
		'TransferedCurrentFloatsArray',
		'TransferedScanFrequencyFloatsArray',
		'TransferedRateComplexesArray',
		'TransferedRateAmplitudeFloatsArray',
		'TransferedRatePhaseFloatsArray',
		'TransferedNormRateAmplitudeFloatsArray',
		'TransferedNormRatePhaseFloatsArray',
		'TransferedParentSingularStr',
		'TransferedNetworkDeriveTransfererVariable'
	]
)
#<DefinePrint>