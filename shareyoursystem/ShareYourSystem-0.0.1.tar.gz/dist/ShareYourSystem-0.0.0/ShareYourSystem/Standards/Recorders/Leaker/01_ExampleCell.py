#/###################/#
# Import modules
#


#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Definition an instance
MyLeaker=SYS.LeakerClass(
	).mapSet(
		{
			'LeakingUnitsInt':3,
			#'LeakingTimeVariable':0.,
			'LeakingTimeVariable':'#scalar:20.*ms',
			#'LeakingTimeVariable':20.,
			#'LeakingTimeVariable':20.*SYS.brian2.ms,
			#'LeakingTimeVariable':[10.,20.,10.],
			'RecordingLabelVariable':[0,1],
			'LeakingSymbolPrefixStr':'r'
		}
	).leak(
	).simulate(
		500.
	)

#/###################/#
# View
#

MyLeaker.view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#print
print('MyLeaker is ')
SYS._print(MyLeaker) 


