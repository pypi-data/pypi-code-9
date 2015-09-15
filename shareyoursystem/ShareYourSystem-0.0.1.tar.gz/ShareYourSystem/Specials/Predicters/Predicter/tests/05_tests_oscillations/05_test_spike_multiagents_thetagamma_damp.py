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
I_I = SYS.numpy.array([[0.2, 0.4, 0.],
               [0., 0.1, 0.3],
                [0.3, 0., 0.2]])
A = SYS.numpy.zeros((5, 5))
A[:2,:2] = E_I
A[2:,2:] = I_I
A = (-1./float(JacobianTimeFloat))*A

#set
AgentUnitsInt=100

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'NumscipyingSeedVariable':4,
			'BrianingStepTimeFloat':0.02,
			'-Populations':[
				('|Sensor',{
					'RecordingLabelVariable':[0,1,2,3,4],
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
							'RecordingInitFloatsArray':scipy.stats.norm(
								0.,0.01
							).rvs(size=AgentUnitsInt)
						}
					}
					#'LeakingNoiseStdVariable':0.01
				}),
				('|Decoder',{
					'RecordingLabelVariable':[0,1,2,3,4],
					#'BrianingDebugVariable':BrianingDebugVariable
					'-Interactions':{
						'|Slow':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					}
				})
			]
		}
	).predict(
		_DynamicBool = True,
		_JacobianVariable = A,
		_CommandVariable = "#custom:#clock:250*ms:(0.5/"+str(
			JacobianTimeFloat
		)+")*mV*(int(t==250*ms)+int(t==500*ms))",
		_DecoderVariable = "#array",
		_DecoderTimeFloat = 10., #(ms)
		_DecoderMeanFloat = 0., 
		_DecoderStdFloat = 80./SYS.numpy.sqrt(AgentUnitsInt),
		_AgentUnitsInt = AgentUnitsInt,
		_AgentTimeFloat = 10., #(ms)
		_InteractionStr="Rate"
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




