#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyLeaker=SYS.LeakerClass(
	).mapSet(
		{
			'-Populations':{
				'|Sensor':{
					'LeakingUnitsInt':2,
					'LeakingSymbolPrefixStr':'r',
					'-Inputs':{
						'|Command':{
							#'LeakingWeightVariable':'#scalar:3.*mV',
							#'LeakingWeightVariable':5.,
							#'LeakingWeightVariable':5.*SYS.brian2.mV,
							#'LeakingWeightVariable':[1.,3.],
							##'LeakingWeightVariable':SYS.getKrenelFloatsArray,
							#'LeakingWeightVariable':"#equation:5.*mV*(1.+tanh(10.*(t-250.*ms)/ms))",
							#'LeakingWeightVariable':"#custom:#clock:10*ms:change=int(t>250*ms);#SymbolStr=5.*mV*change",
							#'LeakingWeightVariable':'#custom:5.*mV*(ms/(t+1*ms))',
							#'LeakingWeightVariable':'#custom:#clock:200*ms:5.*mV*(t==200*ms)*(i==0)',
							'LeakingWeightVariable':'#custom:#clock:200*ms:5.*mV*(t==200*ms)*(i==0)',
							#'LeakingWeightVariable':(
							#	'#custom:#clock:100*ms',
							#	[
							#		'5.*mV*int(t==200*ms)',
							#		'-2.*mV*int(t==100*ms)'
							#	]
							#),
							#'LeakingWeightVariable':(
							#	'#network:#clock:200*ms',
							#	lambda _ActivityQuantity,_TimeQuantity:
							#	5.*SYS.brian2.mV 
							#	if _TimeQuantity==200.*SYS.brian2.ms
							#	else 0.*SYS.brian2.mV
							#),
							#'LeakingWeightVariable':(
							#	'#network:#clock:1*ms',
							#	lambda _ActivityQuantity,_TimeQuantity:
							#	SYS.scipy.stats.norm.rvs(size=2)*SYS.brian2.mV
							#),
							#'RecordingLabelVariable':[0,1]
						}
					},
					'RecordingLabelVariable':[0,1]
				}
			}
		}
	).leak(
	)
	
#/###################/#
# Do one simulation
#

MyLeaker.simulate(
		500.
	)

#/###################/#
# View
#

MyLeaker.mapSet(
		{
			'PyplotingGridVariable':(20,20)
		}
	).view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyLeaker is ')
SYS._print(MyLeaker) 



