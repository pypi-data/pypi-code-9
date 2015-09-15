

#ImportModules
import ShareYourSystem as SYS

#Define
MyStationarizer=SYS.StationarizerClass(
	).stationarize(
		_ConstantTimeVariable=[0.02],
		_ExternalCurrentMeanVariable=[15.],
		_NoiseWeightVariable=[[15.]],
		_InteractionStr="Spike"
	)

#print
print('MyStationarizer is ')
SYS._print(MyStationarizer) 

