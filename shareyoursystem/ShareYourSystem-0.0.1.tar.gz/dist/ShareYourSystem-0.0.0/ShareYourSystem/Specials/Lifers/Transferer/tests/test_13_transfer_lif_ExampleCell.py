#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyTransferer=SYS.TransfererClass(
	).stationarize(
		_MeanWeightVariable=[
			[0.,-10.],
			[10.,0.]
		],
		_RateVariable = [5.,5.],
		_InteractionStr = "Spike"
	).stabilize(
		_ComputeBool=False
	).transfer(
	).view(
		_ColorStrsList = ["red","blue"]
	).pyplot(
	).show(
	)

#print
#print('MyTransferer is ')
#SYS._print(MyTransferer) 

