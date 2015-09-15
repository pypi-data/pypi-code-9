
#ImportModules
import ShareYourSystem as SYS

#Definition an instance
MyRecorder=SYS.RecorderClass(
	).mapSet(
		{
			'MyArray':SYS.numpy.array([4.,5.,8.]),
			'-Traces':{
				'|*MyArray':{
				}
			},
			'-Events':{

			}
		}
	).record(
	)

#Definition the AttestedStr
print('MyRecorder is ')
SYS._print(MyRecorder)

#print
print("MyRecorder['/-Traces/|*MyArray'].RecordedInitFloatsArray is ")
print(MyRecorder['/-Traces/|*MyArray'].RecordedInitFloatsArray)


