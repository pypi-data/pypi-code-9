#!/usr/bin/env python

# import required libraries
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import numpy as np
from pyrf.devices.thinkrf import WSA
from pyrf.util import read_data_and_context



# plot constants
CENTER_FREQ = 2450 * 1e6 
SAMPLE_SIZE = 1024
ATTENUATOR = 0
DECIMATION = 1
RFE_MODE = 'HDR'


# connect to WSA device
dut = WSA()
ip = sys.argv[1]
dut.connect(ip)


# initialize WSA configurations
dut.reset()
dut.request_read_perm()
dut.freq(CENTER_FREQ)
dut.decimation(DECIMATION)
dut.attenuator(ATTENUATOR)
dut.rfe_mode(RFE_MODE)


data, context = read_data_and_context(dut, SAMPLE_SIZE)
i_data = np.array(data.data.numpy_array(), dtype=float)
print i_data
