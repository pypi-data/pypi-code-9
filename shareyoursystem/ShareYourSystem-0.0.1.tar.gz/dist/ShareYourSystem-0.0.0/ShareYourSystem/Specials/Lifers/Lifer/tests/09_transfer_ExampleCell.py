
#/###################/#
# Import modules
#

#import
import ShareYourSystem as SYS

#define
MyLifer=SYS.LiferClass(
    ).lif(
        _PerturbationFrequencyFloat=400.,
        _PerturbationMethodStr='Brunel'
    )

#print
print('MyLifer is')
SYS._print(MyLifer)

#define
MyLifer=SYS.LiferClass(
    ).lif(
        _PerturbationFrequencyFloat=400.,
        _PerturbationMethodStr='Hakim'
    )

#print
print('MyLifer is')
SYS._print(MyLifer)