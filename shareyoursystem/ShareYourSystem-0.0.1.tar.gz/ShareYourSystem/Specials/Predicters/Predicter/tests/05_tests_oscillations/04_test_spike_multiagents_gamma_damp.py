#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS
import scipy.stats
import numpy
numpy.random.seed(4)


#/###################/#
# Build the model
#

#Simulation time
SimulationTimeFloat=1000.
#SimulationTimeFloat=0.2
BrianingDebugVariable=0.1 if SimulationTimeFloat<0.5 else 25.

#A - transition matrix
JacobianTimeFloat = 10. #(ms)
E_I = SYS.numpy.array([[-3., 6.],
                [-4., 4.]])
A = SYS.numpy.zeros((2, 2))
A[:2,:2] = E_I
A = (-1./float(JacobianTimeFloat))*A

#set
AgentUnitsInt=1000

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'NumscipyingSeedVariable':4,
			'BrianingStepTimeFloat':0.02,
			'-Populations':[
				('|Sensor',{
					'RecordingLabelVariable':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Encod':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					}
				}),
				('|Agent',{
					'RecordingLabelVariable':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Traces':{
						'|U':{
							'RecordingInitMeanVariable':-70.,
							'RecordingInitStdVariable':5.,
						}
					},
					'-Interactions':{
						'|Fast':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					#'LeakingNoiseStdVariable':0.01
					#'LeakingThresholdMethodStr':'filterSpikespace'
				}),
				('|Decoder',{
					'RecordingLabelVariable':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable
					'-Interactions':{
						'|Slow':{
							#'BrianingDebugVariable':BrianingDebugVariable,
							#'LeakingWeigthVariable':0.
						}
					}
				})
			]
		}
	).predict(
		_AgentUnitsInt = AgentUnitsInt,
		_JacobianVariable=A,
		_CommandVariable="#custom:#clock:250*ms:0.25*(1.*mV+1.*mV*(int(t==250*ms)+int(t==500*ms)))",
		_DecoderVariable = "#array",
		_DecoderStdFloat = 0.,
		_DecoderMeanFloat = AgentUnitsInt * 1., #need to make an individual PSP around 1 mV
		_AgentResetVariable = -75., #big cost to reset neurons and make the noise then decide who is going to spike next
		_AgentNoiseVariable = 0.5, #noise to make neurons not spiking at the same timestep
		_AgentThresholdVariable = -58.5, #increase the threshold in order to have a linear cost
		_AgentRefractoryVariable = 0.5,
		_InteractionStr = "Spike"
	).simulate(
		SimulationTimeFloat
	)

#/###################/#
# View
#

MyPredicter.mapSet(
		{
			'PyplotingFigureVariable':{
				'figsize':(10,8)
			},
			'PyplotingGridVariable':(30,30),
			'-Panels':[
				(
					'|Run',
					[
						(
							'-Charts',
							[
								(
									'|Sensor_I_Command',
									{
										'PyplotingLegendDict':{
											'fontsize':10,
											'ncol':2
										}
									}
								),
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
											'ncol':1
										}
									}
								),
								(
									'|Agent_Default',{}
								),
								(
									'|Decoder_U',
									{
										'PyplotingLegendDict':{
											'fontsize':10,
											'ncol':1
										}
									}
								)
							]
						)
					]
				)
			]
		}
	).view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 




