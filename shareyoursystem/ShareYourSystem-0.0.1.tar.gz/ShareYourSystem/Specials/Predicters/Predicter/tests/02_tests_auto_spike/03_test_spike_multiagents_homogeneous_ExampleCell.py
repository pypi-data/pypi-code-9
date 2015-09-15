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

#
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
					'-Interactions':{
						'|Fast':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					},
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
		_AgentUnitsInt = AgentUnitsInt,
		_CommandVariable = "#custom:#clock:40*ms:5.*(1.*mV+1.*mV*int(t==40*ms))",#2.,
		_DecoderVariable = "#array",
		_DecoderStdFloat = 0.,
		_DecoderMeanFloat = AgentUnitsInt * 0.5, #need to make an individual PSP around 1 mV
		_AgentResetVariable = -70., #big cost to reset neurons and make the noise then decide who is going to spike next
		_AgentNoiseVariable = 1., #noise to make neurons not spiking at the same timestep
		#_AgentThresholdVariable = -53., #increase the threshold in order to have a linear cost
		_AgentRefractoryVariable=0.5,
		_InteractionStr = "Spike"
	).simulate(
		100.
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

