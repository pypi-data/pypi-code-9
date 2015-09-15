#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#set
BrianingDebugVariable = 25.

#set
AgentUnitsInt = 1000

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'BrianingStepTimeFloat':0.02,
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
					'RecordingLabelVariable':[0],
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
		_AgentUnitsInt=AgentUnitsInt,
		_JacobianVariable = (
            -1./float(30.) #(ms)
        )*SYS.numpy.array([[1.]]), #A matrix
		_CommandVariable="#custom:#clock:40*ms:1.*(1.*mV+1.*mV*int(t==40*ms))",#2.,
		_DecoderVariable="#array",
		_DecoderStdFloat = 300./SYS.numpy.sqrt(AgentUnitsInt), #need to make an individual PSP around 1 mV
		_DecoderMeanFloat = 0./AgentUnitsInt, 
		_AgentResetVariable = -61., #big cost to reset neurons and make the noise then decide who is going to spike next
		_AgentNoiseVariable = 2., #noise to make neurons not spiking at the same timestep
		_AgentThresholdVariable = -59.,
		_SpikeRecordVariable = range(0,100),
		#_AgentRefractoryVariable=0.5,
		_InteractionStr = "Spike"
	).simulate(
		200.
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
									'|Agent_Default_Events',{}
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

