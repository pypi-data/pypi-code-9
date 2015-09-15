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
					'RecordingLabelVariable':[0],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Fast':{
							#'BrianingDebugVariable':BrianingDebugVariable,

						}
					},
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
		_AgentUnitsInt=1,
		_CommandVariable="#custom:#clock:20*ms:0.5*(1.*mV+1.*mV*(int(t==20*ms)+int(t==80*ms)))",#2.,
		_DecoderVariable=[2.],
		#_FastWeightVariable=[-3.],#too weak
		_FastWeightVariable=[-5.],#too strong
		_InteractionStr="Spike",
		#_AgentResetVariable=-70.,
		#_AgentRefractoryVariable=0.5 BE CAREFUL NOT WORKING BECAUSE auto IPSP is then not inducted
		_FastPlasticBool=True,
		_FastLearnRateFloat=0.1
	).simulate(
		150.
	)

#/###################/#
# View
#

MyPredicter.mapSet(
		{
			'PyplotingFigureVariable':{
				'figsize':(10,8)
			},
			'PyplotingGridVariable':(45,30),
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
									'|Agent_Fast_J',
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


