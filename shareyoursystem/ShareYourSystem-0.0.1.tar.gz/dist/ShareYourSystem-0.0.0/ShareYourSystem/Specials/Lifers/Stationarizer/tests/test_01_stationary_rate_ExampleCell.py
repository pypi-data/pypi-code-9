
#ImportModules
import ShareYourSystem as SYS

#Define
MyStationarizer=SYS.StationarizerClass(
	).stationarize(
		_WeightVariable=[[-1.]],
		_ConstantTimeVariable=[0.02,0.01],
		_RateVariable=[5.,15.]
	)

#print
print('MyStationarizer is ')
SYS._print(MyStationarizer) 

