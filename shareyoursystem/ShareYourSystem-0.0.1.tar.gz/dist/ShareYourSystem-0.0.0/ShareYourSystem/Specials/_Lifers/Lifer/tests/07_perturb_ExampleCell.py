
#/###################/#
# Import modules
#

#import
import ShareYourSystem as SYS

#define
MyLifer=SYS.LiferClass(
	).lif(
		_PerturbationLambdaVariable=-2000+2000.*2.*SYS.numpy.pi*1j,
		_PerturbationMethodStr='Brunel'
	)

#print
print('MyLifer is')
SYS._print(MyLifer)

"""
#define
MyLifer=SYS.LiferClass(
	).lif(
		_PerturbationLambdaVariable=0.1+10.*2.*SYS.numpy.pi*1j,
		_PerturbationMethodStr='Hakim'
	)

#print
print('MyLifer is')
SYS._print(MyLifer)
"""