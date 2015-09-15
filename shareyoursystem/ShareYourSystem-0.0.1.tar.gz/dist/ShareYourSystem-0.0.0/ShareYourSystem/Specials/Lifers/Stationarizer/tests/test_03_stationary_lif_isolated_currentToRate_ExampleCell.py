
#ImportModules
import ShareYourSystem as SYS

#Define
MyStationarizer=SYS.StationarizerClass(
	).stationarize(
		_ConstantTimeVariable=[0.02,0.01],
		_ExternalCurrentMeanVariable=[15.,15.],
		_ExternalCurrentNoiseVariable=[5.,5.],
		_InteractionStr="Spike"
	)

#print
print('MyStationarizer is ')
SYS._print(MyStationarizer) 



