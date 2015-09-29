import pyvisa
import telepythic
import tekscope
import h5py

# query all available VISA devices
rm = pyvisa.ResourceManager()
# enumerate the USB devices
usbs = rm.list_resources('USB?*::INSTR')
# check there's only one
assert len(usbs) == 1

# open the device
instr = rm.open_resource(usbs[0])
instr.timeout = 1000
# establish communications
dev = telepythic.TelepythicDevice(instr)
scope = tekscope.TekScope(dev)

# check comms and download traces
print 'Connected', dev.id()

import pylab as pyl
import numpy as np

c = ['b','g','r','k']
with h5py.File("scope.h5","w") as F:
	for i in [1,2,3,4]:
		if int(scope.ask('SELect:CH%i?'%i)):
			print 'Downloading channel',i
			wfmo, T, Y = scope.waveform(i)
			D = F.create_dataset("Ch%i"%i,data=np.vstack([T,Y]).T)
			D.attrs.update(wfmo)
			pyl.plot(T,Y,c[i-1])
pyl.show()