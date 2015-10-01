import numpy as np
from .fortran import fStat
from .Bogli import DeviceHandler, Plot, MultiPlot


def telescopeSpeed(ScanParam, wait=1, style='p'):
    MJD = ScanParam.get('MJD').astype(np.float64)
    azimuth = ScanParam.get('Azimuth').astype(np.float64)
    elevation = ScanParam.get('Elevation').astype(np.float64)

    # Basic plots
    # Azimuth/Elevation
    azStat = fStat.basicstat(azimuth)
    limitsY = np.array([-1, 1]) * 3 * azStat[1] + azStat[0]
    Plot.plot(MJD, azimuth, style=style,
              labelX='MJD-MJD[0] (sec)', labelY='azimuth (deg)',
              limitsY=limitsY,
              caption=ScanParam.caption())

    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    elStat = fStat.basicstat(elevation)
    limitsY = np.array([-1, 1]) * 3 * elStat[1] + elStat[0]
    Plot.plot(MJD, elevation, style=style,
              labelX='MJD-MJD[0] (sec)', labelY='elevation (deg)',
              limitsY=limitsY,
              caption=ScanParam.caption())

    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    limitsX = np.array([-1, 1]) * 3 * azStat[1] + azStat[0]
    limitsY = np.array([-1, 1]) * 3 * elStat[1] + elStat[0]
    Plot.plot(azimuth, elevation, style=style,
              labelX='azimuth (deg)', labelY='elevation (deg)',
              limitsX=limitsX, limitsY=limitsY,
              caption=ScanParam.caption())

    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    # Speed

    dt = MJD[1:] - MJD[:-1]
    azimuthSpeed = (azimuth[1:] - azimuth[:-1]) / dt
    elevationSpeed = (elevation[1:] - elevation[:-1]) / dt

    azSpeedStat = fStat.basicstat(azimuthSpeed)
    elSpeedStat = fStat.basicstat(elevationSpeed)

    limitsY = np.array([-1, 1]) * 4 * azSpeedStat[1] + azSpeedStat[0]
    Plot.plot(MJD[:-1], azimuthSpeed, style=style,
              labelX='MJD-MJD[0] (sec)', labelY='Azimuth Speed (deg/s)',
              limitsY=limitsY,
              caption=ScanParam.caption())
    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    limitsY = np.array([-1, 1]) * 4 * elSpeedStat[1] + elSpeedStat[0]
    Plot.plot(MJD[:-1], elevationSpeed, style=style,
              labelX='MJD-MJD[0] (sec)', labelY='Elevation Speed (deg/s)',
              limitsY=limitsY,
              caption=ScanParam.caption())

    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    limitsX = np.array([-1, 1]) * 4 * azSpeedStat[1] + azSpeedStat[0]
    limitsY = np.array([-1, 1]) * 4 * elSpeedStat[1] + elSpeedStat[0]
    Plot.plot(azimuthSpeed, elevationSpeed, style=style,
              labelX='Azimuth Speed (deg/s)', labelY='Elevation Speed (deg/s)',
              limitsX=limitsX, limitsY=limitsY, aspect=1,
              caption=ScanParam.caption())

    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    # Accelation
    azimuthAccel = (azimuthSpeed[1:] - azimuthSpeed[:-1]) / dt[:-1]
    elevationAccel = (elevationSpeed[1:] - elevationSpeed[:-1]) / dt[:-1]

    azAccelStat = fStat.basicstat(azimuthAccel)
    elAccelStat = fStat.basicstat(elevationAccel)

    limitsY = np.array([-1, 1]) * 5 * azAccelStat[1] + azAccelStat[0]
    Plot.plot(MJD[:-1], azimuthAccel, style=style,
              labelX='MJD-MJD[0] (sec)', labelY='Azimuth Accel (deg/s2)',
              limitsY=limitsY,
              caption=ScanParam.caption())
    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    limitsY = np.array([-1, 1]) * 5 * elAccelStat[1] + elAccelStat[0]
    Plot.plot(MJD[:-1], elevationAccel, style=style,
              labelX='MJD-MJD[0] (sec)', labelY='Elevation Accel (deg/s2)',
              limitsY=limitsY,
              caption=ScanParam.caption())

    if wait:
        print "Press Enter to proceed"
        raw_input()
    Plot.clear()

    limitsX = np.array([-1, 1]) * 5 * azAccelStat[1] + azAccelStat[0]
    limitsY = np.array([-1, 1]) * 5 * elAccelStat[1] + elAccelStat[0]
    Plot.plot(azimuthAccel, elevationAccel, style=style,
              labelX='Azimuth Accel (deg/s2)', labelY='Elevation Accel (deg/s2)',
              limitsX=limitsX, limitsY=limitsY, aspect=1,
              caption=ScanParam.caption())
