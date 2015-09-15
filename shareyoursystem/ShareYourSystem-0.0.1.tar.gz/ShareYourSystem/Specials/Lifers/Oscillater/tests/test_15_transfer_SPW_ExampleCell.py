#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS
import scipy.stats

#/###################/#
# Build the model
#

#Define
MyOscillater=SYS.OscillaterClass(
	).mapSet(
		{
			"-Modes":{
				"ManagingAfterVariable":{
					"StationarizingConstantTimeVariable":[0.02,0.01],
					"StationarizingInteractionStr":"Spike",
					"StabilizingDelayTimeVariable":[
						[0.001,0.0005],
						[0.001,0.0005]
					],
					"StabilizingDecayTimeVariable":[
						[0.002,0.006],
						[0.002,0.006]
					],
					"StabilizingRiseTimeVariable":[
						[0.001,0.0005],
						[0.001,0.0005]
					]
				},			
				"|Sleep":{
					"StationarizingRateVariable":[10.,30.],
					"-Resonances":{
						"|Ripple":{
							"OscillatingFrequencyFloatsTuple":(120.,200.),
							"OscillatingUnitInt":0
						}
					}
				}
			}
		}
	).explore(
		"oscillate",
		_RangeVariable={
			'OscillatingMeanWeightVariable':lambda self:SYS.numpy.array([
				[100.*scipy.stats.uniform.rvs(),-100.*scipy.stats.uniform.rvs()],
				[100.*scipy.stats.uniform.rvs(),-100.*scipy.stats.uniform.rvs()]
			])
		},
		_TrialsInt=1
	)

"""
	.execute(
		"self.mapSet(self.ExploredStoreTuplesListsList[0])"
	).view(
		_ColorStrsList = ["red","blue"],
		_LabelStrsList = ["E","I"]
	).pyplot(
	).show(
	)
"""

#print
#print('MyOscillater is ')
#SYS._print(MyOscillater) 

