#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Definition an instance
MyBrianer=SYS.BrianerClass(
	).mapSet(
		{
			'BrianingNeurongroupDict':{
				'N':10,
				'model':
				'''
					dv/dt = (-(v+60*mV)+11*mV + 5.*mV*sqrt(20.*ms)*xi)/(20*ms) : volt
				''',
				'threshold':'v>-50*mV',
				'reset':'v=-70*mV'
			},
			'-Traces':{
				'|*v':{
					'NumscipyingStdFloat':0.001,
					'-Samples':{
						'|Default':{
							'MoniteringLabelIndexIntsArray':[0,1]						
						}
					}
				}
			},
			'-Events':{
				'|Default':{
				}
			}
		}	
	).brian(
	)
	
#/###################/#
# Print
#

#Definition the AttestedStr
print('MyBrianer is ')
SYS._print(MyBrianer) 

#/###################/#
# Do one simulation
#

MyBrianer.simulate(
		500.
	)

#/###################/#
# View
#

#MyBrianer['/-Traces/|*v/-Samples/|Default'].pyplot()
#MyBrianer['/-Events/|Default'].pyplot()
MyBrianer.pyplot()
SYS.matplotlib.pyplot.show()


"""
from matplotlib import pyplot
pyplot.figure()
M=MyBrianer['/-Traces/|*v/-Samples/|Default'].BrianedStateMonitorVariable
pyplot.plot(M.t, M.v.T)
pyplot.figure()
M=MyBrianer['/-Events/|Default'].BrianedSpikeMonitorVariable
pyplot.plot(M.t, M.i,'.')
pyplot.show()
"""