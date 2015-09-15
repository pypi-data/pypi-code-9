

#ImportModules
import ShareYourSystem as SYS

#Define
MyPredirater=SYS.PrediraterClass(
	).oldpredict(
		#PredictingUnitsInt
		100,
		#PredictingSensorsInt
		1,
		#PredictingDynamicStr
		'leak',
		#PredictingConstantTimeFloat (ms)
		1.,
		#PredictingInputStatStr
		'norm',
		#PredictingDecoderMeanWeightFloat
		0.,
		#PredictingDecoderStdWeightFloat
		45.,
		#PredictingNormalisationInt
		1.,			
		#PredictingCostFloat
		0.,
		#PredictingPerturbativeInputWeightFloat
		0.,
		#PredictingPerturbativeLateralWeightFloat
		5.,
		#PredictingInputRandomStatStr
		'norm',
		#PredictingLateralRandomStatStr
		'norm',
		#PredictingPerturbativeNullBool
		True
	).predisense(
		#PredisensingRunTimeFloat (ms)
		100.,
		#PredisensingStepTimeFloat (ms)
		0.05,
		#PredisensingMonitorList
		[0],
		#PredisensingKrenelClampFloat
		0.05,
		#PredisensingFourierClampFloat
		0.1,
	).predirate(
		#PrediratingConstantTimeFloat
		1.,
		#PrediratingTransferVariable
		#lambda _FloatsArray:SYS.numpy.tanh(_FloatsArray),
		#lambda _FloatsArray:0.5*SYS.numpy.tanh(2.*_FloatsArray),
		#lambda _FloatsArray:0.2*SYS.numpy.tanh(5.*_FloatsArray),
		#lambda _FloatsArray:0.1*SYS.numpy.tanh(10.*_FloatsArray),
		#lambda _FloatsArray:0.05*SYS.numpy.tanh(20.*_FloatsArray),
		#lambda _FloatsArray:0.02*SYS.numpy.tanh(50.*_FloatsArray),
		#lambda _FloatsArray:0.01*SYS.numpy.tanh(100.*_FloatsArray),
		lambda _FloatsArray:0.005*SYS.numpy.tanh(200.*_FloatsArray),
		#lambda _FloatsArray:_FloatsArray,
		#lambda _FloatsArray:SYS.Predirater.getThresholdArray(_FloatsArray,100.),
		#PrediratingMonitorIntsList
		[0,1,3,4,5,6,7],
		#PrediratingInititalFloat
		0.01,
		#PrediratingCommandNoiseFloat
		0.,
		#PrediratingRateNoiseFloat
		0.,
		#PrediratingSymmetryFloat
		1.
	).view(
	).pyplot(
	)
SYS.matplotlib.pyplot.show()

#print
print('MyPredirater is')
SYS._print(MyPredirater)
