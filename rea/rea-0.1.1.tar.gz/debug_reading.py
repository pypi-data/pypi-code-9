import os
import numpy as np
from rea import ReaMBFits, ReaMBFitsReader, ReaDataEntity

path = '/data/abeelen/APEX/c-081.f-0015a-2008'
filename = 'APEX-20772-2008-06-08-C-081.F-0015A-2008'

path = '/data/abeelen/NIKA/Run10/TotalImbfits'
filename = 'iram30m-NIKA2mm-20141109s198-imb.fits'

subscans = []
readHe = 0
readAzEl0 = 0
readT = 0
readWind = 0
readBias = 0
readPWV = 0
channelFlag = 9
integrationFlag = 9

dataset = ReaMBFits.importDataset(os.path.join(path, filename))
reader = ReaMBFitsReader.createReader(dataset)
nSub = reader.openSubscan(subsnum=None)
febesDataset = reader.read("Febes")
useFebe = febesDataset[0]
basebandsDataset = reader.read("UseBand", febe=useFebe)
useBaseband = basebandsDataset[0]
subscansDataset = reader.read("Subscans")
useSubscans = subscansDataset
channelFlag = 1
timeline = ReaDataEntity.TimelineData()
# receiverArray = ReaDataEntity.ReceiverArray()
# scanParam = ReaDataEntity.ScanParameter()

try:
    timeline.ReceiverArray._ReceiverArray__fillFromMBFits(
        reader=reader,
        febe=useFebe,
     baseband=useBaseband,
     subscan=useSubscans[0],
     flag=channelFlag)
except:
    self = timeline.ReceiverArray
    febe = useFebe
    baseband = useBaseband
    subscan = useSubscans[0]
    flag = channelFlag

    useBand = reader.read("UseBand", febe=febe)
    indexBaseband = -1
    for iBand in xrange(len(useBand)):
        if useBand[iBand] == baseband:
            indexBaseband = iBand

    nChannels = reader.read("FebeFeed", febe=febe)
    self.NChannels = nChannels
    usedChannels = reader.read("UseFeed", febe=febe)[indexBaseband]
    if len(usedChannels.shape) == 3:
        usedChannels = usedChannels[0, :, 0]
    nbUsedChan = reader.read("NUseFeeds", febe=febe)[indexBaseband]
    usedChannels = usedChannels[
        :nbUsedChan]  # TODO: Is it really necessary ?!?
    refChannel = reader.read("RefFeed", febe=febe)
    feedType = reader.read("FeedType", febe=febe)[indexBaseband]
    feedString = reader.read("FeedCode", febe=febe)
    offX = reader.read("FeedOffX", febe=febe)
    offY = reader.read("FeedOffY", febe=febe)
    self.Gain = reader.read("FlatField", febe=febe)[indexBaseband]
    self.DCOff = reader.read("DCoffset", febe=febe)[indexBaseband]
    gains = reader._readGains(febe=febe)
    self.JyPerCount = reader.read("BolCalFc", febe=febe)
    self.UsedChannels = usedChannels
    self.CurrChanList = usedChannels
    self.NUsedChannels = len(usedChannels)
    self.RefChannel = refChannel
    self.Telescope.set(reader.read("Telescope", febe=febe),
                       float(reader.read("Diameter", febe=febe)),
                       float(reader.read("SiteLong", febe=febe)),
                       float(reader.read("SiteLat", febe=febe)),
                       float(reader.read("SiteElev", febe=febe)))

    # Still missing for NIKA
    freq = reader.read(
        "RestFreq",
        febe=febe,
     baseband=baseband,
     subsnum=subscan)
    self.DewCabin = reader.read("DewCabin", febe=febe)
    self.DewUser = reader.read("DewUser", febe=febe)
    self.DewExtra = reader.read("DewExtra", febe=febe, subsnum=subscan)


timeline.ScanParam.Telescope = timeline.ReceiverArray.Telescope

try:
    timeline.ScanParam._ScanParameter__fillFromMBFits(reader=reader,
                                                      febe=useFebe,
                                                      baseband=useBaseband,
                                                      subscans=useSubscans,
                                                      flag=integrationFlag,
                                                      readHe=readHe, readAzEl0=readAzEl0,
                                                      readT=readT, readWind=readWind,
                                                      readBias=readBias, readPWV=readPWV)
except:

    self = timeline.ScanParam
    reader = reader
    febe = useFebe
    baseband = useBaseband
    subscans = useSubscans
    flag = integrationFlag
    readHe = readHe
    readAzEl0 = readAzEl0
    readT = readT
    readWind = readWind
    readBias = readBias
    readPWV = readPWV
    self.ScanNum = reader.read("ScanNum")
    self.DateObs = reader.read("DateObs")
    self.ScanType = reader.read("ScanType")
    self.ScanMode = reader.read("ScanMode", subsnum=subscans[0])

    self.Object = reader.read("Object")
    self.Equinox = reader.read("Equinox")
    self.Basis = reader.read("Basis")
    self.Coord = reader.read("Coord")

    self.Frames = reader.read("UsrFrame", subsnum=subscans[0])

    # Missing for NIKA
    WobUsed = reader.read("WobUsed")

    self.DeltaCA = float(reader.read("DeltaCA"))
    self.DeltaIE = float(reader.read("DeltaIE"))

    self.TAIUTC = float(reader.read("TAIUTC"))
    self.UTCUT1 = float(reader.read("UTCUT1"))
    nIntegSubscan = {}
    nIntegTotal = 0
    for subscan in subscans:
        subscanWasOpened = reader.openSubscan(subsnum=subscan)
        nIntegSubscan[subscan] = reader.read("NInteg",
                                             subsnum=subscan,
                                             febe=febe,
                                             baseband=baseband)
        nIntegTotal += nIntegSubscan[subscan]
        if subscanWasOpened:
            reader.closeSubscan(subsnum=subscan)

    self.NInt = nIntegTotal
    self.NObs = reader.read("NObs")
    subscan = subscans[0]
    nbData = nIntegSubscan[subscan]
    subscanWasOpened = reader.openSubscan(subsnum=subscan)
    MJD = reader.read("MJD",
                      subsnum=subscan, febe=febe).astype(np.float64)
    LST = reader.read("LST",
                      subsnum=subscan,
                      febe=febe).astype(np.float32)
    Az = reader.read("Az",
                     subsnum=subscan,
                     febe=febe).astype(np.float32)
    El = reader.read("El",
                     subsnum=subscan,
                     febe=febe).astype(np.float32)
    # MeanRa = reader.read("Ra",
    #                      subsnum=subscan,
    #                      febe=febe).astype(np.float32)
    # MeanDec = reader.read("Dec",
    #                        subsnum=subscan,
    #                        febe=febe).astype(np.float32)
    LonOff = reader.read("LonOff",
                         subsnum=subscan,
                         febe=febe).astype(np.float32)
    LatOff = reader.read("LatOff",
                         subsnum=subscan,
                         febe=febe).astype(np.float32)
    BasLon = reader.read("BasLon",
                         subsnum=subscan,
                         febe=febe).astype(np.float32)
    BasLat = reader.read("BasLat",
                         subsnum=subscan,
                         febe=febe).astype(np.float32)
    Rot = reader.read("RotAngle",
                      subsnum=subscan,
                      febe=febe).astype(np.float32)
    # Missing for NIKA
    reFrac = reader.read("Refract", subsnum=subscan)
    obsType = reader.read("ObsType", subsnum=subscan, febe=febe)
    # Missing for NIKA
    SubscanDir = reader.read("ScanDir", subsnum=subscan, febe=febe)
    date_tmp = reader.read("SubsStart", subsnum=subscan, febe=febe)
    if subscanWasOpened:
        reader.closeSubscan(subsnum=subscan)

try:
    timeline._TimelineData__fillFromMBFits(reader=reader,
                                           febe=useFebe,
                                           baseband=useBaseband,
                                           subscans=useSubscans)
except:
    self = timeline
    reader = reader
    febe = useFebe
    baseband = useBaseband
    subscans = useSubscans

    nUseFeed = reader.read("NUseFeed",
                           subsnum=subscans[0],
                           febe=febe,
                           baseband=baseband)
    subscan = subscans[0]
    subsIndex = 0

    subscanWasOpened = reader.openSubscan(subsnum=subscan)
    subscanStart = self.ScanParam.SubscanIndex[0, subsIndex]
    subscanStop = self.ScanParam.SubscanIndex[1, subsIndex]
    tmpData = reader.read("Data",
                          subsnum=subscan,
                          febe=febe,
                          baseband=baseband)
    if subscanWasOpened:
        reader.closeSubscan(subsnum=subscan)
