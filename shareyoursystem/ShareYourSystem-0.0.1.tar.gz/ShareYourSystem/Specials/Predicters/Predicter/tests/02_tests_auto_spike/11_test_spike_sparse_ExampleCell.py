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

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			#'BrianingStepTimeFloat':0.05,
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
					'-Interactions':{
						'|Fast':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					'-Traces':{
						'|U':{
							#'RecordingInitFloatsArray':-65.+SYS.scipy.stats.norm(0.,0.01).rvs(size=AgentUnitsInt)
						}
					}
					#'LeakingNoiseStdVariable':0.01
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
		_CommandVariable="#custom:#clock:25*ms:1.*(1.*mV+1.*mV*(int(t==25.*ms)+int(t==50.*ms)))",#2., 
        _AgentUnitsInt = 100,
        _AgentRecordVariable = [0,1,2],
        _DecoderVariable="#array",
        
        #100
        _DecoderStdFloat = 50./SYS.numpy.sqrt(100.), #need to make an individual PSP around 1 mV
        _DecoderMeanVariable = 10., 
        _DecoderSparseFloat = 1.,
        _AgentResetVariable = -65., #cost to reset neurons and make the noise then decide who is going to spike next
        _AgentNoiseVariable = 2., #noise (mV) to make neurons not spiking at the same timestep
        _AgentThresholdVariable = -55., #set the threshold the same for everybody
        #1000
        #_DecoderStdFloat = 50./SYS.numpy.sqrt(1000.), #need to make an individual PSP around 1 mV
        #_DecoderMeanVariable = 1., 
        #_DecoderSparseFloat = 1.,
        #_AgentResetVariable = -65., #cost to reset neurons and make the noise then decide who is going to spike next
        #_AgentNoiseVariable = 2., #noise (mV) to make neurons not spiking at the same timestep
        #_AgentThresholdVariable = -55., #set the threshold the same for everybody

        #
        _SpikeRecordVariable = range(0,100),
        _AgentRefractoryVariable=0.5,
        _InteractionStr = "Spike"
	).simulate(
		100.
	)

#/###################/#
# View
#

#mapSet
MyPredicter.view(
	).pyplot(
        _FigureVariable={'figsize':(15,10)},
        _GridVariable=(40,30)
    ).show(
    )

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 

