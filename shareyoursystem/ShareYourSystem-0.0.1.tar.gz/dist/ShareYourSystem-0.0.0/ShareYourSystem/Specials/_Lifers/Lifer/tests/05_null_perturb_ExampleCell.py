
#/###################/#
# Import modules
#

#import
import ShareYourSystem as SYS

#define
MyLifer=SYS.LiferClass(
	).lif(
		_PerturbationLambdaVariable=0.,
		_PerturbationMethodStr='Brunel'
	)

#print
print('MyLifer is')
SYS._print(MyLifer)
