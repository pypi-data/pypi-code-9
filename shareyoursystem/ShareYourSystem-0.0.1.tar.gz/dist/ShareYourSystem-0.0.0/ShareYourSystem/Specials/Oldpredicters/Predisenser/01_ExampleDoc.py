
#ImportModules
import ShareYourSystem as SYS

#Define
MyPredisenser=SYS.PredisenserClass(
	).oldpredict(
		#PredictingUnitsInt
		10,
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
		10.,
		#PredictingNormalisationInt
		0.5,			
		#PredictingCostFloat
		0.,
		#PredictingPerturbativeInputWeightFloat
		0.,
		#PredictingPerturbativeLateralWeightFloat
		0.,
		#PredictingInputRandomStatStr
		'norm',
		#PredictingLateralRandomStatStr
		'norm'
	).predisense(
		#PredisensingRunTimeFloat (ms)
		100.,
		#PredisensingStepTimeFloat (ms)
		0.1,
		#PredisensingClampFloat
		0.5,
		#PredisensingMonitorIntsList
		[0]
	).view(
	).pyplot(
	)
SYS.matplotlib.pyplot.show()

#print
print('MyPredisenser is')
SYS._print(MyPredisenser)
