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
BrianingDebugVariable=25.

#Simulation time
SimulationTimeFloat=1000.

#set
AgentUnitsInt = 100

#A - transition matrix
JacobianTimeFloat = 10. #(ms)
A =  (-1./float(JacobianTimeFloat)
	)*SYS.numpy.array([[1.]])

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'NumscipyingSeedVariable':4,
			'BrianingStepTimeFloat':0.02, #(ms)
			'-Populations':[
				('|Sensor',{
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Inputs':{
						'|Command':{
							'RecordingLabelVariable':[0,1]
						}
					},
					'-Interactions':{
						'|Encod':{
							#'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					'RecordingLabelVariable':[0,1]
				}),
				('|Agent',{
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
					},
					'RecordingLabelVariable':[0,1,2]
				}),
				('|Decoder',{
					#'BrianingDebugVariable':BrianingDebugVariable,
					'RecordingLabelVariable':[0,1]
				})
			]
		}
	).predict(
		_DynamicBool = False,
		_JacobianVariable = A,
		 _CommandVariable = "#custom:#clock:250*ms:(0.5/"+str(
			JacobianTimeFloat
		)+")*mV*(int(t==250*ms)+int(t==500*ms))",
		#_AgentTimeFloat = 10.,
		_DecoderVariable = "#array",
		_DecoderMeanFloat = 0.,
		_DecoderStdFloat = 20./SYS.numpy.sqrt(AgentUnitsInt),
		_AgentUnitsInt =  AgentUnitsInt,
		_InteractionStr = "Rate"
	).simulate(
		SimulationTimeFloat
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
	).show(
	)

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 





