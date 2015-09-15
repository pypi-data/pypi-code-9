
#ImportModules
import ShareYourSystem as SYS

#Definition an instance
MySimulater=SYS.SimulaterClass(
	).mapSet(
		{
			'FirstArray':SYS.numpy.array([[1,2,5,6],[3,5,7,8]]),
			'SecondArray':SYS.numpy.array([[1,2,5,6],[3,5,7,8]]),
			'-Traces':{
				'|*FirstArray':{
					'-Samples':{
						'|Run':{
							'MoniteringLabelIndexIntsArray':[0,1]
						}
					}
				}
			}
		}
	).record(
	)

#Definition the AttestedStr
print('MySimulater is ')
SYS._print(MySimulater)


