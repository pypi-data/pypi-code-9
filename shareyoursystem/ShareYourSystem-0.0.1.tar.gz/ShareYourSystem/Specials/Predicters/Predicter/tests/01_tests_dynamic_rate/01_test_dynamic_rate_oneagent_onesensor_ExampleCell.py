#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Simulation time
BrianingDebugVariable=25.

#A - transition matrix
JacobianTimeFloat = 30. #(ms)
A =  (-1./float(JacobianTimeFloat)
	)*SYS.numpy.array([[1.]])

#Define
MyPredicter=SYS.PredicterClass(
	).predict(
		_DynamicBool=True,
		_JacobianVariable=A,
		_CommandVariable="#custom:#clock:25*ms:0.5*mV*(int(t==25*ms)+int(t==50*ms))",
		_DecoderVariable = [2.],
		_InteractionStr="Rate"
	).simulate(
		100.
	)

#/###################/#
# View
#

MyPredicter.mapSet(
		{
			'PyplotingFigureVariable':{
				'figsize':(10,8)
			},
			'PyplotingGridVariable':(30,30)
		}
	).view(
	).pyplot(
	).show(
	)


#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 



