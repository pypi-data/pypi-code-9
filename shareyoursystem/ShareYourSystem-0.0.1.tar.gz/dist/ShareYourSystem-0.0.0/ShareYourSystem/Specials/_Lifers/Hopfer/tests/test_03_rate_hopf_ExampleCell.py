#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyHopfer=SYS.HopferClass(
	).hopf(
		_UnitsInt=100,
		_StdWeightFloat=90.,
		_SymmetryFloat=-0.7,
		_CriticalBool=True
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
