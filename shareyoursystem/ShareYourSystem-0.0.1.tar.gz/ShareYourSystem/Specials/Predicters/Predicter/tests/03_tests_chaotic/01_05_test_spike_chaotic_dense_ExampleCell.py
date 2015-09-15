#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#set
BrianingDebugVariable=25.

#set
AgentUnitsInt = 1000

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'BrianingStepTimeFloat':0.02,
			'-Populations':[
				('|Sensor',{
					'LeakingMonitorIndexIntsList':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Encod':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					}
				}),
				('|Agent',{
					'LeakingMonitorIndexIntsList':[0,1,2],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Traces':{
						'|U':{
							'RecordingInitMeanVariable':-70.,
							'RecordingInitStdVariable':5.,
						}
					},
					'-Events':{
						'|Default':{
							'BrianingEventSelectVariable':range(0,30)
						}
					},
					'-Interactions':{
						'|Fast':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					#'LeakingNoiseStdVariable':0.01
				}),
				('|Decoder',{
					'LeakingMonitorIndexIntsList':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable,
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
		_AgentUnitsInt=AgentUnitsInt,
		_CommandVariable = "#custom:#clock:200*ms:5.*(1.*mV+1.*mV*int(t==200*ms))",#2.,
		_DecoderVariable = "#array",
		_DecoderStdFloat = SYS.numpy.sqrt(AgentUnitsInt) * 0.3, #need to make an individual PSP around 1 mV
		_DecoderMeanFloat = AgentUnitsInt * 1.5, 
		_AgentResetVariable = -80., #big cost to reset neurons and make the noise then decide who is going to spike next
		_AgentNoiseVariable = 0.01, #noise to make neurons not spiking at the same timestep
		_AgentThresholdVariable = -40.,
		_AgentRefractoryVariable = 1.,
		_FastPerturbStdFloat = SYS.numpy.sqrt(AgentUnitsInt) * 0.2,
		_InteractionStr = "Spike"
	).simulate(
		500.
	)

#/###################/#
# View
#

MyPredicter.view(
	).mapSet(
		{
			'PyplotingFigureVariable':{
				'figsize':(10,8)
			},
			'PyplotingGridVariable':(30,30),
			'-Panels':[
				(
					'|Run',
					{
						#'PyplotingTextVariable':[-0.4,0.],
						#'PyplotingShiftVariable':[0,4],
						#'PyplotingShapeVariable':[8,9],
						'-Charts':{
							'|Decoder_U':{
								'PyplotingLegendDict':{
									'fontsize':12,
									'ncol':2
								}
							}
						}
					}
				),
				(
					'|Stat',
					{
						'PyplotingTextVariable':[-0.4,0.],
						'PyplotingShiftVariable':[0,4],
						'PyplotingShapeVariable':[5,9],
					}
				)
			]
		}
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 


