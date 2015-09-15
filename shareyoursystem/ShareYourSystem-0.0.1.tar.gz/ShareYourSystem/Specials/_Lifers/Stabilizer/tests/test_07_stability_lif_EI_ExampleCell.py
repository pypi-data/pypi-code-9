#ImportModules
import ShareYourSystem as SYS

"""
Nicolas tests

rates 5-15 sigmaext 5-5
taums 20-10 thresholds 20-20 resets 10-10 taurps 0-0
delays 1-1 taur 0.5-0.5 taud 5-5

JEE, JEI, JIE, JII=100,100,100,100:
stable, eigenvalue w largest real part = -36,0

100,100,100,0:
unstable,  128, 184 (f=29Hz)

0,100,100,100:
stable, -15, 338

100,0,0,0:
unstable, 135, 0

0,100,100,0:
unstable, 99, 240 (f=38Hz)


"""

#ImportModules
import ShareYourSystem as SYS

LateralWeightVariablesList=[
    #[[100,-100],[100,-100]],
    [[100,-100],[100,-0]],
    #[[0,-100],[100,-100]],
    #[[100,-0],[0,-0]],
    #[[0,-100],[100,-0]]
    #[[0,0],[0,-100]],
]

#Check
for __LateralWeightVariable in LateralWeightVariablesList:

    #Define
    MyStabilizer=SYS.StabilizerClass(
        ).stationarize(
            _MeanWeightVariable=__LateralWeightVariable,
            _ConstantTimeVariable=[0.02,0.01],
            _RateVariable=[5.,15.],
            _InteractionStr="Spike"
        ).stabilize(
            _DelayTimeVariable=0.001,
            _DecayTimeVariable=0.005,
            _RiseTimeVariable=0.0005,
            #_ScanFrequencyVariable=[10.]
        )

    #Choose the parameters to print
    KeyStrsList=[
        'StationarizingMeanWeightVariable',
        'StabilizingConstantTimeVariable', #in ms
        'StabilizingDelayTimeVariable',
        'StabilizedPerturbationComplex',
        'StabilizedTotalPerturbationComplexesArray', #matrix M
        'StabilizedDeterminantFloatsTuple',  #If it has converged, then it has to be closed to (0,0)
        'StabilizedBiggestLambdaFloatsTuple',
        'StabilizedInstabilityLambdaFloatsTuple',  # real part should be negative if stable,  (from this particular initial condition)
        'StabilizedInstabilityFrequencyFloat'
    ]

    #print
    SYS._print(SYS.collections.OrderedDict(zip(KeyStrsList,MyStabilizer.mapGet(KeyStrsList))))

