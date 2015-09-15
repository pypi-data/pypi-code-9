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
			'-States':{
				'|*v':{
					'MatrixingStdFloat':0.001
				}
			}
		}	
	).brian(
	).simulate(
		500.
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

"""
#Print
from brian2 import Network,ms,mV
MyNetwork=Network()
map(
	MyNetwork.add,
	SYS.flat(
		[
			MyBrianer.NeurongroupedBrianVariable,
			MyBrianer.NeurongroupedSpikeMonitorsList,
			MyBrianer.NeurongroupedStateMonitorsList
		]
	)
)

#plot
MyBrianer.NeurongroupedBrianVariable.v=-55.*mV
MyNetwork.run(500.*ms)
M=MyBrianer.NeurongroupedSpikeMonitorsList[0]
from matplotlib import pyplot
pyplot.plot(M.t/ms, M.i, '.')
pyplot.show()
"""
