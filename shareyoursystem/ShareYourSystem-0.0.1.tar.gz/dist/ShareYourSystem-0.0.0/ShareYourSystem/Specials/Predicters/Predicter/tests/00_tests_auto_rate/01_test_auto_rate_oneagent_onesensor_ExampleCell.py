#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyPredicter=SYS.PredicterClass(
	).predict(
		_DynamicBool=False,
		_CommandVariable = "#custom:#clock:25*ms:0.5*mV*(int(t==25*ms)+int(t==50*ms))", #c array
		_DecoderVariable = [2.], #D array
		_InteractionStr = "Rate"
	).simulate(
		100. #(ms)
	)

#/###################/#
# View
#

MyPredicter.view(
	).pyplot(
	).show()

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyPredicter is ')
SYS._print(MyPredicter) 





