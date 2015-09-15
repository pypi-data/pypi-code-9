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

#set
AgentUnitsInt = 100

#SimulationTimeFloat=0.2
BrianingDebugVariable=0.1 if SimulationTimeFloat<0.5 else 25.

#A - transition matrix
JacobianTimeFloat = 30. #(ms)
A =  (-1./float(JacobianTimeFloat)
	)*SYS.numpy.array([[1.]])

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'NumscipyingSeedVariable':4,
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
					},
					'-Traces':{
						'|U':{
							'RecordingInitFloatsArray':scipy.stats.norm(0.,0.01).rvs(size=AgentUnitsInt)
						}
					}
					#'LeakingNoiseStdVariable':0.01
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
		_DynamicBool=True,
		_JacobianVariable=A,
		_CommandVariable="#custom:#clock:250*ms:(0.5/"+str(
			JacobianTimeFloat
		)+")*mV*(int(t==250*ms)+int(t==500*ms))",
		_AgentTimeFloat = 10.,
		_AgentUnitsInt = AgentUnitsInt,
		_DecoderVariable = "#array",
		_DecoderMeanFloat = 0.,
		_DecoderStdFloat = 20./SYS.numpy.sqrt(AgentUnitsInt),
		_InteractionStr = "Rate"
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



