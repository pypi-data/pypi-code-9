#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Simulation time
SimulationTimeFloat=150.
#SimulationTimeFloat=0.2
BrianingDebugVariable=0.1 if SimulationTimeFloat<0.5 else 25.

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'BrianingStepTimeFloat':0.05,
			'-Populations':[
				('|Sensor',{
					'RecordingLabelVariable':[0],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Encod':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					}
				}),
				('|Agent',{
					'RecordingLabelVariable':[0,1,2],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Fast':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					}
				}),
				('|Decoder',{
					'RecordingLabelVariable':[0],
					#'BrianingDebugVariable':BrianingDebugVariable
				})
			]
		}
	).predict(
		_AgentUnitsInt=100,
		_DynamicBool=False,
		_JacobianVariable={
			'ModeStr':"Track",
			'ConstantTimeFloat':2. #(ms)
		},
		_CommandVariable="#custom:#clock:50*ms:1.*mV*int(t==50*ms)",#2.,
		_RateTransferVariable='(1./<ThresFloat>)*mV*tanh((<ThresFloat>*(#CurrentStr))/(1.*mV))'.replace(
				'<ThresFloat>',
				'10.'
			),
		_DecoderVariable='#array',
		_DecoderStdFloat=8.,
		_DecoderNormalisationInt=1,
		_InteractionStr="Rate",
		#_EncodPerturbStdFloat=5./100.,
		_FastPerturbStdFloat=0.04
	).simulate(
		SimulationTimeFloat
	)

#/###################/#
# View
#

MyPredicter.view(
	).pyplot(
	).show()


#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 







