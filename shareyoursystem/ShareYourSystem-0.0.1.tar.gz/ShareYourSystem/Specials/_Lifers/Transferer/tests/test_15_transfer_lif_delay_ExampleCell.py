#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyTransferer=SYS.TransfererClass(
	).stationarize(
		_MeanWeightVariable=[
			[0.,100.],
			[100.,-200.]
		],
		_ConstantTimeVariable=[0.02,0.01],
		_RateVariable = [10.,30.],
		_InteractionStr = "Spike"
	).stabilize(
		_ComputeBool=False,
		_DelayTimeVariable=[
			[0.001,0.0005],
			[0.001,0.0005]
		],
		_DecayTimeVariable=[
			[0.002,0.006],
			[0.002,0.006]
		],
		_RiseTimeVariable=[
			[0.001,0.0005],
			[0.001,0.0005]
		]
	).explore(
		_MethodStr = 'transfer',
		_ConditionVariable=[
			(
				'checkPeak',
				lambda self:len(self.TransferedNormRateAmplitudeFloatsArray[0])>1 and self.TransferedNormRateAmplitudeFloatsArray[0][1]>120.
			)
		]
	)
	#.view(
	#	_ColorStrsList = ["red","blue"],
	#	_LabelStrsList = ["E","I"]
	#).pyplot(
	#).show(
	#)


#print
print('MyTransferer is ')
SYS._print(MyTransferer) 

