#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Simulation time
SimulationTimeFloat=1000.
#SimulationTimeFloat=0.2
BrianingDebugVariable=0.1 if SimulationTimeFloat<0.5 else 25.

#A - transition matrix
JacobianTimeFloat = 10. #(ms)
A =  (-1./float(JacobianTimeFloat)
	)*SYS.numpy.array([[1.]])

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
					'-Traces':{
						'|U':{
							'RecordingInitMeanVariable':0.,
							'RecordingInitStdVariable':0.1,
						}
					},
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
		_JacobianVariable=A,
		_CommandVariable = "#custom:#clock:250*ms:(0.5/"+str(
			JacobianTimeFloat
		)+")*mV*(int(t==250*ms)+int(t==500*ms))",
		_RateTransferVariable='(1./<ThresFloat>)*mV*tanh((<ThresFloat>*(#CurrentStr))/(1.*mV))'.replace(
				'<ThresFloat>',
				'10.'
			),
		_DecoderVariable='#array',
		_DecoderStdFloat=7.,
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
	).mapSet(
		{
			'-Panels':[
					(
						'|Run',
						[
							(
								'-Charts',
								[
									(
										'|Sensor_U',
										{
											'PyplotingLegendDict':{
												'fontsize':10,
												'ncol':2
											}
										}
									),
									(
										'|Agent_U',
										{
											'PyplotingLegendDict':{
												'fontsize':10,
												'ncol':2
											}
										}
									),
									(
										'|Decoder_U',
										{
											'PyplotingLegendDict':{
												'fontsize':10,
												'ncol':2
											}
										}
									)
								]
							)
						]
					)
				]
		}
	).pyplot(
	).show()


#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 







