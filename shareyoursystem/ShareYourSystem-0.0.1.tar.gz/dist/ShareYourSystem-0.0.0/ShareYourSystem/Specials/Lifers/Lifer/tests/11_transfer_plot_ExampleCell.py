#import
import ShareYourSystem as SYS

#define
MyLifer=SYS.LiferClass(
        ).lif(
        ).setAttr(
            'LifingComputeStationaryBool',
            False
        )

#map
PerturbationFrequencyFloatsArray=SYS.numpy.array(
	SYS.numpy.logspace(0,3,100)
);

#init
SYS.Figure=None

#loop
for __PerturbationMethodStr in [
                    "Brunel",
                    "Hakim"
                ]:

    #set
    MyLifer.LifingPerturbationMethodStr=__PerturbationMethodStr
    
    #map
    LifedPerturbationMeanComplexesArray=SYS.numpy.array(
        map(
            lambda __PerturbationFrequencyFloat:
            MyLifer.setAttr(
                    'LifingPerturbationFrequencyFloat',
                    __PerturbationFrequencyFloat
                ).lif(   
                ).LifedPerturbationMeanComplexVariable,
            PerturbationFrequencyFloatsArray
        )
    )

    #plot
    SYS.plot(
        PerturbationFrequencyFloatsArray,
        abs(LifedPerturbationMeanComplexesArray),
        '.-',linewidth=3,markersize=25,
        color='blue' if __PerturbationMethodStr=='Brunel' else 'red'
    );
    
#init figure
SYS.plot(
    [1.,100.],
    [MyLifer.LifedPerturbationNullFloat]*2,
    '--',linewidth=3,markersize=25,color='green'
);
SYS.Axes.set_xscale('log')
SYS.show()
