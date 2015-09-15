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
			'BrianingStepTimeFloat':0.01,
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
					'LeakingMonitorIndexIntsList':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable,
					'-Interactions':{
						'|Fast':{
							'BrianingDebugVariable':BrianingDebugVariable
						}
					},
					#'LeakingThresholdMethodStr':"filterSpikespace"
					#'LeakingNoiseStdVariable':0.01
				}),
				('|Decoder',{
					'LeakingMonitorIndexIntsList':[0,1],
					#'BrianingDebugVariable':BrianingDebugVariable
					'-Interactions':{
						'|Slow':{
							'BrianingDebugVariable':BrianingDebugVariable,
							#'LeakingWeigthVariable':0.
						}
					}
				})
			]
		}
	).predict(
		_AgentUnitsInt=100,
		_CommandVariable="#custom:#clock:20*ms:1.*mV+1.*mV*int(t==20*ms)",#2.,
		_DecoderVariable="#array",
		_DecoderStdFloat=0.,
		_DecoderSparseFloat=0.2,
		#_AgentResetVariable=-60.,
		_InteractionStr="Spike",
		_DelayFloat=1.,
	).simulate(
		50.
	)

#/###################/#
# View
#

#mapSet
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
							'|Decoder_*U':{
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

