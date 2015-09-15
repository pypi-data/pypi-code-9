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
		_StdWeightFloat=60.,
		_CriticalBool=True
	).leak(
	).simulate(
		500.
	).view(
	).pyplot(
	).show(
	)

#print
print('MyHopfer is ')
SYS._print(MyHopfer) 
