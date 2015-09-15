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
BaseModuleStr="ShareYourSystem.Standards.Viewers.Pyploter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Oldpredicter','Oldpredict','Oldpredicting','Oldpredicted')
#</DefineAugmentation>

#<ImportSpecificModules>
import scipy.stats
import numpy as np
from matplotlib import pyplot
#</ImportSpecificModules>

#<DefineLocals>
def getNullFloatsArray(_FloatsArray, _RtolFloat=1e-5):
	u, s, v = np.linalg.svd(_FloatsArray)
	RankInt = (s > _RtolFloat*s[0]).sum()
	return v[RankInt:].T.copy()
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class OldpredicterClass(BaseClass):
	
	def default_init(self,

						_OldpredictingUnitsInt=0,
						_OldpredictingSensorsInt=0,

						_OldpredictingDynamicStr="leak",
						_OldpredictingConstantTimeFloat=1.,
						_OldpredictingInputStatStr='norm',
						_OldpredictingDecoderMeanWeigtFloat=0.,
						_OldpredictingDecoderStdWeigtFloat=1.,
						_OldpredictingNormalisationInt=1,			

						_OldpredictingCostFloat=1.,
						_OldpredictingPerturbativeInputWeightFloat=0.1,
						_OldpredictingPerturbativeLateralWeightFloat=0.1,
						_OldpredictingInputRandomStatStr='norm',
						_OldpredictingLateralRandomStatStr='norm',
						_OldpredictingPerturbativeNullBool=True,

						_OldpredictedSensorJacobianFloatsArray=None,
						
						_OldpredictedControlDecoderWeigthFloatsArray=None,
						_OldpredictedExactDecoderWeigthFloatsArray=None,

						_OldpredictedLeakWeigthFloatsArray=None,

						_OldpredictedInputRandomFloatsArray=None,
						_OldpredictedPerturbativeInputWeigthFloatsArray=None,
						_OldpredictedNullFloatsArray=None,
						_OldpredictedTotalPerturbativeInputWeigthFloatsArray=None,

						_OldpredictedExactFastLateralWeigthFloatsArray=None,
						_OldpredictedLateralRandomFloatsArray=None,
						_OldpredictedPerturbativeFastLateralWeigthFloatsArray=None,
						_OldpredictedTotalPerturbativeFastLateralWeigthFloatsArray=None,
					
						**_KwargVariablesDict
					):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_oldpredict(self):

		#/#################/#
		# Sensor care : Prepare the input weigth and the null matrix
		#

		if self.OldpredictingDynamicStr=="leak":

			self.OldpredictedSensorJacobianFloatsArray=-np.diag(
				(1./self.OldpredictingConstantTimeFloat)*np.ones(
					self.OldpredictingSensorsInt
				)
			)

		elif self.OldpredictingDynamicStr in ["Gamma","Gamma-Theta"]:

			if self.OldpredictingDynamicStr=="Gamma" and self.OldpredictingSensorsInt<3:
				self.OldpredictingSensorsInt=2
			if self.OldpredictingDynamicStr=="Gamma-Theta" and self.OldpredictingSensorsInt<6:
				self.OldpredictingSensorsInt=6

			self.OldpredictedSensorJacobianFloatsArray=-np.diag(
				(1./self.OldpredictingConstantTimeFloat)*np.ones(
					self.OldpredictingSensorsInt
				)
			)

			#set
			self.OldpredictedSensorJacobianFloatsArray[0,0]+=(1.5/self.OldpredictingConstantTimeFloat)
			self.OldpredictedSensorJacobianFloatsArray[1,0]+=-(3.7/self.OldpredictingConstantTimeFloat)
			self.OldpredictedSensorJacobianFloatsArray[0,1]+=(3.7/self.OldpredictingConstantTimeFloat)
			self.OldpredictedSensorJacobianFloatsArray[1,1]+=-(1./self.OldpredictingConstantTimeFloat)

			if self.OldpredictingDynamicStr=="Gamma-Theta":

				#set
				self.OldpredictedSensorJacobianFloatsArray[2,3]+=(1./self.OldpredictingConstantTimeFloat)
				self.OldpredictedSensorJacobianFloatsArray[3,4]+=-(1.2/self.OldpredictingConstantTimeFloat)
				self.OldpredictedSensorJacobianFloatsArray[4,5]+=-(1.4/self.OldpredictingConstantTimeFloat)
				self.OldpredictedSensorJacobianFloatsArray[5,2]+=-(1.6/self.OldpredictingConstantTimeFloat)

		#debug
		'''
		self.debug(
			[
				'We have prepared the sensor jacobian',
				('self.',self,['OldpredictedSensorJacobianFloatsArray'])
			]
		)
		'''

		#/#################/#
		# Prepare the Decoders weigths
		#

		#Perturbative and exact 

		#random
		self.OldpredictedExactDecoderWeigthFloatsArray=(
			self.OldpredictingDecoderMeanWeigtFloat+self.OldpredictingDecoderStdWeigtFloat*getattr(
				scipy.stats,
				self.OldpredictingInputStatStr
			).rvs(
				size=(
					self.OldpredictingSensorsInt,
					self.OldpredictingUnitsInt
				)
			)
		)/(self.OldpredictingUnitsInt**self.OldpredictingNormalisationInt)
		
		#debug
		'''
		self.debug(
			[
				'We have setted the OldpredictedExactDecoderWeigthFloatsArray',
				('self.',self,[
					'OldpredictedExactDecoderWeigthFloatsArray',
					'OldpredictingDecoderMeanWeigtFloat',
					'OldpredictingDecoderStdWeigtFloat'
				])
			]
		)
		'''

		#find the null space
		self.OldpredictedNullFloatsArray=getNullFloatsArray(
			self.OldpredictedExactDecoderWeigthFloatsArray
		)

		#debug
		'''
		OldpredictedProductArray=np.dot(
			self.OldpredictedExactDecoderWeigthFloatsArray,
			self.OldpredictedNullFloatsArray
		)
		self.debug(
				[
					('self.',self,[
						'OldpredictedExactDecoderWeigthFloatsArray',
						'OldpredictingUnitsInt'
						]
					),
					("locals()['",locals(),['OldpredictedProductArray'],"']")
				]
			)
		'''

		#debug
		'''
		OldpredictedPinvFloatsArray=np.dot(
			self.OldpredictedControlDecoderWeigthFloatsArray,
			self.OldpredictedExactDecoderWeigthFloatsArray.T
		)
		self.debug(
			[
				'OldpredictedPinvFloatsArray is ',
				str(OldpredictedPinvFloatsArray)
			]
		)
		'''

		#/#################/#
		# Build the perturbative input random matrices
		#

		#dot
		if self.OldpredictingPerturbativeNullBool:

			#random
			self.OldpredictedInputRandomFloatsArray=self.OldpredictingPerturbativeInputWeightFloat*getattr(
				scipy.stats,
				self.OldpredictingInputRandomStatStr
			).rvs(
				size=(
					np.shape(self.OldpredictedNullFloatsArray)[1],
					self.OldpredictingSensorsInt
				)
			)

			#dot
			self.OldpredictedPerturbativeInputWeigthFloatsArray=np.dot(
				self.OldpredictedNullFloatsArray,
				self.OldpredictedInputRandomFloatsArray
			)

			#debug
			'''
			self.debug(
				[
					'We have done the null dot',
					('self.',self,[
							'OldpredictedPerturbativeInputWeigthFloatsArray'
						])
				]
			)
			'''

		else:

			#get
			self.OldpredictedPerturbativeInputWeigthFloatsArray=self.OldpredictingPerturbativeInputWeightFloat*getattr(
				scipy.stats,
				self.OldpredictingInputRandomStatStr
			).rvs(
				size=(
					self.OldpredictingUnitsInt,
					self.OldpredictingSensorsInt
				)
			)

			#debug
			'''
			self.debug(
				[
					'We just build a random input matrix',
					('self.',self,[
							'OldpredictedPerturbativeInputWeigthFloatsArray'
						])
				]
			)
			'''


			
		#normalize
		self.OldpredictedPerturbativeInputWeigthFloatsArray/=(self.OldpredictingUnitsInt**self.OldpredictingNormalisationInt)

		#/#################/#
		# Build all the perturbative input
		#

		#sum
		self.OldpredictedTotalPerturbativeInputWeigthFloatsArray=self.OldpredictedExactDecoderWeigthFloatsArray.T+self.OldpredictedPerturbativeInputWeigthFloatsArray


		#/#################/#
		# Build all the possible lateral connectivities
		#

		#Exact

		#dot
		self.OldpredictedExactFastLateralWeigthFloatsArray=np.dot(
				self.OldpredictedExactDecoderWeigthFloatsArray.T,
				self.OldpredictedExactDecoderWeigthFloatsArray
			)

		#debug
		'''
		self.debug(
				[
					('self.',self,[
						'OldpredictedExactFastLateralWeigthFloatsArray',
					])
				]
			)
		'''

		#Perturbative

		#Check
		if self.OldpredictingPerturbativeNullBool:

			#random
			self.OldpredictedLateralRandomFloatsArray=self.OldpredictingPerturbativeLateralWeightFloat*getattr(
				scipy.stats,
				self.OldpredictingLateralRandomStatStr
			).rvs(
				size=(
					np.shape(self.OldpredictedNullFloatsArray)[1],
					self.OldpredictingUnitsInt
				)
			)

			#dot
			self.OldpredictedPerturbativeFastLateralWeigthFloatsArray=np.dot(
					self.OldpredictedNullFloatsArray,
					self.OldpredictedLateralRandomFloatsArray
				)

			#debug
			self.debug(
				[
					'We have done the null dot',
					('self.',self,[
						'OldpredictedPerturbativeFastLateralWeigthFloatsArray'
					])
				]
			)

		else:

			#copy
			self.OldpredictedPerturbativeFastLateralWeigthFloatsArray=self.OldpredictingPerturbativeLateralWeightFloat*getattr(
				scipy.stats,
				self.OldpredictingLateralRandomStatStr
			).rvs(
				size=(
					self.OldpredictingUnitsInt,
					self.OldpredictingUnitsInt
				)
			)

			#debug
			self.debug(
				[
					'We just build a random lateral matrix',
					('self.',self,[
						'OldpredictedPerturbativeFastLateralWeigthFloatsArray'
					])
				]
			)

		#normalize
		self.OldpredictedPerturbativeFastLateralWeigthFloatsArray/=(
			self.OldpredictingUnitsInt**(self.OldpredictingNormalisationInt/2.)
		)

		

#</DefineClass>

#</DefinePrint>
OldpredicterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'OldpredictingUnitsInt',
		'OldpredictingSensorsInt',
		
		'OldpredictingDynamicStr',
		'OldpredictingConstantTimeFloat',
		'OldpredictingInputStatStr',
		'OldpredictingDecoderMeanWeigtFloat',
		'OldpredictingDecoderStdWeigtFloat',
		'OldpredictingNormalisationInt',

		'OldpredictingCostFloat',
		'OldpredictingPerturbativeInputWeightFloat',
		'OldpredictingPerturbativeLateralWeightFloat',
		'OldpredictingInputRandomStatStr',
		'OldpredictingLateralRandomStatStr',
		'OldpredictingPerturbativeNullBool',

		'OldpredictedSensorJacobianFloatsArray',
		
		'OldpredictedLeakWeigthFloatsArray',

		'OldpredictedControlDecoderWeigthFloatsArray',
		'OldpredictedExactDecoderWeigthFloatsArray',

		'OldpredictedInputRandomFloatsArray',
		'OldpredictedPerturbativeInputWeigthFloatsArray',
		'OldpredictedNullFloatsArray',
		'OldpredictedTotalPerturbativeInputWeigthFloatsArray',
		
		'OldpredictedExactFastLateralWeigthFloatsArray',
		'OldpredictedLateralRandomFloatsArray',
		'OldpredictedPerturbativeFastLateralWeigthFloatsArray',
		'OldpredictedTotalPerturbativeFastLateralWeigthFloatsArray',
	]
)
#<DefinePrint>