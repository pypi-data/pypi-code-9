#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#set
StdWeightFloat=15.

#/###################/#
# Build the model
#

#Define
MyHopfer=SYS.HopferClass(
	).hopf(
		_PerturbationAllBool = False,
		_PerturbationEnvelopBool = False,
		_UnitsInt=1000,
		_StdWeightFloat=15.,
		_StationaryExternalMeanVariable = 15.,
		_SymmetryFloat=-0.7,
		_InteractionStr="Spike"
	).leak(
	).simulate(
		500.
	).view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#print
print('MyHopfer is ')
SYS._print(MyHopfer) 
