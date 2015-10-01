# macros.py
#
# BoA macros to reduce maps, pointing, focus, clean data
#
# 2007-03-24 FB fixed clean and map. changed names to macMethod

import os

# datadir = os.environ.get("BOA_HOME_EXAMPLES")
# datadir = os.environ.get("APEXRAWDATA")
# if datadir:
#    indir(datadir)
# proj('T-77.F-0002-2006')
# proj('T-79.F-0010-2007')


#

def macF(ScanNum='4451', refChan=102):
    """
    Quick focus reduction script
    first solves focus without, then with simple skynoise subtraction
    reference channel for SNF should be different from the pointing channel

    USAGE:  macF('4451',refChan=102)
    """

    read(ScanNum, febe='BOLOSZ-SZACBE')
    data.ReceiverArray.RefChannel = refChan
    medianbase(subscan=0)
    signal(range(refChan - 3, refChan + 2))
    print "..SOLVE FOCUS .. PRESS <Enter>"
    raw_input()
    solveFoc()
    # when 102 is reference then noise filter reference=100 !!!
    medianNoiseRemoval(chanRef=100)
    print "..NOW SNR .. PRESS <Enter>"
    raw_input()
    signal(range(refChan - 3, refChan + 2))
    print "..SOLVE FOCUS .. PRESS <Enter>"
    raw_input()
    solveFoc()

#


def macP(ScanNum='4451', refChan=102, flagChannels=[], radius=0,
         Xpos=0, Ypos=0, newrcp=1, solve=1, plot=1, png=0, oversamp=2):
    """
    Quick pointing reduction script.
    When pointing on a non-ref channel (ie not the one that the rcp's are made for)
    then, then make map with the number of the pointing channel
    Note that solvePointing and solvePointingOnMap yield slightly different results.
    We are not sure which on is right.
    OnMap is more robust, thus take that for now.

    USAGE: macP('4451',refChan=102)
    """

    read(ScanNum, febe='BOLOSZ-SZACBE')
    flagCh([143])
    if newrcp:
        updateRCP('aszca-4522.rcp')
    # we assume that the MBFITS gives the right refChan=102
    # data.ReceiverArray.RefChannel = refChan
    medianBase(subscan=1)

    if np.size(data.ScanParam.SubscanNum) > 1:
        data.flagInTime('lst', below=0)

    signal([refChan])
    print "... NOW showing channel map..PRESS <Enter>"
    raw_input()
    mapping([refChan], oversamp=oversamp, noPlot=0, style='idl2')

    if solve:
        print "... NOW Pointing on map"
        data.solvePointingOnMap([refChan], plot=1, style='idl2')
        print "... NEXT Pointing on data ....PRESS <Enter>"
        raw_input()
        data.solvePointing(
            [refChan],
            plot=1,
            radius=radius,
            Xpos=Xpos,
            Ypos=Ypos,
            fixedPos=0)


#

def macLoop(ScanList=[], plot=0, png=1, rmsClip=2):

    for scan in ScanList:
        try:
            macClean(
                ScanNum=str(scan),
                plot=plot,
                png=png,
                rmsClip=rmsClip,
                gain=0)
        except:
            print "********************************"
            print "*"
            print "* Reduction of scan %s failed!" % str(scan)
            print "*"
            print "********************************"

#


def macClean(ScanNum='4534', newrcp=1, despike=1, flagChannels=[], rmsClip=0,
             plot=1, png=0, gain=0, baseOrder=0, rcpfile='aszca-4639-NEW.rcp'):
    """
    Script to read & clean data, ie. view and remove bad channels, baseline.

    USAGE: clean('4534',flagChannels=[34, 82, 87])
    """

    from .fortran import fStat

    pngFiles = []  # The Names of the png files to be created
    pngDir = '/data2/boa2/aszca/'  # The directory where the png files will be stored

    # indir('./Examples')
    # proj('T-77.F-0002-2006')

    if(ScanNum):
        read(ScanNum, febe='BOLOSZ-SZACBE')

    BogliConfig.point['size'] = 0.01

    # flagC([113,167,169,176])  # flag open channels for LABOCA

    if newrcp:
        print "reading in new rcp file", rcpfile
        flagChannelsRcp = updateRCP(rcpfile)
        flagChannels = concatenate((flagChannels, flagChannelsRcp))
        print 'bad channels according to rcp file:'
        print flagChannels

    if np.size(data.ScanParam.SubscanNum) > 1:
        data.flagInTime('lst', below=0)  # sometimes there are large negatives

    print "reference channel=  " + repr(data.ReceiverArray.RefChannel)

    medianBaseline(subscan=0)  # 0 ORDER BASELINE
    medRms = 8. * fStat.f_median(data.getChanListData(type='rms'))

    chans = array([])
    if plot:
        print "... NEXT PLOTTING BAD CHANNELS ...................."
        signal(chanList=flagChannels, limitsY=[-medRms, medRms])
        new = '1'
        while new != '':
            print "... GIVE CHANNEL NUMBER NOT TO FLAG OR -1 TO UNFLAG ALL OR <ENTER>"
            new = raw_input()
            if new != '':
                chans = concatenate((chans, [int(new)]))
                print chans
                if int(new) == -1:
                    flagChannels = []

    if png:
        name = ScanNum + "-signal-0.ps"
        print name
        op(name + '/CPS')
        signal(
            chanList=flagChannels,
            limitsY=[-medRms,
                     medRms],
            overplot=0,
            ci=1,
            style='l')
        close()
        print "Execute ps2png90 800 " + ScanNum + "-signal-0 &"
        os.system("ps2png90 800 " + ScanNum + "-signal-0 &")
        pngFiles.append(ScanNum + "-signal-0.png")

    if flagChannels:
        flagC(chanList=flagChannels)    # FLAG BAD CHANNELS
        unflagC(chanList=chans)         # UNFLAG SOME AGAIN

    if gain:
        print "... APPLYING GAIN CORRECTION TO UNFLAGGED CHANNELS"
        for i in range(320):
            if not data.ReceiverArray.FlagHandler.isSetOnIndex(i):
                data.Data[:, i] = array(
                    data.Data[:, i] / data.ReceiverArray.Gain[i]).astype(Float32)

    base(order=baseOrder, subscan=0)
    # medianBaseline(subscan=0)        # 0 ORDER BASELINE ALL CHANNELS
    stat()              # compute statistics
    if despike:
        data.despike()        # despike

    if plot:
        print "... NEXT PLOTTING GOOD CHANNELS ........."  # ; raw_input()
        signal(overplot=0, ci=1, style='p')

    if png:
        name = ScanNum + "-signal-1.ps"
        print name
        op(name + '/CPS')
        signal(overplot=0, ci=1, style='l')
        close()
        print "Execute ps2png90 800 " + ScanNum + "-signal-1 &"
        os.system("ps2png90 800 " + ScanNum + "-signal-1 &")
        pngFiles.append(ScanNum + "-signal-1.png")

    rmsbelow = 0
    rmsabove = 0
    medianRms = fStat.f_median(data.getChanListData(type='rms'))

    if plot:                                      # SHOW RMS OF CHANNELS
        print "... NEXT PLOTTING RMS OF CHANNELS .. PRESS <Enter>"
        raw_input()
        BogliConfig.point['size'] = 5
        data.plotRmsChan()
        BogliConfig.point['size'] = 0.01

        line = medianRms * array([1., 1.])
        Plot.plot([0, 330], line, overplot=1, ci=2, style='l', ls=1, width=2)
        if rmsClip:
            line = medianRms / rmsClip * array([1., 1.])
            Plot.plot([0, 330], line, overplot=1, ci=2, style='l', ls=4)
            line = medianRms * rmsClip * array([1., 1.])
            Plot.plot([0, 330], line, overplot=1, ci=2, style='l', ls=4)

        print "... MEDIAN=" + repr(fStat.f_median(data.getChanListData(type='rms')))

        if not rmsClip:
            print "... GIVE SELECTION THRESHOLD ABOVE:"
            rmsabove = raw_input()
            print "... GIVE SELECTION THRESHOLD BELOW:"
            rmsbelow = raw_input()

    if rmsClip:
        if not rmsbelow:
            rmsbelow = medianRms / rmsClip
        if not rmsabove:
            rmsabove = rmsClip * medianRms

    if rmsbelow:
        data.flagRms(below=float(rmsbelow))   # FLAG DEAD CHANNELS BELOW VALUE
    if rmsabove:
        data.flagRms(above=float(rmsabove))           # FLAG NOISY CHANNELS

    if plot:
        # print "... NEXT PLOTTING SIGNAL .... PRESS <Enter>"; raw_input()
        signal(overplot=0, ci=1, style='p')
        chans = array([])
        new = '1'
        while new != '':
            print "... ADD A CHANNEL TO FLAG ..................... OR <ENTER>"
            new = raw_input()
            if new != '':
                chans = concatenate((chans, [int(new)]))
                print chans
        if chans:
            chans = array(chans)
            data.flagChannels(chans)
            # signal(overplot=0,ci=1,style='p')

    if png:
        name = ScanNum + "-signal-2.ps"
        op(name + '/CPS')
        signal(overplot=0, ci=1, style='l')
        close()
        print "Execute ps2png90 800 " + ScanNum + "-signal-2 &"
        os.system("ps2png90 800 " + ScanNum + "-signal-2 &")
        name = ScanNum + "-signal-3.ps"
        op(name + '/CPS')
        signal([100, 102, 103], style='l')
        close()
        print "Execute ps2png90 500 " + ScanNum + "-signal-3 &"
        os.system("ps2png90 500 " + ScanNum + "-signal-3 &")
        pngFiles.append(ScanNum + "-signal-2.png")
        pngFiles.append(ScanNum + "-signal-3.png")

    if plot:
        print "... NEXT PLOTTING CORRELATION .... GIVE REF CHANNEL or -1: "
        chan = raw_input()
        if chan:
            plotCorrel(chanRef=int(chan))

        print "... NEXT PLOTTING CORRELATION MATRIX .. PRESS <Enter>"
        raw_input()
        data.plotCorMatrix(distance=1)

    if png:
        # Create the html file in pngDir:
        htmlFilename = os.path.join(pngDir, ScanNum + ".html")

        # open is overwritten in boa!
        import __builtin__

        print "Writing", htmlFilename
        htmlFile = __builtin__.open(htmlFilename, "w")
        htmlFile.write("<html>\n")
        htmlFile.write("<body>\n")
        for pngFile in pngFiles:
            htmlFile.write("<img src=%s><br>\n" % pngFile)
        htmlFile.write("</body>\n")
        htmlFile.write("</html>\n")
        htmlFile.close()

#


def macAzel(ScanNum='4534', plot=1, png=0):
    """
    USAGE: macAzel('4534')
    """

    from .fortran import fStat

    azimuth = data.ScanParam.get('AzOff')
    elevation = data.ScanParam.get('ElOff')
    azStat = fStat.f_stat(azimuth)
    limitsX = array([-1, 1]) * 2.5 * azStat[1] + azStat[0]
    elStat = fStat.f_stat(elevation)
    limitsY = array([-1, 1]) * 2.5 * elStat[1] + elStat[0]

    if plot:
        azeloff(style='p', limitsX=limitsX, limitsY=limitsY, aspect=0)

    if png:
        name = ScanNum + "-azeloff.ps"
        op(name + '/ps')
        BogliConfig.point['size'] = 2
        azeloff(style='p', limitsX=limitsX, limitsY=limitsY, aspect=0)
        BogliConfig.point['size'] = 0.01
        close()
        os.system("ps2png90 600 " + ScanNum + "-azeloff &")

 #


def macMap(ScanNum='4534', solve=0, despike=0, flagChannels=[], rmsClip=0,
           plot=1, png=0, radius=0, gain=1, weight=1):
    """
    script for simple map reduction

    USAGE: macMap('4534',flagChannels=[ 96,133 ],plot=0,rmsClip=2)
           style : g2r r2g r2b blue gray grey inverse idl2 idl4 idl5
                    (see BogliConfig.lutDir)
    """

    from .fortran import fStat

    macClean(
        ScanNum=ScanNum, newrcp=1, despike=despike, flagChannels=flagChannels,
             rmsClip=rmsClip, plot=plot, png=png)

    print "... NEXT SHOWING AZELOFF ....... PRESS <Enter>"
    raw_input()
    macAzel(ScanNum=ScanNum, plot=plot, png=png)

    if weight:
        computeWeight()

    if plot:
        print "... NEXT SHOWING FIRST LOOK MAP ..........  press <Enter>"
        raw_input()
        mapping()            # make a first-look map
        print "... IF YOU WANT TO FLAG A SOURCE, GIVE RADIUS ..... OR <ENTER>:"
        radius = raw_input()
        if radius != '':
            flagPos(radius=float(radius), Az=0, El=0)
                    # Flag source position. Default flag=5

    print "... NOW BASELINE 1 AND NOISE REMOVAL ...."
    base(order=1)
    medianNoiseRemoval()
    # skynoise(ScanNum=ScanNum,ChanRef=ChanRef,plot=plot, radius=float(radius))

    if plot:
        signal(overplot=0, ci=1, style='l')

    if png:
        name = ScanNum + "-signal-sn.ps"
        op(name + '/ps')
        signal(overplot=0, ci=1, style='l')
        close()
        os.system("ps2png90 700 " + ScanNum + "-signal-sn &")

    if plot:
        print "... NEXT SHOWING RMS................... PRESS <Enter>"
        raw_input()
        BogliConfig.point['size'] = 5
        plotRmsChan()
        BogliConfig.point['size'] = 0.01

    if png:
        BogliConfig.point['size'] = 5
        name = ScanNum + "-rms-sn.ps"
        op(name + '/ps')
        data.plotRmsChan()
        close()
        os.system("ps2png90 600 " + ScanNum + "-rms-sn &")
        BogliConfig.point['size'] = 0.01

    print "... MEDIAN=" + repr(fStat.f_median(data.getChanListData(type='rms')))

    first3 = data.ReceiverArray.checkChanList(
        [])[0:3]    # select 3 channels for FFT
    if plot:
        print "... NEXT SHOWING FFT ............ PRESS <Enter>"
        raw_input()
        data.plotFFT(first3)

    if png:
        name = ScanNum + "-fft-sn.ps"
        op(name + '/ps')
        data.plotFFT(first3)
        close()
        os.system("ps2png90 600 " + ScanNum + "-fft-sn &")

    if radius:
        data.unflag(flag=5)   # unflag the previously flagged circle

    if plot:
        print "... NEXT SHOWING MAP.................. PRESS <Enter>"
        raw_input()
    #   data.horizontalMap()
        mapping()

    if png:
        name = ScanNum + "-map-sn.ps"
        op(name + '/cps')
        mapping()
        # Map.display(style='idl4')
        close()
        os.system("ps2png90 600 " + ScanNum + "-map-sn &")

    ChanRef = data.ReceiverArray.RefChannel

    if plot:
        print "... NEXT SHOWING SIGNAL PLOT REF CHAN.........PRESS <ENTER>"
        raw_input()
        #    data.Data = data.DataBackup
        signal(chanList=[ChanRef], ci=1, style='p')
        #    data.Data = Data_SNR
        #    signal(chanList=[ChanRef],overplot=1,ci=2,style='l')

    if png:
        name = ScanNum + "-signal-ref.ps"
        op(name + '/ps')
        signal(chanList=[ChanRef], ci=1, style='p')
        close()
        os.system("ps2png90 400 " + ScanNum + "-signal-ref &")


#

def macPoint(
    ScanNum='42947',
     ChanRef=102,
     rmsClip=0,
     flagChannels=[],
     radius=0,
     Xpos=0,
     Ypos=0,
     newrcp=1,
     solve=0,
     despike=0,
     plot=1,
     png=0):
    """
    USAGE: execfile('macros.py')
           macPoint('42947')          # strong source
           macPoint('46117',Rad=200)  # fainter source
    """

    # 228 p Jup high noise, off pointed, good for test of SN
    # 229 p Jup noisy, offpointed
    # 252 p Jup low noise

    badChan = [
        1,
        3,
     4,
     5,
     6,
     7,
     8,
     12,
     13,
     14,
     15,
     16,
     56,
     62,
     65,
     70,
     77,
     140,
     79,
     80,
     237,
     288]  # 42947 137

    macClean(
        ScanNum=ScanNum,
        newrcp=1,
     despike=despike,
     flagChannels=badChan,
     rmsClip=rmsClip,
     plot=plot,
     png=png)

    macAzel(ScanNum=ScanNum, plot=plot, png=png)

    if plot:
        # data.equatorialMap(aspect=1)
        print "... NEXT SHOWING MAP................................... PRESS <Enter>"
        raw_input()
        mapping(oversamp=3)
        if not radius:  # IF RADIUS IS NOT ALREADY SET
            print "... TO FLAG A SOURCE FOR base AND Noise, GIVE RADIUS ............ OR <ENTER>:"
            radius = raw_input()

    if radius:
        flagPos(radius=float(radius))  # FLAG SOURCE POSITION. DEFAULT flag=5

    print "... NOW BASELINE 1 AND NOISE REMOVAL ...."
    base(order=1)
    medianNoiseRemoval()
    # skynoise(ScanNum=ScanNum,ChanRef=ChanRef,plot=plot, radius=float(radius))

    if radius:
        data.unflag(flag=5)   # UNFLAG THE PREVIOUSLY FLAGGED CIRCLE

    if solve:
        solvepointing(plot=1, radius=-10, Xpos=Xpos, Ypos=Ypos, circular=0)
        # radius<0 means multiple of beam FWHM
        if png:
            BogliConfig.box['color'] = 4
            BogliConfig.box['linewidth'] = 3
            name = ScanNum + "-map-sn.ps"
            op(name + '/cps')
            data.showPointing(style='idl2')
            close()
            BogliConfig.box['color'] = 1
            BogliConfig.box['linewidth'] = 1
            os.system("ps2png90 600 " + ScanNum + "-map-sn &")

    if plot:
        print "... NEXT SHOWING REF CHANNEL MAP .......................... PRESS <Enter>"
        raw_input()
        # data.equatorialMap([ChanRef],aspect=1)
        mapping([ChanRef], system='HO')

    if solve:
        # data.solvePointing(radius=radius,plot=plot,chanList=[ChanRef],Xpos=Xpos,Ypos=Ypos)
        data.solvePointing(
            plot=1,
            radius=-10,
            Xpos=Xpos,
            Ypos=Ypos,
            circular=0,
            chanList=[ChanRef])
        if png:
            BogliConfig.box['color'] = 3
            BogliConfig.box['linewidth'] = 2
            name = ScanNum + "-map-sn-ref.ps"
            op(name + '/cps')
            data.showPointing(style='idl2')
            close()
            BogliConfig.box['color'] = 1
            BogliConfig.box['linewidth'] = 1
            os.system("ps2png90 600 " + ScanNum + "-map-sn-ref &")

    # skynoise(ChanRef=ChanRef,plot=plot)

#    if plot:
#        data.equatorialMap(aspect=1)
#    if solve:
#        data.solvePointing (radius=Rad,plot=plot,chanList=[],Xpos=Xpos,Ypos=Ypos)
# print "...  NEXT SHOWING SIGNAL PLOT  ......................PRESS
# <Enter>" ; raw_input()

#    Data_SNR = data.Data
#    data.Data = data.DataBackup
#    signal(ci=1,style='p')
#    data.Data = Data_SNR
#    signal(overplot=1,ci=2,style='p')

    if plot:
        print "... NEXT SHOWING SIGNAL PLOT REF CHAN.................PRESS <ENTER>"
        raw_input()
        #    data.Data = data.DataBackup
        signal(chanList=[ChanRef], ci=1, style='l')
        #    data.Data = Data_SNR
        #    signal(chanList=[ChanRef],overplot=1,ci=2,style='l')

    if png:
        name = ScanNum + "-signal-ref.ps"
        op(name + '/ps')
        signal(chanList=[ChanRef], ci=1, style='l')
        close()
        os.system("ps2png90 400 " + ScanNum + "-signal-ref &")

#


def macSkydip(ScanNum='316', ChanRef=0, plot=1, solve=1):
    """
    Reduce a skydip observation
    """
    read(ScanNum)

    if not data.ReceiverArray.checkChanList(array(ChanRef)):
        ChanRef = data.ReceiverArray.RefChannel

    # Retrieve signal and elevation
    s = data.getChanData('flux', ChanRef)
    e = data.getChanData('el')
    e = (90. - e) * pi / 180.  # convert to zenithal distance, in radians
    if plot:
        Plot.plot(
            1. / cos(e),
            s,
            labelX='Airmass',
            labelY='Counts',
            caption=data.ScanParam.caption())

    if solve:
        # TODO: linear fit
        pass

#


def macCmpRms(scan, pos=0, window=100, outdir='', pngplot=0):
    """
    Estimate RMS for a given observation using median filter
    """

    read(str(scan), febe='BOLOSZ-SZACBE')

    medianBaseline()

    doPlot = ((outdir != '') & pngplot)
    if doPlot:
        op(outdir + '/' + str(scan) + '_medianbaseline.ps/CPS')
    r = data.medianFilter(plot=1, limitsY=[-60, 60], subtract=1, window=window)
    if doPlot:
        close()
        os.system("ps2png90 600 " + outdir +
                  '/' + str(scan) + '_medianbaseline &')

    if pos != 0:
        updateRCP('aszca-' + str(scan) + '-uncalib.rcp')
        data.flagPosition(pos, radius=180)

    itDespike(below=-4, above=4)

    c = checkChanList([])
    rms = data.getChanListData('rms')

    if (outdir != ''):
        a = file(outdir + '/Channel-RMS_' + str(scan) + '.dat', 'w')
        for i in range(len(c)):
            a.write(str(c[i]) + ' ')
            a.write(str(rms[i]))
            a.write('\n')
        a.close()

    if doPlot:
        op(outdir + '/' + str(scan) + '_rms.ps/CPS')
    signal(limitsY=[-60, 60])
    if pngplot:
        close()
        os.system("ps2png90 600 " + outdir + '/' + str(scan) + '_rms &')


#
