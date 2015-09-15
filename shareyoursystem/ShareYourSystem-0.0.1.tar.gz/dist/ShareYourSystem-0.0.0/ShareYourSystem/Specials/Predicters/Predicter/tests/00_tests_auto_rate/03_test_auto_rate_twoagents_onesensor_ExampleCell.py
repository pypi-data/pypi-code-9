#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Simulation time
SimulationTimeFloat=100.
#SimulationTimeFloat=0.2
BrianingDebugVariable=0.1 if SimulationTimeFloat<0.5 else 25.

#A - transition matrix
JacobianTimeFloat = 10. #(ms)
A =  (-1./float(JacobianTimeFloat)
	)*SYS.numpy.array([[1.,0.],[0.,1.]])

#Define
MyPredicter=SYS.PredicterClass(
	).mapSet(
		{
			'BrianingStepTimeFloat':0.02,
			'-Populations':[
				('|Sensor',{
					#'BrianingDebugVariable':BrianingDebugVariable,
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
					'RecordingLabelVariable':[0,1]
				}),
				('|Decoder',{
					#'BrianingDebugVariable':BrianingDebugVariable,
					'RecordingLabelVariable':[0,1]
				})
			]
		}
	).predict(
		_DynamicBool=False,
		#_JacobianVariable = A,
		_CommandVariable=(
			'#custom:#clock:25*ms',
			[
				"(1./"+str(
					JacobianTimeFloat
				)+")*mV*(int(t==25*ms)+int(t==50*ms))",
				"(-1./"+str(
					JacobianTimeFloat
				)+")*mV*(int(t==25*ms)+int(t==50*ms))"
			]
		),
		#_AgentTimeFloat = 10.,
		_DecoderVariable = SYS.numpy.array([[7.,1.],[1.2,7.1]]),
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
	).show()

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 





