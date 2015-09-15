
#ImportModules
import ShareYourSystem as SYS

#Define
MyPredispiker=SYS.PredispikerClass(
	).predict(
		#PredictingUnitsInt
		1,
		#PredictingSensorsInt
		1,
		#PredictingConstantTimeFloat (ms)
		1.,
		#PredictingDecoderWeigtFloat
		3.,
		#PredictingCostFloat
		1.,
		#PredictingNormalisationInt
		0.5,
		#PredictingPerturbativeInputWeightFloat
		0.,
		#PredictingPerturbativeLateralWeightFloat
		0.
	).predispike(
		#PredispikingRunTimeFloat (ms)
		50.,
		#PredispikingStepTimeFloat (ms)
		0.1,
		#PrediratingClampFloat
		0.1,
		#PredispikingRestFloat
		-60.
	)

#print
print('MyPredispiker is')
SYS._print(MyPredispiker)

