
#ImportModules
import ShareYourSystem as SYS

#Define
MyStabilizer=SYS.StabilizerClass(
	).stationarize(
		_MeanWeightVariable=[[-1700.]]
	).stabilize(
		_DelayTimeVariable=0.001,
		_ScanFrequencyVariable=[10.]
	)

#Choose the parameters to print
KeyStrsList=[
			'StationarizingMeanWeightVariable',
			'StabilizingConstantTimeVariable', #in ms
			'StabilizingDelayTimeVariable',
			'StabilizedTotalPerturbationComplexesArray', #matrix M
			'StabilizedDeterminantFloatsTuple',  #If it has converged, then it has to be closed to (0,0)
			'StabilizedInstabilityLambdaFloatsTuple',  # real part should be negative if stable,  (from this particular initial condition)
			'StabilizedInstabilityFrequencyFloat'
		]

#print
SYS._print(SYS.collections.OrderedDict(zip(KeyStrsList,MyStabilizer.mapGet(KeyStrsList))))
