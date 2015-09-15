#/###################/#
# Import modules
#

#import
import ShareYourSystem as SYS

#define
MyLifer=SYS.LiferClass(
	).lif(
    	_StationaryExternalCurrentMeanFloat=15.,
    	_StationaryExternalCurrentNoiseFloat=21.
	)


#print
print('MyLifer is')
SYS._print(MyLifer)


