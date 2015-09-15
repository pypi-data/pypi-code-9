import ShareYourSystem as SYS;SYS.DebugPrintBool=False;

MyPredicter=SYS.PredicterClass(
    ).predict(
        _CommandVariable="#custom:#clock:50*ms:0.5*(1.*mV+1.*mV*(int(t==50*ms)+int(t==150*ms)))",#2., 
        _AgentUnitsInt = 100,
        _AgentRecordVariable = [0,1,2],
        _DecoderVariable="#array",
        _DecoderStdFloat = 50./SYS.numpy.sqrt(100.), #need to make an individual PSP around 1 mV
        _DecoderMeanVariable = 50., 
        _AgentResetVariable = -70., #cost to reset neurons and make the noise then decide who is going to spike next
        _AgentNoiseVariable = 1., #noise (mV) to make neurons not spiking at the same timestep
        #_AgentThresholdVariable = -59.,  #set the threshold the same for everybody
        _SpikeRecordVariable = range(0,100),
        _AgentRefractoryVariable=0.5,
        _InteractionStr = "Spike",
        #_FastWeightVariable = 0.01*SYS.scipy.stats.norm.rvs(size=1000000).reshape((1000,1000)), #0mega fast array
        _FastPlasticBool = True,
        #_FastLearnRateFloat = 0.01
    ).simulate(
        200. #(ms)
    ).view(
    ).pyplot(
        _FigureVariable={'figsize':(18,10)},
        _GridVariable=(50,30)
    ).show(
    )
