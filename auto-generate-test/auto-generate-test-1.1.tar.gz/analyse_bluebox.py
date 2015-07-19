import subprocess 
import Image

def checkLobbyScreen( pID, dut, singlestream_expected, expectedState, scenario):
    msgSuccess = ""
    msgFailure = ""
    callID = dut.api.flex.participant.status(pID)['calls'][0]['callID']
    state = dut.api.flex.call.status(callID)['conferenceState']
    if state == expectedState:
        msgSuccess += '{} conferenceState {!r} is correct\n'.format(scenario, state)
    else:
        msgFailure += '{} conferenceState {!r}, expected {!r}\n'.format(scenario, state, expectedState)

    endpointPageStatus = dut.webapi.endpoints.endpoint_status(callID).getpage()['Status']
    capabilities = endpointPageStatus['Video channels']
    if singlestream_expected:
        runOcropus(pID, dut)
        
    if ('Single-stream' in capabilities) and singlestream_expected:
        msgSuccess += '{} endpoint is Single-stream\n'.format(scenario)
    else:
        if ('Multistream' in capabilities) and (not singlestream_expected):
            msgSuccess += '{} endpoint is Multistream'.format(scenario)
        else:
            msgFailure +='{} expected {}, endpointPageStatus = {}'.format(
                scenario,
                'Single-stream' if singlestream_expected else 'Multistream',
                endpointPageStatus,
            )
    return msgSuccess, msgFailure 

def runOcropus(pid, dut):
    pic_data = dut.api.flex.participant.get_preview(pid, streams=[{'position':0, 'streamIdentifier':'txMainVideo', 'maxWidth': 176, 'maxHeight': 144}])
    mybin = pic_data['streams'][0]['preview']
    with open("/root/automation/ocropy-master/preview.jpg", "wb") as outfile:
        outfile.write(mybin.data)
        
    #subprocess.call("ocropus-nlbin -n /root/automation/ocropy-master/Preview.jpg -o book", shell=True)
    subprocess.call("ocropus-gpageseg -n /root/automation/ocropy-master/book/0001.bin.png", shell=True)
    subprocess.call("ocropus-rpred -m en-default.pyrnn.gz /root/automation/ocropy-master/book/0001/*.png", shell=True)
    
    