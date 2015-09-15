
#ImportModules
import ShareYourSystem as SYS

#Define
MyPredisenser=SYS.PredisenserClass(
	).predict(
		#PredictingUnitsInt
		10,
		#PredictingSensorsInt
		5,
		#PredictingDynamicStr
		'Gamma-Theta',
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
		[0,1,2,3,4,5]
	).draw(
	).show(
	)

#print
print('MyPredisenser is')
SYS._print(MyPredisenser)
