import ShareYourSystem as SYS;

MyPredicter=SYS.PredicterClass(
    ).predict(
        _CommandVariable="#custom:#clock:25*ms:1.*(1.*mV+1.*mV*(int(t==25.*ms)+int(t==50.*ms)))",#2., 
        _AgentUnitsInt = 1000,
        _AgentRecordVariable = [0,1,2],
        _DecoderVariable="#array",
        _DecoderStdFloat = 200./SYS.numpy.sqrt(1000.), #need to make an individual PSP around 1 mV
        _DecoderMeanVariable = 0., 
        _AgentResetVariable = -62., #cost to reset neurons and make the noise then decide who is going to spike next
        _AgentNoiseVariable = 2., #noise (mV) to make neurons not spiking at the same timestep
        _AgentThresholdVariable = -59.,  #set the threshold the same for everybody
        _SpikeRecordVariable = range(0,100),
        _AgentRefractoryVariable=0.5,
        _InteractionStr = "Spike"
    ).simulate(
        100. #(ms)
    ).view(
    ).pyplot(
        _FigureVariable={'figsize':(15,10)},
        _GridVariable=(40,30)
    ).show(
    )
