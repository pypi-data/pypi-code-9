#ImportModules
import ShareYourSystem as SYS

#Define
MyTransferer=SYS.TransfererClass(
	).stationarize(
		_MeanWeightVariable=[
			#[0.5,-500.],
			#[500.,-10.]
			[0.,0.],
			[0.,0.]
		]
	).stabilize(
		_ComputeBool=False
	).transfer(
	).view(
	).pyplot(
	).show(
	)

#print(MyTransferer.TeamDict['Panels'].ManagementDict['Transfer'].TeamDict['Charts'])

#print
print('MyTransferer is ')
SYS._print(MyTransferer) 
