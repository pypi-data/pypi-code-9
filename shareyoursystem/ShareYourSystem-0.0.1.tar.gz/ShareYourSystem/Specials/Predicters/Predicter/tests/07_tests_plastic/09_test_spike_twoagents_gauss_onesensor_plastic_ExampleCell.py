import ShareYourSystem as SYS;SYS.DebugPrintBool=False;

MyPredicter=SYS.PredicterClass(
    ).predict(
        _AgentUnitsInt=2,
        _CommandVariable="#custom:#clock:20*ms:0.5*(1.*mV+1.*mV*(int(t==20*ms)+int(t==80*ms)))",#2.,
        _DecoderVariable=[2.,2.],
        _AgentRecordVariable=[0,1],
        _FastWeightVariable=[[-0.3,-0.2],[-0.1,0.1]],
        _InteractionStr="Spike",
        #_AgentResetVariable=-70.,
        #_AgentRefractoryVariable=0.5 BE CAREFUL NOT WORKING BECAUSE auto IPSP is then not inducted
        _FastPlasticBool=True,
    ).simulate(
        200. #(ms)
    ).view(
    ).pyplot(
        _FigureVariable={'figsize':(18,10)},
        _GridVariable=(50,30)
    ).show(
    )
